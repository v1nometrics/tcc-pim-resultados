"""
_audit_data.py — Auditoria completa dos dados extraídos
"""
import pandas as pd
import numpy as np
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, "data", "raw")
PROC = os.path.join(BASE, "data", "processed")

print("=" * 80)
print("  AUDITORIA COMPLETA DOS DADOS — TCC ZFM")
print("=" * 80)

# ============================================================
# 1. CSVs BRUTOS
# ============================================================
datasets = {
    "faturamento": ("suframa_faturamento_subsetor.csv", "faturamento_brl"),
    "capex": ("suframa_capex_subsetor.csv", "capex_usd"),
    "emprego": ("suframa_emprego_subsetor.csv", "emprego_suframa"),
    "icms": ("suframa_icms_subsetor.csv", "icms_restituido"),
    "insumos": ("suframa_insumos_subsetor.csv", "insumos_brl"),
}

for name, (fname, valcol) in datasets.items():
    df = pd.read_csv(os.path.join(RAW, fname))
    subs = sorted(df[df["subsetor"] != "TOTAL"]["subsetor"].unique())
    print(f"\n{'='*60}")
    print(f"  {name.upper()}: {len(df)} linhas, {len(subs)} subsetores (excl. TOTAL)")
    print(f"  Subsetores: {subs}")
    print(f"  Anos: {sorted(df['ano'].unique())}")

    # Pivot
    noT = df[df["subsetor"] != "TOTAL"]
    try:
        pv = noT.pivot_table(index="subsetor", columns="ano", values=valcol, aggfunc="first")
        print(pv.to_string())
    except Exception as e:
        print(f"  Pivot error: {e}")

    # TOTAIS
    totais = df[df["subsetor"] == "TOTAL"]
    if not totais.empty:
        print(f"\n  TOTAIS:")
        print(totais.to_string(index=False))
    print()

# ============================================================
# 2. PAINEL PROCESSADO
# ============================================================
print("\n" + "=" * 80)
print("  PAINEL FINAL PROCESSADO")
print("=" * 80)

panel = pd.read_csv(os.path.join(PROC, "painel_subsetor_ano.csv"))
print(f"\nShape: {panel.shape}")
print(f"Subsetores: {panel['subsetor'].nunique()} -> {sorted(panel['subsetor'].unique())}")
print(f"Anos: {sorted(panel['ano'].unique())}")
print(f"Obs por ano: {panel.groupby('ano').size().to_dict()}")

# Check balanced
counts = panel.groupby("subsetor")["ano"].count()
unbalanced = counts[counts != 6]
if len(unbalanced) > 0:
    print(f"\n⚠️ DESBALANCEADO: {unbalanced.to_dict()}")
else:
    print(f"\n✅ Painel BALANCEADO: {panel['subsetor'].nunique()} × 6 = {len(panel)}")

# ============================================================
# 3. VERIFICAR PROXIES E ESTIMATIVAS
# ============================================================
print("\n" + "=" * 80)
print("  INVENTÁRIO DE PROXIES E ESTIMATIVAS")
print("=" * 80)

# 3a. Insumos: quantos são SUFRAMA vs estimados?
if "insumos_source" in panel.columns:
    src = panel.groupby("insumos_source").size()
    print(f"\n  Fonte dos insumos:")
    print(f"  {src.to_dict()}")
    
    # Quais subsetores são estimados?
    est = panel[panel["insumos_source"] == "estimado"]["subsetor"].unique()
    suf = panel[panel["insumos_source"] == "SUFRAMA"]["subsetor"].unique()
    print(f"\n  Insumos SUFRAMA direto ({len(suf)}): {sorted(suf)}")
    print(f"  Insumos ESTIMADOS ({len(est)}): {sorted(est)}")

# 3b. VA negativo?
neg_va = panel[panel["va_real2023"] < 0]
if len(neg_va) > 0:
    print(f"\n  ⚠️ VA NEGATIVO: {len(neg_va)} obs")
    print(neg_va[["subsetor", "ano", "faturamento_real2023", "insumos_estimado", "va_real2023"]].to_string())
else:
    print(f"\n  ✅ VA sempre positivo")

# 3c. Emprego zeros?
zero_emp = panel[panel["emprego_suframa"] == 0]
if len(zero_emp) > 0:
    print(f"\n  ⚠️ Emprego = 0: {len(zero_emp)} obs")
    print(zero_emp[["subsetor", "ano", "emprego_suframa"]].to_string())

# 3d. CAPEX zeros?
zero_capex = panel[panel["capex_real2023"] == 0]
if len(zero_capex) > 0:
    print(f"\n  ⚠️ CAPEX = 0: {len(zero_capex)} obs")
    print(zero_capex[["subsetor", "ano", "capex_real2023"]].to_string())

