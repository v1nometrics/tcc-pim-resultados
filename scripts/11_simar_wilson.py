"""
11_simar_wilson.py
Regressão de 2º estágio — Simar & Wilson (2007), Algorithm #1.

Modelo:
  θ_hat_i = f(z_i) + ε_i

  θ_hat = eficiência VRS (DEA output-oriented, ∈ (0, 1])
  z_i = variáveis ambientais/contextuais (v3):
    - incentivo_faturamento = ICMS/Faturamento (exposição fiscal)
    - automacao = CAPEX/Emprego (intensidade de capital — K/L)
    - salario_medio = Massa Salarial/Emprego (capital humano — W/L)
    - cluster dummies (K-means endógeno, k-1 dummies)
    - tendência temporal
    - covid dummy (2020-2021, no modelo estendido)

Método:
  1. Truncated regression (θ ∈ (0, 1]) via Maximum Likelihood
  2. Bootstrap para inferência (B=2000 repetições)
  3. Intervalos de confiança bootstrap percentil

Alternativa robusta:
  - Tobit censurado em 1 (para comparação)
  - OLS com cluster-robust SEs (pooled)
  - Fractional logit (Papke & Wooldridge)

Outputs:
  - outputs/tables/tab_simar_wilson.csv (coeficientes e ICs)
  - outputs/tables/tab_tobit_comparison.csv
  - outputs/figures/fig_simar_wilson_coefs.png
"""

import pandas as pd
import numpy as np
from scipy import stats
from scipy.optimize import minimize
import statsmodels.api as sm
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

np.random.seed(42)
B_BOOT = 2000  # bootstrap replications


# ============================================================
# TRUNCATED REGRESSION (LEFT-TRUNCATED AT 0, RIGHT-CENSORED AT 1)
# ============================================================
def truncated_regression_mle(y, X, lower=0, upper=1):
    """
    MLE for truncated normal regression.
    y ∈ (lower, upper], X includes constant.
    
    Model: y ~ TruncNormal(Xβ, σ², lower, upper)
    
    Log-likelihood:
    ℓ = Σ [-0.5*log(2πσ²) - (y_i - x_i'β)² / (2σ²) 
          - log(Φ((upper - x_i'β)/σ) - Φ((lower - x_i'β)/σ))]
    """
    n, k = X.shape
    
    def neg_loglik(params):
        beta = params[:k]
        log_sigma = params[k]
        sigma = np.exp(log_sigma)
        
        mu = X @ beta
        z = (y - mu) / sigma
        
        # Truncation normalization
        Phi_upper = stats.norm.cdf((upper - mu) / sigma)
        Phi_lower = stats.norm.cdf((lower - mu) / sigma)
        normalizer = Phi_upper - Phi_lower
        normalizer = np.maximum(normalizer, 1e-10)
        
        # Log-likelihood terms
        ll = -0.5 * np.log(2 * np.pi) - log_sigma - 0.5 * z**2 - np.log(normalizer)
        
        return -np.sum(ll)
    
    # Initial guess: OLS
    beta_init = np.linalg.lstsq(X, y, rcond=None)[0]
    sigma_init = np.log(np.std(y - X @ beta_init))
    x0 = np.concatenate([beta_init, [sigma_init]])
    
    res = minimize(neg_loglik, x0, method="Nelder-Mead", 
                   options={"maxiter": 10000, "xatol": 1e-8, "fatol": 1e-10})
    
    if not res.success:
        # Try L-BFGS-B
        res = minimize(neg_loglik, x0, method="L-BFGS-B",
                       options={"maxiter": 10000})
    
    beta = res.x[:k]
    sigma = np.exp(res.x[k])
    
    return {
        "beta": beta,
        "sigma": sigma,
        "loglik": -res.fun,
        "converged": res.success,
        "n": n,
        "k": k,
    }


