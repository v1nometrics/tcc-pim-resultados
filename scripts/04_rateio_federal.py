"""
04_rateio_federal.py
Rateio proporcional dos gastos tributários federais (DGT/RFB) por subsetor PIM.

ATENÇÃO METODOLÓGICA:
  Este rateio é utilizado APENAS para fins DESCRITIVOS — estimar o custo fiscal
  total (federal + estadual) da ZFM por subsetor. Ele NÃO entra como variável
  nos modelos DEA ou K-means porque:
    1. Se rateio ∝ faturamento → I_fed/Fat = constante ∀ s → zero discriminação no DEA
    2. Se rateio ∝ ICMS → I_total = c_t × ICMS → collinear após Z-score → redundante
  (Cooper, Seiford & Tone, 2007: inputs/outputs must show genuine cross-sectional variation)

Fontes:
  - data/raw/rfb_zfm_all_rows.csv (extraído do DGT Bases efetivas 2020, Q XXVI)
  - data/raw/suframa_faturamento_subsetor.csv (peso de rateio)
  - data/raw/suframa_icms_subsetor.csv (incentivo estadual observado)

Outputs:
  - data/interim/rateio_federal_descritivo.csv  (rateio por subsetor × ano)
  - outputs/tables/tab_custo_fiscal_total.csv    (tabela descritiva para o TCC)

Referência jurídica: Art. 198 CTN — sigilo fiscal impede acesso a dados por contribuinte.
Referência metodológica: Rateio proporcional como proxy de alocação é prática padrão em
  finanças públicas quando microdados são indisponíveis (Musgrave & Musgrave, 2004).
"""

import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
INTERIM_DIR = os.path.join(BASE_DIR, "data", "interim")
TABLE_DIR = os.path.join(BASE_DIR, "outputs", "tables")
os.makedirs(INTERIM_DIR, exist_ok=True)
os.makedirs(TABLE_DIR, exist_ok=True)

ANOS = [2018, 2019, 2020, 2021, 2022, 2023]

print("=" * 70)
print("  RATEIO FEDERAL DESCRITIVO — TCC ZFM")
print("=" * 70)

# ============================================================
# 1. CARREGAR TOTAIS FEDERAIS (DGT Q XXVI)
# ============================================================
print("\n1. CARREGANDO TOTAIS FEDERAIS (DGT Q XXVI)...")

df_rfb = pd.read_csv(os.path.join(RAW_DIR, "rfb_zfm_all_rows.csv"))
q26 = df_rfb[df_rfb["aba"] == "Q XXVI"].copy()

# Identify tributos by Excel line number in Q XXVI:
# L24  → II (Imposto de Importação)       — 6 values (col_idx 0-5 = 2018-2023)
# L130 → IPI (Imposto sobre Produtos Ind.) — 6 values
# L150 → IRPJ                             — 6 values
# PIS/COFINS: sum of subcategories (Alíquotas Diferenciadas + Aquisição de Mercadorias)
#   L216 + L217 (short series) or L301 + L302 (also short)
# For PIS/COFINS we use the larger "Alíquotas Diferenciadas" series that has 6 values:
#   L301 has 6 values for PIS/COFINS-Alíq.Dif.

TRIBUTO_LINES = {
    "II": 24,        # Imposto de Importação
    "IPI": 130,      # Imposto sobre Produtos Industrializados
    "IRPJ": 150,     # Imposto de Renda PJ
}

# Build tributo totals
tributo_totals = {}
for tributo, linha in TRIBUTO_LINES.items():
    data = q26[q26["linha"] == linha].sort_values("col_idx")
    if len(data) >= 6:
        values = data["valor"].values[:6]
        tributo_totals[tributo] = dict(zip(ANOS, values))
        print(f"  {tributo} (L{linha}): {[f'R${v/1e9:.1f}B' for v in values]}")
    else:
        print(f"  ⚠️ {tributo} (L{linha}): apenas {len(data)} valores")

