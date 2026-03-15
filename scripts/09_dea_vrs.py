"""
09_dea_vrs.py
Análise Envoltória de Dados (DEA) — BCC output-oriented (VRS).

Especificação (v2 — eficiência de incentivos):
  Inputs:  I (ICMS restituído real 2023), K (CAPEX real 2023)
  Outputs: Fat (Faturamento real 2023), E (Emprego SUFRAMA)

Execução:
  1. DEA cross-sectional para cada ano (2018-2023)
  2. DEA pooled (todos os anos juntos)
  3. DEA por cluster (K-means)
  4. Metafrontier: eficiência global vs. dentro-do-cluster → TGR

Outputs:
  - data/processed/dea_scores.csv (eficiências por subsetor-ano)
  - outputs/tables/tab_dea_summary.csv
  - outputs/tables/tab_dea_by_cluster.csv
  - outputs/tables/tab_metafrontier_tgr.csv
  - outputs/figures/fig_dea_scores.png
  - outputs/figures/fig_dea_by_cluster.png
  - outputs/figures/fig_tgr_evolution.png
"""

import pandas as pd
import numpy as np
import cvxpy as cp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
TABLE_DIR = os.path.join(BASE_DIR, "outputs", "tables")
FIG_DIR = os.path.join(BASE_DIR, "outputs", "figures")
os.makedirs(TABLE_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams.update({"figure.dpi": 150, "font.size": 10})
sns.set_style("whitegrid")


# ============================================================
# DEA SOLVER (output-oriented VRS — BCC)
# ============================================================
def _solve_dea_lp(X_mat, Y_mat, o, vrs=True):
    """
    Solve a single output-oriented DEA LP using scipy.linprog.
    
    Primal (output-oriented):
        max  φ
        s.t. Σ λ_j x_{ij} ≤ x_{io}       ∀ i
             Σ λ_j y_{rj} ≥ φ y_{ro}       ∀ r
             Σ λ_j = 1  (if VRS)
             λ_j ≥ 0, φ free (≥1 implied)
    
    scipy.linprog minimizes c^T z, so we minimize -φ.
    Decision vector z = [φ, λ_1, ..., λ_n]
    """
    from scipy.optimize import linprog
    
    n, m = X_mat.shape
    s = Y_mat.shape[1] if Y_mat.ndim > 1 else 1
    if Y_mat.ndim == 1:
        Y_mat = Y_mat.reshape(-1, 1)
    
    # z = [phi, lambda_1, ..., lambda_n]  (n+1 variables)
    # Objective: min -phi  → c = [-1, 0, 0, ..., 0]
    c = np.zeros(n + 1)
    c[0] = -1.0
    
    # Inequality constraints (A_ub @ z <= b_ub)
    # 1) Input: Σ λ_j x_{ij} ≤ x_{io}  → [0, x_1i, ..., x_ni] @ z ≤ x_{oi}
    # 2) Output: -Σ λ_j y_{rj} + φ y_{ro} ≤ 0  (rewritten: φ y_ro - Σ λ y_rj ≤ 0)
    
    A_ub_rows = []
    b_ub_rows = []
    
    # Input constraints
    for i in range(m):
        row = np.zeros(n + 1)
        row[0] = 0  # phi coefficient
        row[1:] = X_mat[:, i]  # lambda coefficients
        A_ub_rows.append(row)
        b_ub_rows.append(X_mat[o, i])
    
    # Output constraints: φ y_{ro} - Σ λ_j y_{rj} ≤ 0
    for r in range(s):
        row = np.zeros(n + 1)
        row[0] = Y_mat[o, r]  # phi coefficient
        row[1:] = -Y_mat[:, r]  # lambda coefficients (negative)
        A_ub_rows.append(row)
        b_ub_rows.append(0.0)
    
    A_ub = np.array(A_ub_rows)
    b_ub = np.array(b_ub_rows)
    
    # Equality constraint (VRS): Σ λ_j = 1
    A_eq = None
    b_eq = None
    if vrs:
        A_eq = np.zeros((1, n + 1))
        A_eq[0, 0] = 0  # phi
        A_eq[0, 1:] = 1  # sum of lambdas
        b_eq = np.array([1.0])
    
    # Bounds: phi ≥ 1 (output-oriented), lambda ≥ 0
    bounds = [(1.0, None)] + [(0.0, None)] * n
    
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  bounds=bounds, method="highs")
    
    if res.success:
        phi = res.x[0]
        lam = res.x[1:]
        return phi, lam, "ok"
    else:
        return np.nan, np.zeros(n), res.message


