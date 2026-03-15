"""Quick audit of all pipeline outputs — run once, delete after."""
import pandas as pd
import numpy as np

print("=" * 70)
print("  AUDIT: PIPELINE v3 RESULTS")
print("=" * 70)

# 1. Panel
df = pd.read_csv("data/processed/painel_subsetor_ano.csv")
print(f"\n1. PAINEL: {len(df)} obs, {df['subsetor'].nunique()} subsetores, anos={sorted(df['ano'].unique())}")
print(f"   Colunas: {len(df.columns)}")
print(f"   Zero faturamento: {(df['faturamento_real2023'] == 0).sum()}")
print(f"   Zero emprego: {(df['emprego'] == 0).sum()}")
print(f"   NaN salario_medio: {df['salario_medio'].isna().sum()}")
print(f"   Excluidos: {df['excluido'].sum()}")

couros = df[df["subsetor"] == "Couros e Similares"]
print(f"\n   Couros e Similares: {len(couros)} obs, anos={sorted(couros['ano'].tolist())}")
print(couros[["subsetor", "ano", "faturamento_real2023", "emprego", "salario_medio", "automacao", "excluido"]].to_string(index=False))

# 2. DEA
dea = pd.read_csv("data/processed/dea_scores.csv")
print(f"\n2. DEA SCORES: {len(dea)} obs")
print(f"   Global: mean VRS={dea['eff_vrs'].mean():.3f}, median={dea['eff_vrs'].median():.3f}")
print(f"   Frontier (θ>=0.999): {(dea['eff_vrs'] >= 0.999).sum()} of {len(dea)}")
for yr in sorted(dea["ano"].unique()):
    eff = dea[(dea["ano"] == yr) & (dea["eff_vrs"] >= 0.999)]
    print(f"   {yr}: {len(eff)} efficient — {eff['subsetor'].tolist()}")

# 3. Malmquist
malm = pd.read_csv("data/processed/malmquist_results.csv")
print(f"\n3. MALMQUIST: {len(malm)} obs (transitions)")
valid = malm.dropna(subset=["M"])
print(f"   Valid transitions: {len(valid)}")
print(f"   Global M (geomean): {np.exp(np.log(valid['M']).mean()):.3f}")
print(f"   Global EC: {np.exp(np.log(valid['EC']).mean()):.3f}")
print(f"   Global TC: {np.exp(np.log(valid['TC']).mean()):.3f}")

# 4. K-means
clusters = pd.read_csv("data/processed/subsetor_cluster_map.csv")
print(f"\n4. K-MEANS: {len(clusters)} subsetores mapped")
for c in sorted(clusters["cluster"].unique()):
    members = clusters[clusters["cluster"] == c]["subsetor"].tolist()
    print(f"   C{c}: {len(members)} — {members}")

# 5. Simar-Wilson
sw = pd.read_csv("outputs/tables/tab_simar_wilson.csv")
print(f"\n5. SIMAR-WILSON:")
for _, row in sw.iterrows():
    sig = "***" if row.get("Significativo", "") == "*" else "   "
    print(f"   {sig} {row['Variável']:20s}: β={row['Coeficiente']:+.4f}  IC=[{row['IC 2.5%']:.4f}, {row['IC 97.5%']:.4f}]")

print("\n" + "=" * 70)
print("  AUDIT COMPLETE")
print("=" * 70)
