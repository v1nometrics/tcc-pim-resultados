"""
10_malmquist.py
Índice de Produtividade de Malmquist (orientado a output, CRS principal).

Decomposição de Färe et al. (1994):
    M(x^{t+1}, y^{t+1}, x^t, y^t) = EC × TC

    Componente adicional (decomposição de escala):
        EC = PEC × SC
        PEC: Pure Efficiency Change (VRS)
        SC: Scale Change (= EC/PEC)

  EC = D^{t+1}(x^{t+1}, y^{t+1}) / D^t(x^t, y^t)
     = eficiência relativa em t+1 / eficiência em t
     → catching-up (mudança de eficiência técnica)

  TC = [D^t(x^{t+1}, y^{t+1}) / D^{t+1}(x^{t+1}, y^{t+1}) ×
        D^t(x^t, y^t) / D^{t+1}(x^t, y^t)]^{1/2}
     → frontier shift (mudança tecnológica)

  M > 1: ganho de produtividade
  M < 1: perda de produtividade

Outputs:
  - data/processed/malmquist_results.csv (índices por subsetor-período)
  - outputs/tables/tab_malmquist_summary.csv
  - outputs/figures/fig_malmquist_decomp.png
  - outputs/figures/fig_malmquist_evolution.png
"""

import pandas as pd
import numpy as np
from scipy.optimize import linprog
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

plt.rcParams.update({"figure.dpi": 150, "font.size": 10})
sns.set_style("whitegrid")


# ============================================================
# DEA SOLVER (reusável — output-oriented VRS via scipy LP)
# ============================================================
def dea_phi(X_ref, Y_ref, x_eval, y_eval, vrs=True):
    """
    Compute output-oriented efficiency phi for a SINGLE DMU (x_eval, y_eval)
    against the reference technology defined by (X_ref, Y_ref).
    
    Returns phi (≥1). Efficiency = 1/phi.
    """
    n = X_ref.shape[0]
    m = X_ref.shape[1]
    s = Y_ref.shape[1] if Y_ref.ndim > 1 else 1
    if Y_ref.ndim == 1:
        Y_ref = Y_ref.reshape(-1, 1)
    if y_eval.ndim == 0 or len(y_eval.shape) == 0:
        y_eval = np.array([y_eval])
    
    # z = [phi, lambda_1, ..., lambda_n]
    c = np.zeros(n + 1)
    c[0] = -1.0  # minimize -phi = maximize phi
    
    A_ub_rows = []
    b_ub_rows = []
    
    # Input constraints: Σ λ_j x_{ij} ≤ x_eval_i
    for i in range(m):
        row = np.zeros(n + 1)
        row[1:] = X_ref[:, i]
        A_ub_rows.append(row)
        b_ub_rows.append(x_eval[i])
    
    # Output constraints: φ y_eval_r - Σ λ_j y_{rj} ≤ 0
    for r in range(s):
        row = np.zeros(n + 1)
        row[0] = y_eval[r]
        row[1:] = -Y_ref[:, r]
        A_ub_rows.append(row)
        b_ub_rows.append(0.0)
    
    A_ub = np.array(A_ub_rows)
    b_ub = np.array(b_ub_rows)
    
    A_eq = None
    b_eq = None
    if vrs:
        A_eq = np.zeros((1, n + 1))
        A_eq[0, 1:] = 1
        b_eq = np.array([1.0])
    
    bounds = [(1.0, None)] + [(0.0, None)] * n
    
    res = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq,
                  bounds=bounds, method="highs")
    
    if res.success:
        return res.x[0]  # phi
    else:
        return np.nan