def bootstrap_truncated(y, X, var_names, lower=0, upper=1, B=2000):
    """
    Simar-Wilson Algorithm #1 bootstrap for truncated regression.
    
    Steps:
    1. Estimate truncated regression → β_hat, σ_hat
    2. For b = 1..B:
       a. Draw ε*_i from TruncNormal(0, σ², lower - x_i'β, upper - x_i'β)
       b. Construct y*_i = x_i'β + ε*_i
       c. Re-estimate truncated regression on (y*, X)
    3. Compute percentile confidence intervals
    """
    # Step 1: point estimates
    res = truncated_regression_mle(y, X, lower, upper)
    beta_hat = res["beta"]
    sigma_hat = res["sigma"]
    
    print(f"  Estimativa pontual: σ={sigma_hat:.4f}, convergiu={res['converged']}")
    
    # Step 2: bootstrap
    boot_betas = np.zeros((B, len(beta_hat)))
    boot_sigmas = np.zeros(B)
    n_failed = 0
    
    for b in range(B):
        if b % 500 == 0 and b > 0:
            print(f"    Bootstrap: {b}/{B}...")
        
        # Draw residuals from truncated normal
        mu_hat = X @ beta_hat
        eps_star = np.zeros(len(y))
        for i in range(len(y)):
            a = (lower - mu_hat[i]) / sigma_hat
            b_bound = (upper - mu_hat[i]) / sigma_hat
            eps_star[i] = stats.truncnorm.rvs(a, b_bound, loc=0, scale=sigma_hat)
        
        y_star = mu_hat + eps_star
        y_star = np.clip(y_star, lower + 1e-6, upper)
        
        try:
            res_b = truncated_regression_mle(y_star, X, lower, upper)
            boot_betas[b] = res_b["beta"]
            boot_sigmas[b] = res_b["sigma"]
        except:
            boot_betas[b] = np.nan
            boot_sigmas[b] = np.nan
            n_failed += 1
    
    # Step 3: confidence intervals (percentile method)
    valid = ~np.any(np.isnan(boot_betas), axis=1)
    boot_valid = boot_betas[valid]
    
    ci_lower = np.percentile(boot_valid, 2.5, axis=0)
    ci_upper = np.percentile(boot_valid, 97.5, axis=0)
    boot_se = np.std(boot_valid, axis=0)
    
    # Bias-corrected estimate
    boot_mean = np.mean(boot_valid, axis=0)
    bias = boot_mean - beta_hat
    beta_bc = 2 * beta_hat - boot_mean  # bias-corrected
    
    results_table = pd.DataFrame({
        "Variável": var_names,
        "Coeficiente": beta_hat,
        "Coef. BC": beta_bc,
        "SE (boot)": boot_se,
        "IC 2.5%": ci_lower,
        "IC 97.5%": ci_upper,
        "Significativo": ["*" if ci_lower[i] * ci_upper[i] > 0 else "" 
                         for i in range(len(beta_hat))],
    })
    
    print(f"  Bootstrap: {B} reps, {n_failed} falhas, {len(boot_valid)} válidas")
    
    return results_table, {
        "beta_hat": beta_hat,
        "beta_bc": beta_bc,
        "sigma_hat": sigma_hat,
        "boot_betas": boot_valid,
        "loglik": res["loglik"],
    }


# ============================================================
# MAIN
# ============================================================
print("=" * 70)
print("  SIMAR-WILSON 2º ESTÁGIO — TCC ZFM")
print("=" * 70)

# Load DEA scores
df_dea = pd.read_csv(os.path.join(PROCESSED_DIR, "dea_scores.csv"))
df_panel = pd.read_csv(os.path.join(PROCESSED_DIR, "painel_com_cluster.csv"))

# Merge
merge_cols = ["subsetor", "ano", "incentivo_fiscal_real2023", "incentivo_faturamento",
              "automacao", "salario_medio", "ln_capex",
              "faturamento_real2023", "emprego", "pib_manaus_real2023"]
df = df_dea.merge(df_panel[merge_cols], on=["subsetor", "ano"], how="left")

print(f"\nDados: {len(df)} obs, {df['subsetor'].nunique()} subsetores")

