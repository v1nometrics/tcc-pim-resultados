"""
06_build_panel.py
Monta o painel final (subsetor × ano) unificando fontes SUFRAMA + IBGE + BCB.

Fontes de dados:
  - SUFRAMA (Cadernos de Indicadores de Desempenho do PIM):
      Faturamento, CAPEX, Mão-de-Obra, ICMS, Salários/Encargos/Benefícios
  - IBGE: deflator IPCA (base 2023), PIB Manaus
  - BCB: PTAX (câmbio anual médio via API OLINDA)

Especificação DEA (Cooper, Seiford & Tone, 2007):
  Inputs  = (ICMS restituído real, CAPEX real)       → custo fiscal + investimento privado
  Outputs = (Faturamento real, Emprego SUFRAMA)       → retorno econômico + social

Decisões metodológicas:
  - Emprego = SUFRAMA (média mensal: efetiva + temporária + terceirizada).
    Fonte primária porque: (a) cobre universo exato do PIM, (b) inclui terceirizados,
    (c) consistência interna com demais variáveis SUFRAMA, (d) sem necessidade de
    crosswalk CNAE→Subsetor (suscetível a erro de enquadramento).
  - VA (Valor Adicionado) NÃO é calculado: insumos disponíveis apenas para 11/23
    subsetores (cf. Gouvêa 2024, Bolognese 2024). Todos usam Faturamento.
  - Incentivo fiscal = ICMS restituído (dado observado por subsetor).
  - Incentivos federais (II, IPI, PIS/COFINS): agregados no DGT, sem desagregação
    por subsetor. Rateio proporcional circular com faturamento → descritivo apenas.
  - Câmbio: API BCB PTAX (média anual compra+venda, Resolução 3.568/2008).

Variáveis derivadas (K-means / Simar-Wilson):
  - automacao            = K / L   (CAPEX por empregado — proxy de automação)
  - salario_medio        = W / L   (massa salarial por empregado — proxy capital humano)
  - incentivo_faturamento = I / Fat (intensidade fiscal)
  - incentivo_emprego     = I / L   (incentivo por empregado)
  - produtividade_trabalho = Fat / L (produtividade do trabalho)

Salva em data/processed/painel_subsetor_ano.csv
"""