# ============================================================
# MALMQUIST INDEX COMPUTATION
# ============================================================
def compute_malmquist(df, input_cols, output_cols, year_col="ano",
                      dmu_col="subsetor", vrs_main=False):
    """
    Compute Malmquist TFP index and its decomposition for all DMU pairs
    across consecutive periods.
    
    Returns DataFrame with columns:
    subsetor, period (e.g. "2018-2019"), EC, TC, M, PEC, SC
    """
    years = sorted(df[year_col].unique())
    results = []
    
    for t_idx in range(len(years) - 1):
        t = years[t_idx]
        t1 = years[t_idx + 1]
        
        df_t = df[df[year_col] == t]
        df_t1 = df[df[year_col] == t1]
        
        # Reference technologies
        X_t = df_t[input_cols].values
        Y_t = df_t[output_cols].values
        X_t1 = df_t1[input_cols].values
        Y_t1 = df_t1[output_cols].values
        
        dmus_t = df_t[dmu_col].values
        dmus_t1 = df_t1[dmu_col].values
        
        # Positivity filter: only keep DMUs with all inputs/outputs > 0.
        # Structural zeros (e.g. Couros 2018) already removed in 06_build_panel,
        # but safety net for Malmquist cross-period feasibility.
        pos_t = np.all(X_t > 0, axis=1) & np.all(Y_t > 0, axis=1)
        pos_t1 = np.all(X_t1 > 0, axis=1) & np.all(Y_t1 > 0, axis=1)
        X_t, Y_t, dmus_t = X_t[pos_t], Y_t[pos_t], dmus_t[pos_t]
        X_t1, Y_t1, dmus_t1 = X_t1[pos_t1], Y_t1[pos_t1], dmus_t1[pos_t1]
        
        # Common DMUs (handles unbalanced panel naturally)
        common = set(dmus_t) & set(dmus_t1)
        
        for dmu in common:
            idx_t = np.where(dmus_t == dmu)[0][0]
            idx_t1 = np.where(dmus_t1 == dmu)[0][0]
            
            x_t = X_t[idx_t]
            y_t = Y_t[idx_t]
            x_t1 = X_t1[idx_t1]
            y_t1 = Y_t1[idx_t1]
            
            # Four distance functions (phi values)
            # D^t(x^t, y^t): DMU at t against frontier at t
            phi_tt = dea_phi(X_t, Y_t, x_t, y_t, vrs=vrs_main)
            
            # D^{t+1}(x^{t+1}, y^{t+1}): DMU at t+1 against frontier at t+1
            phi_t1t1 = dea_phi(X_t1, Y_t1, x_t1, y_t1, vrs=vrs_main)
            
            # D^t(x^{t+1}, y^{t+1}): DMU at t+1 against frontier at t
            phi_t_t1 = dea_phi(X_t, Y_t, x_t1, y_t1, vrs=vrs_main)
            
            # D^{t+1}(x^t, y^t): DMU at t against frontier at t+1
            phi_t1_t = dea_phi(X_t1, Y_t1, x_t, y_t, vrs=vrs_main)

            # Pure efficiency component under VRS (contemporaneous frontiers)
            phi_tt_vrs = dea_phi(X_t, Y_t, x_t, y_t, vrs=True)
            phi_t1t1_vrs = dea_phi(X_t1, Y_t1, x_t1, y_t1, vrs=True)
            
            # Skip if any NaN
            if any(np.isnan([phi_tt, phi_t1t1, phi_t_t1, phi_t1_t, phi_tt_vrs, phi_t1t1_vrs])):
                results.append({
                    "subsetor": dmu,
                    "period": f"{t}-{t1}",
                    "t": t,
                    "t1": t1,
                    "EC": np.nan,
                    "TC": np.nan,
                    "M": np.nan,
                    "PEC": np.nan,
                    "SC": np.nan,
                })
                continue
            
            # Efficiency change (EC = catching up)
            # EC = D^t(x^t, y^t) / D^{t+1}(x^{t+1}, y^{t+1})
            # Using phi (expansion): EC = phi_tt / phi_t1t1
            # If EC > 1: DMU caught up (got closer to frontier)
            EC = phi_tt / phi_t1t1
            
            # Technical change (TC = frontier shift)
            # TC = [phi_t1t1/phi_t_t1 * phi_tt/phi_t1_t]^0.5
            ratio1 = phi_t1t1 / phi_t_t1 if phi_t_t1 > 0 else np.nan
            ratio2 = phi_tt / phi_t1_t if phi_t1_t > 0 else np.nan
            
            if np.isnan(ratio1) or np.isnan(ratio2) or ratio1 <= 0 or ratio2 <= 0:
                TC = np.nan
            else:
                TC = (ratio1 * ratio2) ** 0.5
            
            # Malmquist = EC × TC
            M = EC * TC if not np.isnan(EC) and not np.isnan(TC) else np.nan

            # Pure efficiency change (VRS) and scale change
            PEC = phi_tt_vrs / phi_t1t1_vrs if phi_t1t1_vrs > 0 else np.nan
            SC = EC / PEC if (not np.isnan(EC) and not np.isnan(PEC) and PEC > 0) else np.nan
            
            results.append({
                "subsetor": dmu,
                "period": f"{t}-{t1}",
                "t": t,
                "t1": t1,
                "EC": EC,
                "TC": TC,
                "M": M,
                "PEC": PEC,
                "SC": SC,
                "phi_tt": phi_tt,
                "phi_t1t1": phi_t1t1,
                "phi_t_t1": phi_t_t1,
                "phi_t1_t": phi_t1_t,
                "phi_tt_vrs": phi_tt_vrs,
                "phi_t1t1_vrs": phi_t1t1_vrs,
            })
    
    return pd.DataFrame(results)