def dea_output_vrs(X_mat, Y_mat, names=None):
    """
    Output-oriented VRS DEA (BCC model) using scipy linprog (HiGHS solver).
    Efficiency = 1/φ (1 = efficient, <1 = inefficient).
    """
    n = X_mat.shape[0]
    
    if Y_mat.ndim == 1:
        Y_mat = Y_mat.reshape(-1, 1)
    
    phis = np.zeros(n)
    lambdas = np.zeros((n, n))
    status_list = []
    
    for o in range(n):
        phi, lam, status = _solve_dea_lp(X_mat, Y_mat, o, vrs=True)
        phis[o] = phi
        lambdas[o] = lam
        status_list.append(status)
    
    eff = np.where(phis > 0, 1.0 / phis, np.nan)
    
    return {
        "phi": phis,
        "eff": eff,
        "lambdas": lambdas,
        "names": names if names is not None else list(range(n)),
        "status": status_list,
    }


def dea_crs(X_mat, Y_mat, names=None):
    """CRS DEA (CCR model) using scipy linprog — for scale efficiency."""
    n = X_mat.shape[0]
    
    if Y_mat.ndim == 1:
        Y_mat = Y_mat.reshape(-1, 1)
    
    phis = np.zeros(n)
    
    for o in range(n):
        phi, _, status = _solve_dea_lp(X_mat, Y_mat, o, vrs=False)
        phis[o] = phi
    
    eff = np.where(phis > 0, 1.0 / phis, np.nan)
    return {"phi": phis, "eff": eff, "names": names}


# ============================================================
# 1. CARREGAR DADOS
# ============================================================
print("=" * 70)
print("  DEA-VRS (BCC orientado a output) — TCC ZFM")
print("=" * 70)

df = pd.read_csv(os.path.join(PROCESSED_DIR, "painel_com_cluster.csv"))
print(f"\nPainel: {df.shape[0]} obs, {df['subsetor'].nunique()} subsetores, clusters: {sorted(df['cluster'].unique())}")

# DEA specification (v2 — eficiência de incentivos + investimento → receita + emprego)
# Decisão: ICMS restituído como proxy de incentivo (dado observado por subsetor).
# VA removido: insumos disponíveis apenas para 11/22 sub (cf. Gouvêa 2024, Morais 2019).
INPUT_COLS = ["icms_restituido_real2023", "capex_real2023"]
OUTPUT_COLS = ["faturamento_real2023", "emprego"]
INPUT_LABELS = ["ICMS Restituído (I)", "CAPEX (K)"]
OUTPUT_LABELS = ["Faturamento (Fat)", "Emprego (E)"]


# ============================================================
# 2. DEA CROSS-SECTIONAL POR ANO
# ============================================================
print("\n2. DEA CROSS-SECTIONAL POR ANO...")

all_scores = []
years = sorted(df["ano"].unique())

for year in years:
    df_yr = df[df["ano"] == year].copy()
    
    X = df_yr[INPUT_COLS].values
    Y = df_yr[OUTPUT_COLS].values
    names = df_yr["subsetor"].values
    
    # Positivity filter: exclude DMU-years where any input or output is zero/negative.
    # Structural zeros (e.g. Couros 2018) should already be removed in 06_build_panel,
    # but this is a safety net for DEA feasibility (Cooper, Seiford & Tone 2007).
    pos_mask = np.all(X > 0, axis=1) & np.all(Y > 0, axis=1)
    if not np.all(pos_mask):
        n_drop = (~pos_mask).sum()
        dropped = names[~pos_mask]
        print(f"  ⚠️ {year}: excluindo {n_drop} DMU(s) sem positividade: {dropped}")
        X = X[pos_mask]
        Y = Y[pos_mask]
        names = names[pos_mask]
        df_yr = df_yr[pos_mask.tolist()]
    
    if len(names) < 3:
        print(f"  ⚠️ {year}: apenas {len(names)} DMUs, pulando")
        continue
    
    # VRS (BCC)
    res_vrs = dea_output_vrs(X, Y, names)
    
    # CRS (CCR) for scale efficiency
    res_crs = dea_crs(X, Y, names)
    
    for i, sub in enumerate(names):
        all_scores.append({
            "subsetor": sub,
            "ano": year,
            "cluster": df_yr[df_yr["subsetor"] == sub]["cluster"].values[0],
            "eff_vrs": res_vrs["eff"][i],
            "eff_crs": res_crs["eff"][i],
            "phi_vrs": res_vrs["phi"][i],
            "status": res_vrs["status"][i],
        })
    
    # Summary for this year
    eff_vrs = res_vrs["eff"]
    n_eff = np.sum(np.isclose(eff_vrs, 1.0, atol=0.01))
    print(f"  {year}: {len(names)} DMUs, "
          f"eficiência média={np.nanmean(eff_vrs):.3f}, "
          f"n_eficientes={n_eff}, "
          f"min={np.nanmin(eff_vrs):.3f}")