import pandas as pd
import numpy as np
import requests
import os
import sys
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
INTERIM_DIR = os.path.join(BASE_DIR, "data", "interim")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(INTERIM_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

ANOS = [2018, 2019, 2020, 2021, 2022, 2023]

print("=" * 70)
print("  CONSTRUÇÃO DO PAINEL — TCC ZFM (v3 — emprego SUFRAMA, salários, zero estrutural)")
print("=" * 70)


# ============================================================
# 0. COLETA DE CÂMBIO VIA API BCB PTAX
# ============================================================
def fetch_ptax_annual(anos: list[int]) -> dict[int, float]:
    """
    Obtém PTAX média anual (média de compra e venda, média diária do ano)
    via API OLINDA do BCB.
    Retorna dict {ano: taxa_media_anual}.

    Referência: BCB Resolução 3.568/2008 — PTAX é a taxa oficial para
    conversão de obrigações em moeda estrangeira.
    """
    print("\n0. COLETANDO PTAX ANUAL VIA API BCB...")

    fx_rates = {}
    for ano in anos:
        dt_ini = f"01-01-{ano}"
        dt_fim = f"12-31-{ano}"
        url = (
            "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
            f"CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
            f"?@dataInicial='{dt_ini}'&@dataFinalCotacao='{dt_fim}'"
            f"&$format=json"
            f"&$select=cotacaoCompra,cotacaoVenda,dataHoraCotacao"
        )

        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            data = resp.json().get("value", [])

            if not data:
                print(f"  ⚠️ {ano}: sem dados PTAX")
                continue

            # Média anual = média de todas as cotações diárias
            compras = [d["cotacaoCompra"] for d in data if d.get("cotacaoCompra")]
            vendas = [d["cotacaoVenda"] for d in data if d.get("cotacaoVenda")]

            if compras and vendas:
                media_compra = np.mean(compras)
                media_venda = np.mean(vendas)
                ptax_media = (media_compra + media_venda) / 2
                fx_rates[ano] = round(ptax_media, 4)
                print(f"  {ano}: PTAX média = R$ {ptax_media:.4f}/USD "
                      f"({len(compras)} cotações, compra={media_compra:.4f}, venda={media_venda:.4f})")
            else:
                print(f"  ⚠️ {ano}: dados incompletos ({len(compras)} compras, {len(vendas)} vendas)")

        except Exception as e:
            print(f"  ⚠️ {ano}: erro na API BCB — {e}")

    # Fallback para anos sem dados da API
    FALLBACK = {2018: 3.6558, 2019: 3.9461, 2020: 5.1964,
                2021: 5.3956, 2022: 5.1655, 2023: 4.9942}
    for ano in anos:
        if ano not in fx_rates:
            fx_rates[ano] = FALLBACK.get(ano, 5.0)
            print(f"  {ano}: usando fallback = {fx_rates[ano]}")

    return fx_rates


# ============================================================
# 1. CARREGAR DADOS BRUTOS
# ============================================================
print("\n1. CARREGANDO DADOS BRUTOS...")

# Deflator
df_defl = pd.read_csv(os.path.join(RAW_DIR, "deflator_anual_2023.csv"))
defl_map = dict(zip(df_defl["ano"], df_defl["deflator_2023"]))
print(f"  Deflator: {defl_map}")

# PIB Manaus
df_pib = pd.read_csv(os.path.join(RAW_DIR, "pib_municipal_manaus.csv"))
# Handle both old format (2 cols) and new format (multi-variable)
if "variavel_id" in df_pib.columns:
    df_pib_total = df_pib[df_pib["variavel_id"] == 37][["ano", "valor_mil_reais"]].copy()
    df_pib_total.columns = ["ano", "pib_manaus_mil_reais"]
    pib_map = dict(zip(df_pib_total["ano"], df_pib_total["pib_manaus_mil_reais"]))
else:
    pib_map = dict(zip(df_pib["ano"], df_pib["pib_manaus_mil_reais"]))
print(f"  PIB Manaus: {pib_map}")

# Faturamento
df_fat = pd.read_csv(os.path.join(RAW_DIR, "suframa_faturamento_subsetor.csv"))
print(f"  Faturamento: {len(df_fat)} linhas, {df_fat['subsetor'].nunique()} subsetores")

# CAPEX (em US$)
df_capex = pd.read_csv(os.path.join(RAW_DIR, "suframa_capex_subsetor.csv"))
print(f"  CAPEX: {len(df_capex)} linhas, {df_capex['subsetor'].nunique()} subsetores")

# Emprego SUFRAMA — Output DEA principal
# Nota metodológica: "Dados médios mensais de Mão-de-obra efetiva + temporária + terceirizada"
# Fonte: Cadernos de Indicadores de Desempenho do PIM (SUFRAMA)
df_emp = pd.read_csv(os.path.join(RAW_DIR, "suframa_emprego_subsetor.csv"))
print(f"  Emprego SUFRAMA (Output DEA): {len(df_emp)} linhas, {df_emp['subsetor'].nunique()} subsetores")

# Salários, Encargos e Benefícios Sociais (variável estrutural K-means / Simar-Wilson)
sal_path = os.path.join(RAW_DIR, "suframa_salarios_subsetor.csv")
df_sal = None
if os.path.exists(sal_path):
    df_sal = pd.read_csv(sal_path)
    print(f"  Salários SUFRAMA: {len(df_sal)} linhas, {df_sal['subsetor'].nunique()} subsetores")
else:
    print("  ℹ️ suframa_salarios_subsetor.csv não encontrado — execute 02_suframa_extract.py")

# ICMS
df_icms = pd.read_csv(os.path.join(RAW_DIR, "suframa_icms_subsetor.csv"))
print(f"  ICMS: {len(df_icms)} linhas, {df_icms['subsetor'].nunique()} subsetores")

# Câmbio via API BCB
fx_rates = fetch_ptax_annual(ANOS)


# ============================================================
# 2. HARMONIZAR SUBSETORES
# ============================================================
print("\n2. HARMONIZANDO SUBSETORES...")

all_subsetors = set()
dfs_harmonize = [("fat", df_fat), ("capex", df_capex), ("emp", df_emp), ("icms", df_icms)]
if df_sal is not None:
    dfs_harmonize.append(("sal", df_sal))
for name, df in dfs_harmonize:
    subs = set(df["subsetor"].unique()) - {"TOTAL"}
    all_subsetors.update(subs)
    print(f"  {name}: {len(subs)} subsetores")

print(f"\n  Todos os subsetores ({len(all_subsetors)}): {sorted(all_subsetors)}")

# Merge "Bens de Informática" → "Eletroeletrônico" no faturamento
print("\n  Merging 'Bens de Informática' into 'Eletroeletrônico' no faturamento...")
mask_bi = df_fat["subsetor"] == "Bens de Informática"
mask_ee = df_fat["subsetor"] == "Eletroeletrônico"
if mask_bi.any():
    bi_data = df_fat[mask_bi].set_index("ano")["faturamento_brl"]
    for idx in df_fat[mask_ee].index:
        ano = df_fat.loc[idx, "ano"]
        if ano in bi_data.index:
            df_fat.loc[idx, "faturamento_brl"] += bi_data[ano]
    df_fat = df_fat[~mask_bi].copy()
    print(f"  Faturamento após merge: {df_fat['subsetor'].nunique()} subsetores")


# ============================================================
# 3. CONSTRUIR PAINEL BASE
# ============================================================
print("\n3. CONSTRUINDO PAINEL BASE...")

# Remove TOTAL rows
df_fat = df_fat[df_fat["subsetor"] != "TOTAL"].copy()
df_capex = df_capex[df_capex["subsetor"] != "TOTAL"].copy()
df_emp = df_emp[df_emp["subsetor"] != "TOTAL"].copy()
df_icms = df_icms[df_icms["subsetor"] != "TOTAL"].copy()
if df_sal is not None:
    df_sal = df_sal[df_sal["subsetor"] != "TOTAL"].copy()

# Start with faturamento as base
panel = df_fat[["subsetor", "ano", "faturamento_brl"]].copy()

# Merge CAPEX
panel = panel.merge(
    df_capex[["subsetor", "ano", "capex_usd"]],
    on=["subsetor", "ano"], how="left"
)

# Merge emprego SUFRAMA — Output DEA principal
# "Dados médios mensais de Mão-de-obra efetiva + temporária + terceirizada"
panel = panel.merge(
    df_emp[["subsetor", "ano", "emprego_suframa"]],
    on=["subsetor", "ano"], how="left"
)
panel["emprego"] = panel["emprego_suframa"]

# Merge Salários/Encargos/Benefícios (variável estrutural)
if df_sal is not None:
    sal_cols = [c for c in df_sal.columns if c not in ["subsetor", "ano"]]
    panel = panel.merge(
        df_sal[["subsetor", "ano"] + sal_cols],
        on=["subsetor", "ano"], how="left"
    )
    print(f"  Salários merged: {sal_cols}")

# Merge ICMS
panel = panel.merge(
    df_icms[["subsetor", "ano", "icms_recolhido", "icms_restituido", "icms_devido"]],
    on=["subsetor", "ano"], how="left"
)

print(f"  Painel bruto: {panel.shape}")
print(f"  Subsetores: {panel['subsetor'].nunique()}")
print(f"  Obs por ano: {panel.groupby('ano').size().to_dict()}")


# ============================================================
# 4. CALCULAR VARIÁVEIS DERIVADAS
# ============================================================
print("\n4. CALCULANDO VARIÁVEIS DERIVADAS...")

# 4.1 Convert CAPEX from USD to BRL via PTAX (API BCB)
print(f"  PTAX utilizada: {fx_rates}")
panel["capex_brl"] = panel.apply(
    lambda r: r["capex_usd"] * fx_rates.get(int(r["ano"]), 5.0), axis=1
)

# 4.2 Incentivo fiscal = ICMS restituído (dado observado por subsetor)
panel["incentivo_fiscal_brl"] = panel["icms_restituido"].fillna(0)

# 4.3 Deflacionar para R$ constantes de 2023
COLS_DEFLATE = {
    "faturamento_brl": "faturamento_real2023",
    "capex_brl": "capex_real2023",
    "incentivo_fiscal_brl": "incentivo_fiscal_real2023",
    "icms_recolhido": "icms_recolhido_real2023",
    "icms_restituido": "icms_restituido_real2023",
    "icms_devido": "icms_devido_real2023",
}
for col_nom, col_real in COLS_DEFLATE.items():
    panel[col_real] = panel.apply(
        lambda r: r[col_nom] * defl_map.get(r["ano"], 1.0) if pd.notna(r[col_nom]) else np.nan,
        axis=1
    )

# 4.4 Deflacionar massa salarial (se disponível)
if "massa_salarial_brl" in panel.columns:
    COLS_DEFLATE["massa_salarial_brl"] = "massa_salarial_real2023"
    panel["massa_salarial_real2023"] = panel.apply(
        lambda r: r["massa_salarial_brl"] * defl_map.get(r["ano"], 1.0)
        if pd.notna(r.get("massa_salarial_brl")) else np.nan,
        axis=1
    )

# 4.5 Variáveis derivadas para K-means e Simar-Wilson
# Automação: CAPEX por empregado (proxy de intensidade tecnológica)
panel["automacao"] = panel["capex_real2023"] / panel["emprego"]
panel["automacao"] = panel["automacao"].replace([np.inf, -np.inf], np.nan)

# Capital humano: massa salarial por empregado (proxy de qualificação)
if "massa_salarial_real2023" in panel.columns:
    panel["salario_medio"] = panel["massa_salarial_real2023"] / panel["emprego"]
    panel["salario_medio"] = panel["salario_medio"].replace([np.inf, -np.inf], np.nan)

# Intensidade fiscal: incentivo por real de faturamento
panel["incentivo_faturamento"] = panel["incentivo_fiscal_real2023"] / panel["faturamento_real2023"]
panel["incentivo_faturamento"] = panel["incentivo_faturamento"].replace([np.inf, -np.inf], np.nan)

# Incentivo por empregado
panel["incentivo_emprego"] = panel["incentivo_fiscal_real2023"] / panel["emprego"]
panel["incentivo_emprego"] = panel["incentivo_emprego"].replace([np.inf, -np.inf], np.nan)

# Produtividade do trabalho: faturamento por empregado
panel["produtividade_trabalho"] = panel["faturamento_real2023"] / panel["emprego"]
panel["produtividade_trabalho"] = panel["produtividade_trabalho"].replace([np.inf, -np.inf], np.nan)

# Nota: capital_trabalho removido em v3. Usar 'automacao' diretamente.

# Log-transforms
panel["ln_capex"] = np.log(panel["capex_real2023"].clip(lower=1))
panel["ln_faturamento"] = np.log(panel["faturamento_real2023"].clip(lower=1))

# 4.5 PIB Manaus (deflated, contextual variable for Simar-Wilson)
panel["pib_manaus_real2023"] = panel["ano"].map(
    lambda a: pib_map.get(a, np.nan) * 1000 * defl_map.get(a, 1.0)
)


# ============================================================
# 5. FILTRAR DMUs VIÁVEIS
# ============================================================
print("\n5. FILTRANDO DMUs VIÁVEIS...")

# 5.1 Zero Estrutural (row-level): DMU-ano sem operação industrial.
#     Critério: faturamento == 0 AND emprego == 0 → DMU inativa no período.
#     Ex.: Couros e Similares em 2018 (sem atividade registrada).
#     Conforme seção metodológica TCC1: "positividade para DEA: I > 0, Fat > 0, E > 0".
struct_zero_mask = (
    (panel["faturamento_real2023"].fillna(0) == 0) &
    (panel["emprego"].fillna(0) == 0)
)
n_struct_zero = struct_zero_mask.sum()
if n_struct_zero > 0:
    rows_removed = panel.loc[struct_zero_mask, ["subsetor", "ano"]]
    for _, row in rows_removed.iterrows():
        print(f"  🚫 Zero estrutural: {row['subsetor']} {row['ano']} — DMU inativa, excluída")
    panel = panel[~struct_zero_mask].copy()
    print(f"  → {n_struct_zero} obs removidas (zero estrutural). Painel agora: {len(panel)} obs")
else:
    print("  ✅ Nenhum zero estrutural detectado")

# 5.2 Diagnóstico de completude por subsetor (após remoção de zeros estruturais)
completeness = panel.groupby("subsetor").agg(
    n_anos=("ano", "count"),
    fat_nulls=("faturamento_brl", lambda x: x.isna().sum()),
    fat_zeros=("faturamento_brl", lambda x: (x == 0).sum()),
    emp_nulls=("emprego_suframa", lambda x: x.isna().sum()),
    emp_zeros=("emprego_suframa", lambda x: (x == 0).sum()),
    icms_nulls=("icms_restituido", lambda x: x.isna().sum()),
    icms_zeros=("icms_restituido", lambda x: (x == 0).sum()),
    capex_nulls=("capex_usd", lambda x: x.isna().sum()),
).sort_values("n_anos", ascending=False)

print("\nCompletude por subsetor:")
print(completeness.to_string())

# 5.3 Exclusão subsetor-nível: subsetores com dados cronicamente insuficientes
exclude = []
for sub in panel["subsetor"].unique():
    sub_data = panel[panel["subsetor"] == sub]
    n_active = len(sub_data)
    emp_issues = (sub_data["emprego"].isna() | (sub_data["emprego"] == 0)).sum()
    icms_issues = (sub_data["icms_restituido"].isna() | (sub_data["icms_restituido"] == 0)).sum()

    if n_active < 3:
        exclude.append(sub)
        print(f"  ⚠️ Excluindo {sub}: apenas {n_active} obs ativas (mínimo 3)")
    elif emp_issues >= 3:
        exclude.append(sub)
        print(f"  ⚠️ Excluindo {sub}: {emp_issues} anos sem emprego SUFRAMA")
    elif sub_data["emprego"].max() < 50:
        exclude.append(sub)
        print(f"  ⚠️ Excluindo {sub}: max emprego SUFRAMA = {sub_data['emprego'].max()}")
    elif icms_issues >= 3:
        exclude.append(sub)
        print(f"  ⚠️ Excluindo {sub}: {icms_issues} anos sem ICMS")

panel["excluido"] = panel["subsetor"].isin(exclude)
panel_clean = panel[~panel["excluido"]].copy()

# Painel desbalanceado: nem toda DMU tem 6 anos (ex.: Couros sem 2018)
obs_per_sub = panel_clean.groupby("subsetor")["ano"].count()
unbalanced = obs_per_sub[obs_per_sub < 6]
if len(unbalanced) > 0:
    print(f"\n  ⚠️ Painel DESBALANCEADO (OK — zeros estruturais removidos):")
    for sub, n in unbalanced.items():
        anos_ativos = sorted(panel_clean[panel_clean["subsetor"] == sub]["ano"].unique())
        print(f"    {sub}: {n}/6 anos ({anos_ativos})")
else:
    print("\n  ✅ Painel balanceado (todos os subsetores com 6 anos)")

print(f"\n  Painel limpo: {panel_clean.shape}")
print(f"  DMUs (subsetores) ativas: {panel_clean['subsetor'].nunique()}")
print(f"  Observações subsetor-ano: {len(panel_clean)}")
print(f"  Excluídos: {exclude}")

# 5.4 DEA variable validation — positivity check
dea_vars = ["icms_restituido_real2023", "capex_real2023", "faturamento_real2023", "emprego"]
for col in dea_vars:
    zeros = (panel_clean[col] == 0).sum()
    nans = panel_clean[col].isna().sum()
    if zeros > 0 or nans > 0:
        print(f"  ⚠️ {col}: {zeros} zeros, {nans} NaN no painel limpo")
        if col == "icms_restituido_real2023":
            panel_clean.loc[panel_clean[col] == 0, col] = 1.0
            print(f"    → zeros de incentivo substituídos por R$ 1 (evita infeasibilidade DEA)")
        else:
            # Para inputs/outputs centrais, alertar — zeros residuais são problemas reais
            print(f"    → ATENÇÃO: verificar se são zeros reais ou dados faltantes")


# ============================================================
# 6. SALVAR PAINEL
# ============================================================
print("\n6. SALVANDO PAINEL...")

outpath_full = os.path.join(PROCESSED_DIR, "painel_subsetor_ano_full.csv")
panel.to_csv(outpath_full, index=False)
print(f"  ✅ Painel completo: {outpath_full}")

outpath_clean = os.path.join(PROCESSED_DIR, "painel_subsetor_ano.csv")
panel_clean.to_csv(outpath_clean, index=False)
print(f"  ✅ Painel limpo: {outpath_clean}")


# ============================================================
# 7. RESUMO ESTATÍSTICO
# ============================================================
print("\n" + "=" * 70)
print("  RESUMO DO PAINEL FINAL")
print("=" * 70)

key_vars = [
    "faturamento_real2023", "emprego", "capex_real2023",
    "icms_restituido_real2023", "incentivo_faturamento",
    "automacao", "produtividade_trabalho",
]
if "salario_medio" in panel_clean.columns:
    key_vars.insert(5, "salario_medio")

print("\nEstatísticas descritivas (painel limpo):")
print(panel_clean[key_vars].describe().round(2).to_string())

print("\nMédias por ano:")
yearly = panel_clean.groupby("ano")[key_vars[:4]].mean()
print(yearly.round(0).to_string())

print("\nSubsetores no painel final:")
for sub in sorted(panel_clean["subsetor"].unique()):
    sub_data = panel_clean[panel_clean["subsetor"] == sub]
    n_obs = len(sub_data)
    avg_emp = sub_data["emprego"].mean()
    avg_fat = sub_data["faturamento_real2023"].mean()
    avg_icms = sub_data["icms_restituido_real2023"].mean()
    print(f"  {sub}: {n_obs} anos, ~{avg_emp:.0f} empr. (SUFRAMA), R$ {avg_fat/1e9:.2f}B fat., "
          f"R$ {avg_icms/1e6:.0f}M ICMS")

# DEA specification summary
print("\n" + "-" * 70)
print("  ESPECIFICAÇÃO DEA:")
print("  Inputs:  (1) ICMS restituído real 2023  (2) CAPEX real 2023")
print("  Outputs: (1) Faturamento real 2023      (2) Emprego SUFRAMA (média mensal)")
print("  Orientação: Output (BCC/VRS)")
print("  DMUs: {} subsetores × {} anos = {} obs".format(
    panel_clean["subsetor"].nunique(), len(ANOS), len(panel_clean)))
print("-" * 70)