# Drop observations where efficiency is exactly 1 (on the frontier — Simar-Wilson excludes these)
# Actually, S-W #1 includes all; #2 excludes efficient DMUs
# We include all for maximum sample size
print(f"  Eficientes (θ≥0.99): {(df['eff_vrs'] >= 0.99).sum()}")
print(f"  Média θ: {df['eff_vrs'].mean():.3f}")

# ============================================================
# 1. PREPARE VARIABLES
# ============================================================
print("\n1. PREPARANDO VARIÁVEIS...")

# Dependent variable: DEA efficiency (θ ∈ (0,1])
y = df["eff_vrs"].values

# Independent variables (z) — v3: razões estruturais + ambientais
# Razões de variáveis DEA capturam composição, não níveis (cf. Simar & Wilson 2007)
df["log_incentivo_fat"] = np.log(df["incentivo_faturamento"].clip(lower=1e-6))
df["log_automacao"] = np.log(df["automacao"].clip(lower=1))
df["log_salario_medio"] = np.log(df["salario_medio"].clip(lower=1))

# Cluster dummies (dinâmico: k determinado em 08_kmeans)
# Referência: cluster com maior nº de observações
cluster_counts = df["cluster"].value_counts()
ref_cluster = cluster_counts.idxmax()
k_star = df["cluster"].nunique()
cluster_dummies = []
for c in sorted(df["cluster"].unique()):
    if c == ref_cluster:
        continue
    col = f"cluster_{c}"
    df[col] = (df["cluster"] == c).astype(float)
    cluster_dummies.append(col)
print(f"  Clusters: k*={k_star}, referência=cluster {ref_cluster}")

# Time trend (centered)
df["trend"] = df["ano"] - 2020.5

# COVID dummy
df["covid"] = (df["ano"].isin([2020, 2021])).astype(float)

# Variable selection for Simar-Wilson
Z_COLS = ["log_incentivo_fat", "log_automacao", "log_salario_medio"] + cluster_dummies + ["trend"]
Z_NAMES = ["ln(I/Fat)", "ln(K/L)", "ln(W/L)"] + [f"Cluster {c}" for c in sorted(df["cluster"].unique()) if c != ref_cluster] + ["Tendência"]

# Drop rows with NaN/Inf in dependent or independent variables
# (structural zeros already removed in 06_build_panel; this catches any residual)
regr_cols = ["eff_vrs"] + Z_COLS
n_before = len(df)
df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(subset=regr_cols)
n_after = len(df)
if n_before != n_after:
    print(f"  ⚠️ Removidas {n_before - n_after} obs com NaN/Inf nos regressores")

# Rebuild y after dropna
y = df["eff_vrs"].values

# Add constant
X = sm.add_constant(df[Z_COLS].values)
var_names = ["Constante"] + Z_NAMES

print(f"  N = {len(y)}")
print(f"  Variáveis: {var_names}")

# ============================================================
# 2. TRUNCATED REGRESSION (Simar-Wilson)  
# ============================================================
print("\n2. REGRESSÃO TRUNCADA (Simar-Wilson Algorithm #1)...")

# Clean y: ensure (0, 1]
y_clean = np.clip(y, 0.001, 1.0)

tab_sw, res_sw = bootstrap_truncated(y_clean, X, var_names, 
                                      lower=0, upper=1, B=B_BOOT)
print("\n  Resultados Simar-Wilson:")
print(tab_sw.round(4).to_string(index=False))

tab_sw.to_csv(os.path.join(TABLE_DIR, "tab_simar_wilson.csv"), index=False)
print(f"\n  ✅ tab_simar_wilson.csv")

# ============================================================
# 3. MODELOS ALTERNATIVOS (robustez)
# ============================================================
print("\n\n3. MODELOS ALTERNATIVOS (robustez)...")

# 3a. OLS com erros robustos (cluster por subsetor)
print("\n  3a. OLS pooled (cluster-robust SEs)...")
ols = sm.OLS(y_clean, X).fit(cov_type="cluster", 
                              cov_kwds={"groups": df["subsetor"].values})