df_scores = pd.DataFrame(all_scores)

# Scale efficiency = CRS / VRS
df_scores["scale_eff"] = df_scores["eff_crs"] / df_scores["eff_vrs"]
df_scores["scale_eff"] = df_scores["scale_eff"].clip(0, 1)

# Returns to scale classification
df_scores["rts"] = "CRS"
df_scores.loc[df_scores["scale_eff"] < 0.99, "rts"] = "Non-CRS"
# More precise: IRS if VRS > CRS at small scale, DRS if at large scale
# Simplified: compare to NIRS (non-increasing returns)
# For now, classify based on sum of lambdas from VRS solution

print(f"\nEficiência média por ano:")
yearly_eff = df_scores.groupby("ano").agg(
    eff_vrs_mean=("eff_vrs", "mean"),
    eff_vrs_median=("eff_vrs", "median"),
    eff_crs_mean=("eff_crs", "mean"),
    scale_eff_mean=("scale_eff", "mean"),
    n_efficient=("eff_vrs", lambda x: (x > 0.99).sum()),
).round(3)
print(yearly_eff.to_string())


# ============================================================
# 3. DEA POOLED (todos os anos juntos)  
# ============================================================
print("\n\n3. DEA POOLED...")

X_pool = df[INPUT_COLS].values
Y_pool = df[OUTPUT_COLS].values
names_pool = [f"{r['subsetor']}_{r['ano']}" for _, r in df.iterrows()]

# Positivity filter (safety net — structural zeros removed in 06_build_panel)
pos_pool = np.all(X_pool > 0, axis=1) & np.all(Y_pool > 0, axis=1)
if not np.all(pos_pool):
    n_drop = (~pos_pool).sum()
    print(f"  ⚠️ Pooled: excluindo {n_drop} obs sem positividade")
    X_pool = X_pool[pos_pool]
    Y_pool = Y_pool[pos_pool]
    names_pool = [n for n, m in zip(names_pool, pos_pool) if m]

res_pool = dea_output_vrs(X_pool, Y_pool, names_pool)

df["eff_pooled"] = res_pool["eff"]
n_eff_pool = np.sum(np.isclose(res_pool["eff"], 1.0, atol=0.01))
print(f"  Pooled: {len(names_pool)} DMUs, "
      f"média={np.nanmean(res_pool['eff']):.3f}, "
      f"n_eficientes={n_eff_pool}, "
      f"min={np.nanmin(res_pool['eff']):.3f}")


# ============================================================
# 4. DEA POR CLUSTER (group frontiers)
# ============================================================
print("\n\n4. DEA POR CLUSTER (fronteiras de grupo)...")

df_scores["eff_group"] = np.nan

for c in sorted(df["cluster"].unique()):
    for year in years:
        mask = (df_scores["cluster"] == c) & (df_scores["ano"] == year)
        df_c = df[(df["cluster"] == c) & (df["ano"] == year)]
        
        if len(df_c) < 2:
            # Can't run DEA with < 2 DMUs
            df_scores.loc[mask, "eff_group"] = 1.0
            continue
        
        X_c = df_c[INPUT_COLS].values
        Y_c = df_c[OUTPUT_COLS].values
        # Positivity filter for group frontier
        pos_c = np.all(X_c > 0, axis=1) & np.all(Y_c > 0, axis=1)
        if not np.all(pos_c):
            X_c = X_c[pos_c]
            Y_c = Y_c[pos_c]
        names_c = df_c["subsetor"].values
        if not np.all(pos_c):
            names_c = names_c[pos_c]
        
        res_c = dea_output_vrs(X_c, Y_c, names_c)
        
        for i, sub in enumerate(names_c):
            idx = mask & (df_scores["subsetor"] == sub)
            df_scores.loc[idx, "eff_group"] = res_c["eff"][i]