# PIS/COFINS — Alíquotas Diferenciadas (L301, 6 values) + Aquisição de Mercadorias (L302, 2 values)
# We use L216 (6 values) + L217 (2 values, fill rest with 0) for conservative estimate
# Or use L301 (6 values) which seems to be the larger consolidated series
pis_aliq = q26[q26["linha"] == 301].sort_values("col_idx")
pis_aquis = q26[q26["linha"] == 302].sort_values("col_idx")

# L301 has 6 values
if len(pis_aliq) >= 6:
    pis_values = pis_aliq["valor"].values[:6]
    # L302 has only 2 values — fill missing years with 0
    aquis_map = {}
    for _, row in pis_aquis.iterrows():
        aquis_map[int(row["col_idx"])] = row["valor"]
    
    pis_cofins_total = {}
    for i, ano in enumerate(ANOS):
        pis_cofins_total[ano] = pis_values[i] + aquis_map.get(i, 0)
    
    tributo_totals["PIS_COFINS"] = pis_cofins_total
    print(f"  PIS/COFINS: {[f'R${v/1e9:.1f}B' for v in pis_cofins_total.values()]}")
else:
    # Fallback: use L216 (smaller Alíquotas Diferenciadas series)
    pis_aliq_small = q26[q26["linha"] == 216].sort_values("col_idx")
    if len(pis_aliq_small) >= 6:
        tributo_totals["PIS_COFINS"] = dict(zip(ANOS, pis_aliq_small["valor"].values[:6]))
        print(f"  PIS/COFINS (fallback L216): {[f'R${v/1e9:.1f}B' for v in pis_aliq_small['valor'].values[:6]]}")
    else:
        print("  ⚠️ PIS/COFINS: dados insuficientes")

# Total federal por ano
print("\n  TOTAL FEDERAL POR ANO:")
total_federal = {}
for ano in ANOS:
    total = sum(tributo_totals[t].get(ano, 0) for t in tributo_totals)
    total_federal[ano] = total
    breakdown = " + ".join(f"{t}={tributo_totals[t].get(ano,0)/1e9:.1f}B" for t in tributo_totals)
    print(f"  {ano}: R$ {total/1e9:.1f}B ({breakdown})")


# ============================================================
# 2. CARREGAR PESOS DE RATEIO (FATURAMENTO POR SUBSETOR)
# ============================================================
print("\n2. CARREGANDO PESOS DE RATEIO (faturamento)...")

df_fat = pd.read_csv(os.path.join(RAW_DIR, "suframa_faturamento_subsetor.csv"))
df_fat = df_fat[df_fat["subsetor"] != "TOTAL"].copy()

# Merge Bens de Informática → Eletroeletrônico (consistência com painel)
if "Bens de Informática" in df_fat["subsetor"].values:
    mask_bi = df_fat["subsetor"] == "Bens de Informática"
    mask_ee = df_fat["subsetor"] == "Eletroeletrônico"
    bi_data = df_fat[mask_bi].set_index("ano")["faturamento_brl"]
    for idx in df_fat[mask_ee].index:
        ano = df_fat.loc[idx, "ano"]
        if ano in bi_data.index:
            df_fat.loc[idx, "faturamento_brl"] += bi_data[ano]
    df_fat = df_fat[~mask_bi].copy()

# Compute faturamento share per subsetor-year
fat_total_by_year = df_fat.groupby("ano")["faturamento_brl"].sum().to_dict()
df_fat["fat_share"] = df_fat.apply(
    lambda r: r["faturamento_brl"] / fat_total_by_year.get(r["ano"], 1), axis=1
)
print(f"  Subsetores: {df_fat['subsetor'].nunique()}")
print(f"  Share total por ano (verificação = 1.0): {df_fat.groupby('ano')['fat_share'].sum().to_dict()}")