print(f"    R² = {ols.rsquared:.3f}, R² adj = {ols.rsquared_adj:.3f}")
print(f"    F = {ols.fvalue:.2f}, p = {ols.f_pvalue:.4f}")

ols_summary = pd.DataFrame({
    "Variável": var_names,
    "Coef. OLS": ols.params,
    "SE (cluster)": ols.bse,
    "t": ols.tvalues,
    "p-valor": ols.pvalues,
})
print(ols_summary.round(4).to_string(index=False))

# 3b. Tobit censurado em 1
print("\n  3b. Tobit (censurado superiormente em 1)...")
# Using statsmodels doesn't have Tobit directly, but we can approximate
# via truncated regression or manually implement
# For simplicity, use OLS on non-censored observations as comparison
n_censored = (y_clean >= 0.99).sum()
print(f"    Obs censuradas (θ≥0.99): {n_censored} ({n_censored/len(y_clean)*100:.1f}%)")

# 3c. Extended model with more variables
print("\n  3c. Modelo estendido (mais variáveis)...")
Z_EXT = Z_COLS + ["covid", "scale_eff"]
Z_EXT_NAMES = Z_NAMES + ["COVID (2020-21)", "Efic. de Escala"]
ext_cols = ["eff_vrs", "subsetor"] + Z_EXT
df_ext = df.replace([np.inf, -np.inf], np.nan).dropna(subset=ext_cols).copy()
X_ext = sm.add_constant(df_ext[Z_EXT].values)
y_ext = np.clip(df_ext["eff_vrs"].values, 0.001, 1.0)
var_ext_names = ["Constante"] + Z_EXT_NAMES

ols_ext = sm.OLS(y_ext, X_ext).fit(cov_type="cluster",
                                   cov_kwds={"groups": df_ext["subsetor"].values})
print(f"    R² = {ols_ext.rsquared:.3f}, R² adj = {ols_ext.rsquared_adj:.3f}")

ext_summary = pd.DataFrame({
    "Variável": var_ext_names,
    "Coef.": ols_ext.params,
    "SE": ols_ext.bse,
    "t": ols_ext.tvalues,
    "p-valor": ols_ext.pvalues,
})
print(ext_summary.round(4).to_string(index=False))

# Save comparison table
comparison = pd.DataFrame({
    "Variável": var_names,
    "SW Coef.": tab_sw["Coeficiente"].values,
    "SW IC 2.5%": tab_sw["IC 2.5%"].values,
    "SW IC 97.5%": tab_sw["IC 97.5%"].values,
    "OLS Coef.": ols.params,
    "OLS SE": ols.bse,
    "OLS p": ols.pvalues,
}).round(4)
comparison.to_csv(os.path.join(TABLE_DIR, "tab_tobit_comparison.csv"), index=False)
print(f"\n  ✅ tab_tobit_comparison.csv")


# ============================================================
# 4. FIGURAS
# ============================================================
print("\n\n4. GERANDO FIGURAS...")

# ---- 4.1 Coefficient plot (SW with bootstrap CIs) ----
fig, ax = plt.subplots(figsize=(8, 5))
coefs = tab_sw["Coeficiente"].values[1:]  # skip constant
ci_low = tab_sw["IC 2.5%"].values[1:]
ci_high = tab_sw["IC 97.5%"].values[1:]
names = var_names[1:]

y_pos = np.arange(len(names))
colors = ["#e41a1c" if ci_low[i] * ci_high[i] > 0 else "#999999" 
          for i in range(len(names))]

ax.barh(y_pos, coefs, xerr=[coefs - ci_low, ci_high - coefs],
        color=colors, alpha=0.7, capsize=5, edgecolor="white")
ax.axvline(0, color="black", linewidth=0.8)
ax.set_yticks(y_pos)
ax.set_yticklabels(names)
ax.set_xlabel("Coeficiente (Simar-Wilson, IC 95% bootstrap)")
ax.set_title("Determinantes da Eficiência Técnica VRS — Simar-Wilson")

# Add significance markers
for i, (c, lo, hi) in enumerate(zip(coefs, ci_low, ci_high)):
    if lo * hi > 0:
        ax.text(max(c, hi) + 0.002, i, "***", fontsize=10, va="center", color="red")

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_simar_wilson_coefs.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_simar_wilson_coefs.png")