print("  Eficiência média por cluster (group frontier):")
cluster_eff = df_scores.groupby("cluster").agg(
    eff_global_mean=("eff_vrs", "mean"),
    eff_group_mean=("eff_group", "mean"),
    n_obs=("eff_vrs", "count"),
).round(3)
print(cluster_eff.to_string())


# ============================================================
# 5. METAFRONTIER & TGR
# ============================================================
print("\n\n5. METAFRONTIER & TGR...")

# TGR = eff_global / eff_group
# Technology Gap Ratio: how close is the group frontier to the metafrontier
df_scores["tgr"] = df_scores["eff_vrs"] / df_scores["eff_group"]
df_scores["tgr"] = df_scores["tgr"].clip(0, 1)

print("  TGR médio por cluster:")
tgr_summary = df_scores.groupby("cluster").agg(
    tgr_mean=("tgr", "mean"),
    tgr_median=("tgr", "median"),
    tgr_std=("tgr", "std"),
).round(3)
print(tgr_summary.to_string())

print("\n  TGR médio por cluster × ano:")
tgr_yr = df_scores.pivot_table(index="cluster", columns="ano", values="tgr", aggfunc="mean").round(3)
print(tgr_yr.to_string())


# ============================================================
# 6. SALVAR RESULTADOS
# ============================================================
print("\n\n6. SALVANDO RESULTADOS...")

# Full scores
outpath = os.path.join(PROCESSED_DIR, "dea_scores.csv")
df_scores.to_csv(outpath, index=False)
print(f"  ✅ {outpath}")

# Summary table
tab_summary = df_scores.groupby("subsetor").agg(
    cluster=("cluster", "first"),
    eff_vrs_mean=("eff_vrs", "mean"),
    eff_vrs_std=("eff_vrs", "std"),
    eff_crs_mean=("eff_crs", "mean"),
    scale_eff_mean=("scale_eff", "mean"),
    eff_group_mean=("eff_group", "mean"),
    tgr_mean=("tgr", "mean"),
).round(3).sort_values(["cluster", "eff_vrs_mean"], ascending=[True, False])

tab_summary.to_csv(os.path.join(TABLE_DIR, "tab_dea_summary.csv"))
print(f"  ✅ tab_dea_summary.csv")
print("\nResumo DEA por subsetor:")
print(tab_summary.to_string())

# Metafrontier TGR table
tab_tgr = df_scores.pivot_table(
    index="subsetor", columns="ano", values="tgr", aggfunc="mean"
).round(3)
tab_tgr.to_csv(os.path.join(TABLE_DIR, "tab_metafrontier_tgr.csv"))
print(f"\n  ✅ tab_metafrontier_tgr.csv")


# ============================================================
# 7. FIGURAS
# ============================================================
print("\n\n7. GERANDO FIGURAS...")

colors_cluster = {0: "#e41a1c", 1: "#377eb8", 2: "#4daf4a"}

# ---- 7.1 Eficiência VRS por subsetor (barras horizontais, cor por cluster) ----
fig, ax = plt.subplots(figsize=(10, 8))
sub_eff = df_scores.groupby("subsetor").agg(
    eff=("eff_vrs", "mean"),
    cluster=("cluster", "first"),
).sort_values("eff")

bar_colors = [colors_cluster[c] for c in sub_eff["cluster"]]
ax.barh(range(len(sub_eff)), sub_eff["eff"], color=bar_colors, edgecolor="white")
ax.set_yticks(range(len(sub_eff)))
ax.set_yticklabels(sub_eff.index, fontsize=8)
ax.set_xlabel("Eficiência Técnica VRS (média 2018-2023)")
ax.set_title("Eficiência DEA-BCC Output-Oriented por Subsetor")
ax.axvline(1.0, color="gray", linestyle="--", alpha=0.5)