# ============================================================
# MAIN
# ============================================================
print("=" * 70)
print("  ÍNDICE DE MALMQUIST — TCC ZFM")
print("=" * 70)

df = pd.read_csv(os.path.join(PROCESSED_DIR, "painel_com_cluster.csv"))
print(f"\nPainel: {df.shape[0]} obs, {df['subsetor'].nunique()} subsetores")

# v2: mesma especificação do DEA (eficiência de incentivos)
INPUT_COLS = ["icms_restituido_real2023", "capex_real2023"]
OUTPUT_COLS = ["faturamento_real2023", "emprego"]

# ============================================================
# 1. COMPUTE MALMQUIST
# ============================================================
print("\n1. CALCULANDO ÍNDICE DE MALMQUIST (CRS — padrão Färe et al. 1994)...")
print("   Nota: Malmquist usa CRS para evitar infeasibilidade cross-period.")
print("   (4 DEAs × 22 DMUs × 5 períodos = 440 LPs)")

df_malm = compute_malmquist(df, INPUT_COLS, OUTPUT_COLS, vrs_main=False)
print(f"\n  Resultados: {len(df_malm)} observações")

# Add cluster info
cluster_map = df.groupby("subsetor")["cluster"].first().to_dict()
df_malm["cluster"] = df_malm["subsetor"].map(cluster_map)

# Save
outpath = os.path.join(PROCESSED_DIR, "malmquist_results.csv")
df_malm.to_csv(outpath, index=False)
print(f"  ✅ {outpath}")

# ============================================================
# 2. SUMMARY TABLES
# ============================================================
print("\n2. RESUMO...")

# By period
period_summary = df_malm.groupby("period").agg(
    EC_mean=("EC", "mean"),
    EC_median=("EC", "median"),
    PEC_mean=("PEC", "mean"),
    SC_mean=("SC", "mean"),
    TC_mean=("TC", "mean"),
    TC_median=("TC", "median"),
    M_mean=("M", "mean"),
    M_median=("M", "median"),
    n=("M", "count"),
).round(3)
print("\nMédia por período:")
print(period_summary.to_string())

# By subsetor (geometric mean across periods)
sub_summary = df_malm.groupby("subsetor").agg(
    cluster=("cluster", "first"),
    EC_gmean=("EC", lambda x: np.exp(np.nanmean(np.log(x.clip(lower=1e-6))))),
    PEC_gmean=("PEC", lambda x: np.exp(np.nanmean(np.log(x.clip(lower=1e-6))))),
    SC_gmean=("SC", lambda x: np.exp(np.nanmean(np.log(x.clip(lower=1e-6))))),
    TC_gmean=("TC", lambda x: np.exp(np.nanmean(np.log(x.clip(lower=1e-6))))),
    M_gmean=("M", lambda x: np.exp(np.nanmean(np.log(x.clip(lower=1e-6))))),
    n_periods=("M", lambda x: x.notna().sum()),
).round(3).sort_values(["cluster", "M_gmean"], ascending=[True, False])