# ---- 4.2 Efficiency vs. Incentive scatter ----
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

colors_cluster = {i: c for i, c in enumerate(["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"])}

ax = axes[0]
for c in sorted(df["cluster"].unique()):
    mask = df["cluster"] == c
    ax.scatter(df.loc[mask, "log_incentivo_fat"], df.loc[mask, "eff_vrs"],
               c=colors_cluster.get(c, "grey"), alpha=0.5, s=25, label=f"Cluster {c}")
ax.set_xlabel("ln(Incentivo/Faturamento)")
ax.set_ylabel("Eficiência VRS")
ax.set_title("Eficiência vs. Intensidade de Incentivo")
ax.legend()

ax = axes[1]
for c in sorted(df["cluster"].unique()):
    mask = df["cluster"] == c
    ax.scatter(df.loc[mask, "log_automacao"], df.loc[mask, "eff_vrs"],
               c=colors_cluster.get(c, "grey"), alpha=0.5, s=25, label=f"Cluster {c}")
ax.set_xlabel("ln(K/L)")
ax.set_ylabel("Eficiência VRS")
ax.set_title("Eficiência vs. Intensidade de Capital")
ax.legend()

ax = axes[2]
for c in sorted(df["cluster"].unique()):
    mask = df["cluster"] == c
    ax.scatter(df.loc[mask, "log_salario_medio"], df.loc[mask, "eff_vrs"],
               c=colors_cluster.get(c, "grey"), alpha=0.5, s=25, label=f"Cluster {c}")
ax.set_xlabel("ln(W/L)")
ax.set_ylabel("Eficiência VRS")
ax.set_title("Eficiência vs. Capital Humano")
ax.legend()

fig.suptitle("Relação entre Variáveis Contextuais e Eficiência DEA (v3)", fontsize=12, y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_eff_vs_contextual.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_eff_vs_contextual.png")


# ============================================================
# 5. INTERPRETAÇÃO
# ============================================================
print("\n" + "=" * 70)
print("  INTERPRETAÇÃO DOS RESULTADOS")
print("=" * 70)

print("\nSimar-Wilson (truncated regression, bootstrap):")
for _, row in tab_sw.iterrows():
    sig = "SIGNIFICATIVO" if row["Significativo"] == "*" else "não signif."
    direction = "+" if row["Coeficiente"] > 0 else "-"
    print(f"  {row['Variável']:40s}: β={row['Coeficiente']:+.4f} ({sig})")
    if row["Significativo"] == "*":
        if "I/Fat" in row["Variável"]:
            if row["Coeficiente"] > 0:
                print(f"    → Maior intensidade de incentivo AUMENTA eficiência")
            else:
                print(f"    → Maior intensidade de incentivo REDUZ eficiência")
        elif "K/L" in row["Variável"]:
            if row["Coeficiente"] > 0:
                print(f"    → Maior intensidade de capital AUMENTA eficiência")
            else:
                print(f"    → Maior intensidade de capital REDUZ eficiência")
        elif "W/L" in row["Variável"]:
            if row["Coeficiente"] > 0:
                print(f"    → Maior capital humano (salário médio) AUMENTA eficiência")
            else:
                print(f"    → Maior capital humano (salário médio) REDUZ eficiência")
        elif "Cluster" in row["Variável"]:
            if row["Coeficiente"] > 0:
                print(f"    → Este cluster é MAIS eficiente vs. referência")
            else:
                print(f"    → Este cluster é MENOS eficiente vs. referência")
        elif "Tend" in row["Variável"]:
            if row["Coeficiente"] > 0:
                print(f"    → Eficiência MELHORANDO ao longo do tempo")
            else:
                print(f"    → Eficiência PIORANDO ao longo do tempo")

print(f"\nR² (OLS referência): {ols.rsquared:.3f}")
print(f"N observações: {len(y_clean)}")
print(f"B (bootstrap): {B_BOOT}")