# Add cluster legend
from matplotlib.patches import Patch
legend_items = [Patch(facecolor=colors_cluster[c], label=f"Cluster {c}") 
                for c in sorted(colors_cluster.keys()) if c in sub_eff["cluster"].values]
ax.legend(handles=legend_items, loc="lower right")

for i, (idx, row) in enumerate(sub_eff.iterrows()):
    ax.text(row["eff"] + 0.005, i, f"{row['eff']:.3f}", va="center", fontsize=7)

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_dea_scores.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_dea_scores.png")

# ---- 7.2 Eficiência VRS por cluster (boxplot por ano) ----
fig, axes = plt.subplots(1, 3, figsize=(14, 5), sharey=True)
for c in sorted(df_scores["cluster"].unique()):
    ax = axes[c]
    data_c = df_scores[df_scores["cluster"] == c]
    bp_data = [data_c[data_c["ano"] == y]["eff_vrs"].values for y in years]
    bp = ax.boxplot(bp_data, labels=[str(y) for y in years], patch_artist=True)
    for patch in bp["boxes"]:
        patch.set_facecolor(colors_cluster[c])
        patch.set_alpha(0.6)
    ax.set_title(f"Cluster {c} ({len(data_c['subsetor'].unique())} sub.)")
    ax.set_xlabel("Ano")
    if c == 0:
        ax.set_ylabel("Eficiência VRS")
    ax.set_ylim(0, 1.1)
    ax.axhline(1.0, color="gray", linestyle="--", alpha=0.5)

fig.suptitle("Eficiência DEA-BCC por Cluster e Ano", fontsize=13, y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_dea_by_cluster.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_dea_by_cluster.png")

# ---- 7.3 TGR evolution ----
fig, ax = plt.subplots(figsize=(10, 6))
for c in sorted(df_scores["cluster"].unique()):
    data_c = df_scores[df_scores["cluster"] == c].groupby("ano")["tgr"].mean()
    ax.plot(data_c.index, data_c.values, "o-", color=colors_cluster[c],
            label=f"Cluster {c}", linewidth=2, markersize=6)

ax.set_xlabel("Ano")
ax.set_ylabel("Technology Gap Ratio (TGR)")
ax.set_title("Evolução do TGR por Cluster — Metafronteira")
ax.legend()
ax.set_ylim(0, 1.1)
ax.set_xticks(years)
ax.axhline(1.0, color="gray", linestyle="--", alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_tgr_evolution.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_tgr_evolution.png")

# ---- 7.4 Efficiency frontier scatter (2D: K vs Faturamento by year) ----
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
for idx, (ax, year) in enumerate(zip(axes.flat, years)):
    df_yr = df_scores[df_scores["ano"] == year]
    df_data = df[df["ano"] == year]
    
    for c in sorted(df_yr["cluster"].unique()):
        mask = df_yr["cluster"] == c
        subs = df_yr[mask]["subsetor"].values
        data_c = df_data[df_data["subsetor"].isin(subs)]
        
        ax.scatter(data_c["capex_real2023"] / 1e9, data_c["faturamento_real2023"] / 1e9,
                  c=colors_cluster[c], label=f"C{c}", s=40, alpha=0.7,
                  edgecolors="white", linewidth=0.3)
    
    ax.set_xlabel("CAPEX (R$ bi 2023)")
    ax.set_ylabel("Faturamento (R$ bi 2023)")
    ax.set_title(f"{year}")
    if idx == 0:
        ax.legend(fontsize=8)

fig.suptitle("Fronteira de Eficiência: Capital vs. Faturamento", fontsize=13, y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_frontier_scatter.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_frontier_scatter.png")


print("\n" + "=" * 70)
print("  DEA CONCLUÍDO")
print("=" * 70)
print(f"\n  DMUs: {df_scores['subsetor'].nunique()}")
print(f"  Anos: {years}")
print(f"  Eficiência VRS média global: {df_scores['eff_vrs'].mean():.3f}")
print(f"  DMUs eficientes (VRS≥0.99) por ano: {yearly_eff['n_efficient'].to_dict()}")
print(f"  TGR médio por cluster: {tgr_summary['tgr_mean'].to_dict()}")