# 3e. ICMS restituído zeros?
zero_icms = panel[panel["incentivo_fiscal_real2023"] == 0]
if len(zero_icms) > 0:
    print(f"\n  ⚠️ Incentivo = 0: {len(zero_icms)} obs")
    print(zero_icms[["subsetor", "ano", "incentivo_fiscal_real2023"]].to_string())

# 3f. Automação infinita ou NaN?
bad_auto = panel[~np.isfinite(panel["automacao"])]
if len(bad_auto) > 0:
    print(f"\n  ⚠️ Automação Inf/NaN: {len(bad_auto)} obs")

# ============================================================
# 4. COMPARAÇÃO: "Bens de Informática" merge
# ============================================================
print("\n" + "=" * 80)
print("  VERIFICAÇÃO: MERGE BENS DE INFORMÁTICA → ELETROELETRÔNICO")
print("=" * 80)

df_fat_raw = pd.read_csv(os.path.join(RAW, "suframa_faturamento_subsetor.csv"))
bi = df_fat_raw[df_fat_raw["subsetor"] == "Bens de Informática"]
ee = df_fat_raw[df_fat_raw["subsetor"] == "Eletroeletrônico"]
print(f"Bens de Info no CSV bruto: {len(bi)} registros")
print(f"Eletroeletrônico no CSV bruto: {len(ee)} registros")
if not bi.empty:
    print("\nBens de Informática:")
    print(bi.to_string(index=False))
    print("\nEletroeletrônico (antes do merge):")
    print(ee.to_string(index=False))

# No painel final
ee_panel = panel[panel["subsetor"] == "Eletroeletrônico"]
print(f"\nEletroeletrônico no painel final (pos-merge):")
print(ee_panel[["ano", "faturamento_real2023"]].to_string(index=False))

# ============================================================
# 5. VERIFICAR SUBSETORES EXCLUÍDOS
# ============================================================
print("\n" + "=" * 80)
print("  SUBSETORES AUSENTES DO PAINEL FINAL")
print("=" * 80)

# Subsetores no CAPEX mas não no painel
capex_subs = set(pd.read_csv(os.path.join(RAW, "suframa_capex_subsetor.csv"))["subsetor"].unique()) - {"TOTAL"}
emp_subs = set(pd.read_csv(os.path.join(RAW, "suframa_emprego_subsetor.csv"))["subsetor"].unique()) - {"TOTAL"}
fat_subs = set(pd.read_csv(os.path.join(RAW, "suframa_faturamento_subsetor.csv"))["subsetor"].unique()) - {"TOTAL"}
icms_subs = set(pd.read_csv(os.path.join(RAW, "suframa_icms_subsetor.csv"))["subsetor"].unique()) - {"TOTAL"}
panel_subs = set(panel["subsetor"].unique())

print(f"CAPEX: {len(capex_subs)} sub -> {sorted(capex_subs - panel_subs)} ausentes do painel")
print(f"Emprego: {len(emp_subs)} sub -> {sorted(emp_subs - panel_subs)} ausentes do painel")
print(f"Faturamento: {len(fat_subs)} sub -> {sorted(fat_subs - panel_subs)} ausentes do painel")
print(f"ICMS: {len(icms_subs)} sub -> {sorted(icms_subs - panel_subs)} ausentes do painel")

# ============================================================
# 6. TAXAS DE CÂMBIO (PTAX)
# ============================================================
print("\n" + "=" * 80)
print("  TAXAS DE CÂMBIO USADAS (BRL/USD)")
print("=" * 80)
fx_rates = {2018: 3.655, 2019: 3.946, 2020: 5.196, 2021: 5.395, 2022: 5.165, 2023: 4.994}
print(f"  Hardcoded: {fx_rates}")
print("  NOTA: Verificar contra PTAX médio anual do BCB")

# ============================================================
# 7. DEFLATOR
# ============================================================
print("\n" + "=" * 80)
print("  DEFLATOR IPCA (base 2023)")
print("=" * 80)
defl = pd.read_csv(os.path.join(RAW, "deflator_anual_2023.csv"))
print(defl.to_string(index=False))

# ============================================================
# 8. RAZÕES INSUMO/FATURAMENTO
# ============================================================
print("\n" + "=" * 80)
print("  RAZÕES INSUMO/FATURAMENTO USADAS PARA ESTIMAÇÃO")
print("=" * 80)
insumo_fat_ratio = {
    2018: 50_493_153_316 / 94_211_163_641,
    2019: 53_255_909_337 / 104_787_183_840,
    2020: 65_972_892_060 / 120_318_479_886,
    2021: 95_849_267_392 / 159_779_061_668,
    2022: 103_360_525_949 / 177_929_010_474,
    2023: 86_894_139_187 / 173_470_415_218,
}
for year, ratio in insumo_fat_ratio.items():
    print(f"  {year}: {ratio:.4f} ({ratio:.1%})")
print("  NOTA: Estes são os totais agregados PIM. Verificar contra o PDF original.")

print("\n" + "=" * 80)
print("  FIM DA AUDITORIA")
print("=" * 80)