print("\nMédia geométrica por subsetor:")
print(sub_summary.to_string())

sub_summary.to_csv(os.path.join(TABLE_DIR, "tab_malmquist_summary.csv"))
print(f"\n  ✅ tab_malmquist_summary.csv")

# By cluster
cluster_summary = df_malm.groupby("cluster").agg(
    EC_gmean=("EC", lambda x: np.exp(np.nanmean(np.log(x.clip(lower=1e-6))))),
    PEC_gmean=("PEC", lambda x: np.exp(np.nanmean(np.log(x.clip(lower=1e-6))))),
    SC_gmean=("SC", lambda x: np.exp(np.nanmean(np.log(x.clip(lower=1e-6))))),
    TC_gmean=("TC", lambda x: np.exp(np.nanmean(np.log(x.clip(lower=1e-6))))),
    M_gmean=("M", lambda x: np.exp(np.nanmean(np.log(x.clip(lower=1e-6))))),
    n=("M", "count"),
).round(3)
print("\nMédia geométrica por cluster:")
print(cluster_summary.to_string())

# Overall
M_overall = np.exp(np.nanmean(np.log(df_malm["M"].clip(lower=1e-6))))
EC_overall = np.exp(np.nanmean(np.log(df_malm["EC"].clip(lower=1e-6))))
PEC_overall = np.exp(np.nanmean(np.log(df_malm["PEC"].clip(lower=1e-6))))
SC_overall = np.exp(np.nanmean(np.log(df_malm["SC"].clip(lower=1e-6))))
TC_overall = np.exp(np.nanmean(np.log(df_malm["TC"].clip(lower=1e-6))))
print(f"\nGeral (média geométrica): M={M_overall:.3f}, EC={EC_overall:.3f}, PEC={PEC_overall:.3f}, SC={SC_overall:.3f}, TC={TC_overall:.3f}")
if M_overall > 1:
    print("  → Ganho de produtividade no período")
else:
    print("  → Perda de produtividade no período")

# ============================================================
# 3. FIGURES
# ============================================================
print("\n3. GERANDO FIGURAS...")

colors_cluster = {0: "#e41a1c", 1: "#377eb8", 2: "#4daf4a"}
periods = sorted(df_malm["period"].unique())

# ---- 3.1 Malmquist decomposition by period ----
fig, ax = plt.subplots(figsize=(10, 6))
x_pos = np.arange(len(periods))
width = 0.25

ec_vals = [period_summary.loc[p, "EC_mean"] for p in periods]
tc_vals = [period_summary.loc[p, "TC_mean"] for p in periods]
m_vals = [period_summary.loc[p, "M_mean"] for p in periods]

bars1 = ax.bar(x_pos - width, ec_vals, width, label="EC (catching-up)", color="#377eb8", alpha=0.8)
bars2 = ax.bar(x_pos, tc_vals, width, label="TC (frontier shift)", color="#4daf4a", alpha=0.8)
bars3 = ax.bar(x_pos + width, m_vals, width, label="M (produtividade total)", color="#984ea3", alpha=0.8)

ax.axhline(1.0, color="gray", linestyle="--", alpha=0.5, label="Sem mudança")
ax.set_xticks(x_pos)
ax.set_xticklabels(periods, fontsize=9)
ax.set_ylabel("Índice (>1 = ganho, <1 = perda)")
ax.set_title("Decomposição do Índice de Malmquist por Período")
ax.legend(fontsize=9)

# Add value labels
for bars in [bars1, bars2, bars3]:
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.2f}", xy=(bar.get_x() + bar.get_width() / 2, height),
                   xytext=(0, 3), textcoords="offset points", ha="center", fontsize=7)

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_malmquist_decomp.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_malmquist_decomp.png")