# ============================================================
# 3. APLICAR RATEIO
# ============================================================
print("\n3. APLICANDO RATEIO PROPORCIONAL...")
print("  Fórmula: I_fed(s,t) = I_fed_total(t) × [Fat(s,t) / ΣFat(t)]")

rows = []
for _, r in df_fat.iterrows():
    sub = r["subsetor"]
    ano = int(r["ano"])
    share = r["fat_share"]
    
    row = {"subsetor": sub, "ano": ano, "fat_share": share}
    
    for tributo in tributo_totals:
        total_t = tributo_totals[tributo].get(ano, 0)
        row[f"{tributo.lower()}_rateado"] = total_t * share
    
    row["federal_total_rateado"] = total_federal.get(ano, 0) * share
    rows.append(row)

df_rateio = pd.DataFrame(rows)

# ============================================================
# 4. ADICIONAR ICMS REAL (incentivo estadual observado)
# ============================================================
print("\n4. ADICIONANDO ICMS REAL...")

df_icms = pd.read_csv(os.path.join(RAW_DIR, "suframa_icms_subsetor.csv"))
df_icms = df_icms[df_icms["subsetor"] != "TOTAL"].copy()

df_rateio = df_rateio.merge(
    df_icms[["subsetor", "ano", "icms_restituido"]],
    on=["subsetor", "ano"], how="left"
)

df_rateio["incentivo_total_estimado"] = (
    df_rateio["federal_total_rateado"].fillna(0) + 
    df_rateio["icms_restituido"].fillna(0)
)

# ============================================================
# 5. SALVAR
# ============================================================
print("\n5. SALVANDO...")

outpath = os.path.join(INTERIM_DIR, "rateio_federal_descritivo.csv")
df_rateio.to_csv(outpath, index=False)
print(f"  ✅ {outpath} ({len(df_rateio)} linhas)")

# ============================================================
# 6. TABELA DESCRITIVA PARA O TCC
# ============================================================
print("\n6. TABELA DESCRITIVA: CUSTO FISCAL TOTAL ESTIMADO DA ZFM...")

# Aggregate by year
yearly = df_rateio.groupby("ano").agg(
    ii_total=("ii_rateado", "sum"),
    ipi_total=("ipi_rateado", "sum"),
    irpj_total=("irpj_rateado", "sum"),
    pis_cofins_total=("pis_cofins_rateado", "sum"),
    federal_total=("federal_total_rateado", "sum"),
    icms_total=("icms_restituido", "sum"),
    incentivo_total=("incentivo_total_estimado", "sum"),
).round(0)

yearly["pct_federal"] = (yearly["federal_total"] / yearly["incentivo_total"] * 100).round(1)

print("\n  CUSTO FISCAL TOTAL ESTIMADO DA ZFM (R$ bilhões):")
print("-" * 80)
for ano in ANOS:
    r = yearly.loc[ano]
    print(f"  {ano}: Federal R${r['federal_total']/1e9:.1f}B + ICMS R${r['icms_total']/1e9:.1f}B"
          f" = Total R${r['incentivo_total']/1e9:.1f}B (federal = {r['pct_federal']:.0f}%)")

yearly.to_csv(os.path.join(TABLE_DIR, "tab_custo_fiscal_total.csv"))
print(f"\n  ✅ tab_custo_fiscal_total.csv")

# Top 5 subsetores by total incentive (average across years)
top5 = df_rateio.groupby("subsetor")["incentivo_total_estimado"].mean().nlargest(5)
print(f"\n  Top 5 subsetores por incentivo total estimado (média anual):")
for sub, val in top5.items():
    print(f"    {sub}: R$ {val/1e9:.2f}B")

print("\n" + "=" * 70)
print("  NOTA: Este rateio é DESCRITIVO. No modelo DEA, usa-se apenas o ICMS")
print("  restituído (dado observado por subsetor) como proxy de incentivo fiscal.")
print("  O total federal entra como contexto no texto do TCC, não nos modelos.")
print("=" * 70)
