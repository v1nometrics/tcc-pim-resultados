"""Collect all v3 results for DOCUMENTO_MESTRE rewrite."""
import pandas as pd
import numpy as np
from scipy.stats import gmean

# Panel
df = pd.read_csv('data/processed/painel_com_cluster.csv')
print('=== PANEL ===')
print(f'Rows: {len(df)}, Cols: {len(df.columns)}')
print(f'Subsetores: {df.subsetor.nunique()}')
print(f'Anos: {sorted(df.ano.unique())}')

# Concentration
total_fat = df.groupby('subsetor')['faturamento_real2023'].sum()
pct = (total_fat / total_fat.sum() * 100).sort_values(ascending=False)
print('\n=== CONCENTRATION ===')
print(f'Top 1 (Eletroeletrônico): {pct.iloc[0]:.1f}%')
print(f'Top 6: {pct.iloc[:6].sum():.1f}%')
for s, v in pct.iloc[:6].items():
    print(f'  {s}: {v:.1f}%')

# Emprego concentration
total_emp = df.groupby('subsetor')['emprego'].sum()
pct_emp = (total_emp / total_emp.sum() * 100).sort_values(ascending=False)
print(f'\nEmprego Top 1: {pct_emp.iloc[0]:.1f}% ({pct_emp.index[0]})')

# DEA
dea = pd.read_csv('data/processed/dea_scores.csv')
print('\n=== DEA GLOBAL ===')
print(f'N obs DEA: {len(dea)}')
print(f'VRS: mean={dea.eff_vrs.mean():.3f}, median={dea.eff_vrs.median():.3f}, std={dea.eff_vrs.std():.3f}')
print(f'CRS: mean={dea.eff_crs.mean():.3f}')
print(f'Scale: mean={dea.scale_eff.mean():.3f}')
frontier = (dea.eff_vrs >= 0.9999).sum()
print(f'Frontier (VRS=1): {frontier}/{len(dea)} ({frontier/len(dea)*100:.0f}%)')
print('Frontier per year:')
for yr in sorted(dea.ano.unique()):
    n = (dea[dea.ano==yr].eff_vrs >= 0.9999).sum()
    total = len(dea[dea.ano==yr])
    print(f'  {yr}: {n}/{total}')

# TGR by cluster
print('\n=== TGR BY CLUSTER ===')
for c in sorted(dea.cluster.unique()):
    t = dea[dea.cluster==c].tgr.mean()
    n = len(dea[dea.cluster==c])
    print(f'  C{c}: TGR={t:.3f} (n={n})')

# VRS by cluster
print('\n=== VRS BY CLUSTER ===')
for c in sorted(dea.cluster.unique()):
    v = dea[dea.cluster==c].eff_vrs.mean()
    print(f'  C{c}: VRS_mean={v:.3f}')

# Malmquist
malm = pd.read_csv('data/processed/malmquist_results.csv')
valid = malm.dropna(subset=['M'])
print(f'\n=== MALMQUIST ===')
print(f'Valid transitions: {len(valid)}/{len(malm)}')
for col in ['EC', 'TC', 'M']:
    vals = valid[col].dropna()
    vals = vals[vals > 0]
    print(f'{col}: gmean={gmean(vals):.3f}, n={len(vals)}')

print('\nBy period:')
for p in sorted(valid.periodo.unique()):
    sub = valid[valid.periodo == p]
    ec_v = sub.EC.dropna()
    tc_v = sub.TC.dropna()
    m_v = sub.M.dropna()
    ec_v = ec_v[ec_v > 0]
    tc_v = tc_v[tc_v > 0]
    m_v = m_v[m_v > 0]
    print(f'  {p}: M={gmean(m_v):.3f}, EC={gmean(ec_v):.3f}, TC={gmean(tc_v):.3f}, n={len(sub)}')

# K-means validation
print('\n=== KMEANS VALIDATION ===')
val = pd.read_csv('outputs/tables/tab_elbow_silhouette.csv')
print(val.to_string(index=False))

# SW extended model
print('\n=== SW EXTENDED MODEL ===')
# Read from script output if available
try:
    import glob
    # Check for extended model results in the tables
    ext_files = glob.glob('outputs/tables/*extended*')
    print(f'Extended files: {ext_files}')
except:
    pass

# Figures and tables inventory
import os
figs = sorted(os.listdir('outputs/figures/'))
tabs = sorted(os.listdir('outputs/tables/'))
print(f'\n=== INVENTORY ===')
print(f'Figures: {len(figs)}')
print(f'Tables: {len(tabs)}')
for f in figs:
    print(f'  {f}')
for t in tabs:
    print(f'  {t}')