# ---- 3.2 Malmquist evolution by cluster ----
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
for c in sorted(df_malm["cluster"].unique()):
    data_c = df_malm[df_malm["cluster"] == c]
    ax = axes[c]
    
    ec_c = data_c.groupby("period")["EC"].mean()
    tc_c = data_c.groupby("period")["TC"].mean()
    m_c = data_c.groupby("period")["M"].mean()
    
    ax.plot(range(len(periods)), [ec_c.get(p, np.nan) for p in periods], 
            "o-", label="EC", color="#377eb8", linewidth=2)
    ax.plot(range(len(periods)), [tc_c.get(p, np.nan) for p in periods], 
            "s-", label="TC", color="#4daf4a", linewidth=2)
    ax.plot(range(len(periods)), [m_c.get(p, np.nan) for p in periods], 
            "D-", label="M", color="#984ea3", linewidth=2)
    
    ax.axhline(1.0, color="gray", linestyle="--", alpha=0.5)
    ax.set_xticks(range(len(periods)))
    ax.set_xticklabels(periods, fontsize=8, rotation=30)
    n_subs = data_c["subsetor"].nunique()
    ax.set_title(f"Cluster {c} ({n_subs} sub.)")
    if c == 0:
        ax.set_ylabel("Índice de Malmquist")
    ax.legend(fontsize=8)

fig.suptitle("Evolução do Índice de Malmquist por Cluster", fontsize=13, y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_malmquist_evolution.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_malmquist_evolution.png")

# ---- 3.3 EC vs TC scatter (by subsetor, averaged) ----
fig, ax = plt.subplots(figsize=(10, 8))
for c in sorted(sub_summary["cluster"].unique()):
    mask = sub_summary["cluster"] == c
    subs = sub_summary[mask]
    ax.scatter(subs["TC_gmean"], subs["EC_gmean"], 
               c=colors_cluster[c], s=60, alpha=0.8, edgecolors="white",
               label=f"Cluster {c}")
    for idx, row in subs.iterrows():
        short = idx[:12] + "..." if len(idx) > 15 else idx
        ax.annotate(short, (row["TC_gmean"], row["EC_gmean"]),
                   textcoords="offset points", xytext=(5, 5), fontsize=7)

ax.axhline(1.0, color="gray", linestyle="--", alpha=0.3)
ax.axvline(1.0, color="gray", linestyle="--", alpha=0.3)
ax.set_xlabel("TC (Mudança Tecnológica) — média geométrica 2018-2023")
ax.set_ylabel("EC (Catching-up) — média geométrica 2018-2023")
ax.set_title("Decomposição de Malmquist: EC vs. TC por Subsetor")
ax.legend()

# Quadrant labels
xlim = ax.get_xlim()
ylim = ax.get_ylim()
ax.text(0.99 * xlim[1], 0.99 * ylim[1], "Progresso total", ha="right", va="top", fontsize=8, color="green", alpha=0.6)
ax.text(0.99 * xlim[0] + 0.01, 0.99 * ylim[0] + 0.01, "Regresso total", ha="left", va="bottom", fontsize=8, color="red", alpha=0.6)

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_malmquist_ec_tc.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_malmquist_ec_tc.png")


print("\n" + "=" * 70)
print("  MALMQUIST CONCLUÍDO")
print("=" * 70)
print(f"\n  Geral: M={M_overall:.3f}, EC={EC_overall:.3f}, PEC={PEC_overall:.3f}, SC={SC_overall:.3f}, TC={TC_overall:.3f}")
print(f"  Interpretação: {'Ganho' if M_overall > 1 else 'Perda'} de produtividade")
print(f"    EC {'>' if EC_overall > 1 else '<'} 1: {'catching-up' if EC_overall > 1 else 'afastamento da fronteira'}")
print(f"    PEC {'>' if PEC_overall > 1 else '<'} 1: {'ganho de eficiência pura' if PEC_overall > 1 else 'perda de eficiência pura'}")
print(f"    SC {'>' if SC_overall > 1 else '<'} 1: {'ganho de escala' if SC_overall > 1 else 'perda de escala'}")
print(f"    TC {'>' if TC_overall > 1 else '<'} 1: {'inovação na fronteira' if TC_overall > 1 else 'retrocesso tecnológico'}")
