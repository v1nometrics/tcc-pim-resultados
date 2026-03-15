"""
06_build_panel.py
Monta o painel final (subsetor × ano) unificando todas as fontes:
  - SUFRAMA: faturamento, CAPEX, emprego, ICMS restituído, insumos
  - IBGE: deflator IPCA, PIB Manaus
  - RFB: total ZFM (para validação)

Calcula variáveis derivadas:
  - VA (Valor Adicionado) = Faturamento - Insumos
  - Incentivo fiscal = ICMS restituído + rateio federal
  - Automação A = CAPEX/Emprego
  - Todas deflacionadas para R$ constantes de 2023

Salva em data/processed/painel_subsetor_ano.csv
"""

import pandas as pd
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
INTERIM_DIR = os.path.join(BASE_DIR, "data", "interim")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
os.makedirs(INTERIM_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

ANOS = [2018, 2019, 2020, 2021, 2022, 2023]

print("=" * 70)
print("  CONSTRUÇÃO DO PAINEL — TCC ZFM")
print("=" * 70)

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
pib_map = dict(zip(df_pib["ano"], df_pib["pib_manaus_mil_reais"]))
print(f"  PIB Manaus: {pib_map}")

# Faturamento
df_fat = pd.read_csv(os.path.join(RAW_DIR, "suframa_faturamento_subsetor.csv"))
print(f"  Faturamento: {len(df_fat)} linhas, {df_fat['subsetor'].nunique()} subsetores")

# CAPEX (em US$)
df_capex = pd.read_csv(os.path.join(RAW_DIR, "suframa_capex_subsetor.csv"))
print(f"  CAPEX: {len(df_capex)} linhas, {df_capex['subsetor'].nunique()} subsetores")

# Emprego
df_emp = pd.read_csv(os.path.join(RAW_DIR, "suframa_emprego_subsetor.csv"))
print(f"  Emprego: {len(df_emp)} linhas, {df_emp['subsetor'].nunique()} subsetores")

# ICMS
df_icms = pd.read_csv(os.path.join(RAW_DIR, "suframa_icms_subsetor.csv"))
print(f"  ICMS: {len(df_icms)} linhas, {df_icms['subsetor'].nunique()} subsetores")

# Insumos (only 11 subsetores)
df_insumos = pd.read_csv(os.path.join(RAW_DIR, "suframa_insumos_subsetor.csv"))
# Fix: extraction parsed both R$ and US$ tables → duplicates for 2018-2019.
# Keep first (R$) value per (subsetor, ano).
df_insumos = df_insumos.drop_duplicates(subset=["subsetor", "ano"], keep="first")
print(f"  Insumos: {len(df_insumos)} linhas, {df_insumos['subsetor'].nunique()} subsetores")


# ============================================================
# 2. HARMONIZAR SUBSETORES
# ============================================================
print("\n2. HARMONIZANDO SUBSETORES...")

# Check which subsetores appear in each dataset
all_subsetors = set()
for name, df in [("fat", df_fat), ("capex", df_capex), ("emp", df_emp), ("icms", df_icms)]:
    subs = set(df["subsetor"].unique()) - {"TOTAL"}
    all_subsetors.update(subs)
    print(f"  {name}: {sorted(subs)}")

print(f"\n  Todos os subsetores ({len(all_subsetors)}): {sorted(all_subsetors)}")

# Note: Faturamento has "Bens de Informática" as separate from Eletroeletrônico
# But CAPEX and Emprego have Eletroeletrônico inclusive
# Decision: merge "Bens de Informática" into "Eletroeletrônico" in faturamento
# to be consistent with investment and employment data.

# Also: some datasets have "Couros e Similares" with 0 workers in 2018
# Keep it but flag

# Handle Bens de Informática — merge into Eletroeletrônico
print("\n  Merging 'Bens de Informática' into 'Eletroeletrônico' no faturamento...")
mask_bi = df_fat["subsetor"] == "Bens de Informática"
mask_ee = df_fat["subsetor"] == "Eletroeletrônico"

if mask_bi.any():
    # For each year, sum faturamento of both
    bi_data = df_fat[mask_bi].set_index("ano")["faturamento_brl"]
    for idx in df_fat[mask_ee].index:
        ano = df_fat.loc[idx, "ano"]
        if ano in bi_data.index:
            df_fat.loc[idx, "faturamento_brl"] += bi_data[ano]
    
    # Remove Bens de Informática rows
    df_fat = df_fat[~mask_bi].copy()
    print(f"  Faturamento após merge: {df_fat['subsetor'].nunique()} subsetores")

# Similarly merge in insumos if present
if "Bens de Informática" in df_insumos["subsetor"].values:
    mask_bi = df_insumos["subsetor"] == "Bens de Informática"
    mask_ee = df_insumos["subsetor"] == "Eletroeletrônico"
    bi_data = df_insumos[mask_bi].set_index("ano")["insumos_brl"]
    for idx in df_insumos[mask_ee].index:
        ano = df_insumos.loc[idx, "ano"]
        if ano in bi_data.index:
            df_insumos.loc[idx, "insumos_brl"] += bi_data[ano]
    df_insumos = df_insumos[~mask_bi].copy()


# ============================================================
# 3. CONSTRUIR PAINEL BASE
# ============================================================
print("\n3. CONSTRUINDO PAINEL BASE...")

# Remove TOTAL rows from all datasets
df_fat = df_fat[df_fat["subsetor"] != "TOTAL"].copy()
df_capex = df_capex[df_capex["subsetor"] != "TOTAL"].copy()
df_emp = df_emp[df_emp["subsetor"] != "TOTAL"].copy()
df_icms = df_icms[df_icms["subsetor"] != "TOTAL"].copy()
df_insumos = df_insumos[df_insumos["subsetor"] != "TOTAL"].copy()

# Start with faturamento as base (most complete)
panel = df_fat[["subsetor", "ano", "faturamento_brl"]].copy()

# Merge CAPEX
panel = panel.merge(
    df_capex[["subsetor", "ano", "capex_usd"]], 
    on=["subsetor", "ano"], how="left"
)

# Merge emprego
panel = panel.merge(
    df_emp[["subsetor", "ano", "emprego_suframa"]], 
    on=["subsetor", "ano"], how="left"
)

# Merge ICMS (use icms_restituido as proxy for fiscal incentive)
panel = panel.merge(
    df_icms[["subsetor", "ano", "icms_recolhido", "icms_restituido", "icms_devido"]], 
    on=["subsetor", "ano"], how="left"
)

# Merge insumos
panel = panel.merge(
    df_insumos[["subsetor", "ano", "insumos_brl"]], 
    on=["subsetor", "ano"], how="left"
)

print(f"  Painel bruto: {panel.shape}")
print(f"  Subsetores: {panel['subsetor'].nunique()}")
print(f"  Obs por ano: {panel.groupby('ano').size().to_dict()}")

# ============================================================
# 4. CALCULAR VARIÁVEIS DERIVADAS
# ============================================================
print("\n4. CALCULANDO VARIÁVEIS DERIVADAS...")

# 4.1 Valor Adicionado (VA)
# VA = Faturamento - Insumos
# Para subsetores sem dados de insumos individuais, estimar via ratio agregado
# Ratio médio: insumos_total / faturamento_total (do PIM agregado)
insumo_fat_ratio = {
    2018: 50_493_153_316 / 94_211_163_641,  # 0.536
    2019: 53_255_909_337 / 104_787_183_840,  # 0.508
    2020: 65_972_892_060 / 120_318_479_886,  # 0.548
    2021: 95_849_267_392 / 159_779_061_668,  # 0.600
    2022: 103_360_525_949 / 177_929_010_474,  # 0.581
    2023: 86_894_139_187 / 173_470_415_218,  # 0.501
}
print(f"  Ratios insumo/faturamento (agregado PIM): {insumo_fat_ratio}")

# Where insumos is missing, estimate using average ratio
panel["insumos_estimado"] = panel.apply(
    lambda r: r["insumos_brl"] if pd.notna(r["insumos_brl"]) 
    else r["faturamento_brl"] * insumo_fat_ratio.get(r["ano"], 0.55),
    axis=1
)
panel["insumos_source"] = panel["insumos_brl"].apply(
    lambda x: "SUFRAMA" if pd.notna(x) else "estimado"
)
panel["va_brl"] = panel["faturamento_brl"] - panel["insumos_estimado"]

# 4.2 Convert CAPEX from USD to BRL using annual average exchange rates
# Average BRL/USD rates:
fx_rates = {
    2018: 3.655,
    2019: 3.946,
    2020: 5.196,
    2021: 5.395,
    2022: 5.165,
    2023: 4.994,
}
panel["capex_brl"] = panel.apply(
    lambda r: r["capex_usd"] * fx_rates.get(r["ano"], 5.0), axis=1
)

# 4.3 Incentivo fiscal = ICMS restituído (principal proxy por subsetor)
panel["incentivo_fiscal_brl"] = panel["icms_restituido"].fillna(0)

# 4.4 Deflacionar para R$ constantes de 2023
for col in ["faturamento_brl", "va_brl", "capex_brl", "incentivo_fiscal_brl", 
            "icms_recolhido", "icms_restituido", "icms_devido", "insumos_estimado"]:
    col_real = col.replace("_brl", "_real2023").replace("_brl", "_real2023")
    if "_brl" in col:
        col_real = col.replace("_brl", "_real2023")
    else:
        col_real = col + "_real2023"
    panel[col_real] = panel.apply(
        lambda r: r[col] * defl_map.get(r["ano"], 1.0) if pd.notna(r[col]) else np.nan,
        axis=1
    )

# 4.5 CAPEX real (already converted to BRL, now deflate)
# Already done above

# 4.6 Automação: A = CAPEX_real / Emprego
panel["automacao"] = panel["capex_real2023"] / panel["emprego_suframa"]
panel["automacao"] = panel["automacao"].replace([np.inf, -np.inf], np.nan)

# 4.7 Intensidades
panel["incentivo_va"] = panel["incentivo_fiscal_real2023"] / panel["va_real2023"]
panel["incentivo_va"] = panel["incentivo_va"].replace([np.inf, -np.inf], np.nan)

panel["incentivo_emprego"] = panel["incentivo_fiscal_real2023"] / panel["emprego_suframa"]
panel["incentivo_emprego"] = panel["incentivo_emprego"].replace([np.inf, -np.inf], np.nan)

panel["porte_ln_capex"] = np.log(panel["capex_real2023"].clip(lower=1))

# 4.8 Add PIB Manaus (deflated)
panel["pib_manaus_real2023"] = panel["ano"].map(
    lambda a: pib_map.get(a, np.nan) * 1000 * defl_map.get(a, 1.0)  # Convert from mil to R$
)

# ============================================================
# 5. FILTRAR DMUs VIÁVEIS
# ============================================================
print("\n5. FILTRANDO DMUs VIÁVEIS...")

# Check completeness
completeness = panel.groupby("subsetor").agg(
    n_anos=("ano", "count"),
    fat_nulls=("faturamento_brl", lambda x: x.isna().sum()),
    emp_nulls=("emprego_suframa", lambda x: x.isna().sum()),
    emp_zeros=("emprego_suframa", lambda x: (x == 0).sum()),
    icms_nulls=("icms_restituido", lambda x: x.isna().sum()),
    icms_zeros=("icms_restituido", lambda x: (x == 0).sum()),
    capex_nulls=("capex_usd", lambda x: x.isna().sum()),
).sort_values("n_anos", ascending=False)

print("\nCompletude por subsetor:")
print(completeness.to_string())

# Flag subsetores to exclude (0 or missing employment in multiple years)
# Criteria: exclude if ≥3 years with 0 employment or missing critical vars
exclude = []
for sub in panel["subsetor"].unique():
    sub_data = panel[panel["subsetor"] == sub]
    emp_issues = (sub_data["emprego_suframa"].isna() | (sub_data["emprego_suframa"] == 0)).sum()
    if emp_issues >= 3:
        exclude.append(sub)
        print(f"  ⚠️ Excluindo {sub}: {emp_issues} anos sem emprego")

# Also flag very small subsetores (< 50 empregados em todos os anos)
for sub in panel["subsetor"].unique():
    if sub in exclude:
        continue
    sub_data = panel[panel["subsetor"] == sub]
    if sub_data["emprego_suframa"].max() < 50:
        exclude.append(sub)
        print(f"  ⚠️ Excluindo {sub}: max emprego = {sub_data['emprego_suframa'].max()}")

panel["excluido"] = panel["subsetor"].isin(exclude)
panel_clean = panel[~panel["excluido"]].copy()

print(f"\n  Painel limpo: {panel_clean.shape}")
print(f"  DMUs (subsetores) ativas: {panel_clean['subsetor'].nunique()}")
print(f"  Observações subsetor-ano: {len(panel_clean)}")
print(f"  Excluídos: {exclude}")


# ============================================================
# 6. SALVAR PAINEL
# ============================================================
print("\n6. SALVANDO PAINEL...")

# Full panel (including excluded)
outpath_full = os.path.join(PROCESSED_DIR, "painel_subsetor_ano_full.csv")
panel.to_csv(outpath_full, index=False)
print(f"  ✅ Painel completo: {outpath_full}")

# Clean panel (for modeling)
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
    "faturamento_real2023", "va_real2023", "emprego_suframa",
    "capex_real2023", "incentivo_fiscal_real2023", "automacao",
    "incentivo_va", "incentivo_emprego", "porte_ln_capex"
]

print("\nEstatísticas descritivas (painel limpo):")
print(panel_clean[key_vars].describe().round(2).to_string())

print("\nMédias por ano:")
yearly = panel_clean.groupby("ano")[key_vars[:5]].mean()
print(yearly.round(0).to_string())

print("\nSubsetores no painel final:")
for sub in sorted(panel_clean["subsetor"].unique()):
    n_obs = len(panel_clean[panel_clean["subsetor"] == sub])
    avg_emp = panel_clean[panel_clean["subsetor"] == sub]["emprego_suframa"].mean()
    avg_fat = panel_clean[panel_clean["subsetor"] == sub]["faturamento_real2023"].mean()
    print(f"  {sub}: {n_obs} anos, ~{avg_emp:.0f} empregados, R$ {avg_fat/1e9:.2f}B fat. médio")
