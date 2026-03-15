"""
08_kmeans_cluster.py
Clusterização K-means dos subsetores do PIM — v3 (3 variáveis estruturais).

Variáveis de clusterização (padronizadas via StandardScaler):
  1. automacao              = K / L    (CAPEX por empregado — proxy de intensidade tecnológica)
  2. salario_medio          = W / L    (massa salarial por empregado — proxy capital humano)
  3. incentivo_faturamento  = I / Fat  (ICMS restituído / Faturamento — exposição fiscal)

Justificativa: cada variável captura uma dimensão estrutural distinta:
  - Automação: escolha tecnológica do subsetor (Lakshmanan et al. 2020)
  - Capital humano: nível de qualificação/complexidade (Murphy 2022)
  - Exposição fiscal: dependência do incentivo tributario

Fonte de emprego: SUFRAMA (média mensal: efetiva + temporária + terceirizada).
Fonte de salários: SUFRAMA Tab 24 (salários + encargos + benefícios sociais).

Métodos de seleção de k (5 critérios):
  1. Cotovelo (WCSS — 2ª derivada)
  2. Silhouette Score — Kaufman & Rousseeuw (1990)
  3. Calinski-Harabasz Score — Calinski & Harabasz (1974)
  4. Davies-Bouldin Index — Davies & Bouldin (1979)
  5. Gap Statistic — Tibshirani, Walther & Hastie (2001)

Estabilidade: Bootstrap (B=100) com Adjusted Rand Index (ARI)

Decisão de k*: sem constraint artificial. Consenso dos 5 métodos.

Outputs:
  - outputs/tables/tab_kmeans_validation.csv   (todos os critérios)
  - outputs/tables/tab_gap_statistic.csv
  - outputs/tables/tab_bootstrap_stability.csv
  - outputs/tables/tab_perfil_clusters_v2.csv
  - outputs/figures/fig_validation_panel.png
  - outputs/figures/fig_clusters_2d_v2.png
  - outputs/figures/fig_clusters_radar_v2.png
  - data/processed/painel_com_cluster.csv
  - data/processed/subsetor_cluster_map.csv
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import (silhouette_score, calinski_harabasz_score,
                             davies_bouldin_score, adjusted_rand_score)
from sklearn.decomposition import PCA
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
TABLE_DIR = os.path.join(BASE_DIR, "outputs", "tables")
FIG_DIR = os.path.join(BASE_DIR, "outputs", "figures")
os.makedirs(TABLE_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

plt.rcParams.update({"figure.dpi": 150, "font.size": 10})
sns.set_style("whitegrid")

SEED = 42
K_RANGE = range(2, 9)
B_BOOT = 100  # bootstrap replications for stability


# ============================================================
# GAP STATISTIC — Tibshirani, Walther & Hastie (2001)
# ============================================================
def gap_statistic(X: np.ndarray, k_range: range, B: int = 50, seed: int = 42) -> pd.DataFrame:
    """
    Compute Gap Statistic for k in k_range.
    
    Gap(k) = E*[log W_k] - log W_k
    where E* is the expectation under a uniform reference distribution.
    
    Optimal k: smallest k such that Gap(k) >= Gap(k+1) - s_{k+1}
    where s_{k+1} is the standard error of the reference log W.
    """
    rng = np.random.RandomState(seed)
    n, p = X.shape
    
    # Bounding box for uniform reference
    mins = X.min(axis=0)
    maxs = X.max(axis=0)
    
    results = []
    for k in k_range:
        # Observed W_k
        km = KMeans(n_clusters=k, n_init=20, max_iter=500, random_state=seed)
        km.fit(X)
        W_k = km.inertia_
        log_W_k = np.log(W_k) if W_k > 0 else 0
        
        # Reference W_k (B uniform samples)
        ref_log_Ws = []
        for _ in range(B):
            X_ref = rng.uniform(low=mins, high=maxs, size=(n, p))
            km_ref = KMeans(n_clusters=k, n_init=10, max_iter=200, random_state=seed)
            km_ref.fit(X_ref)
            W_ref = km_ref.inertia_
            ref_log_Ws.append(np.log(W_ref) if W_ref > 0 else 0)
        
        E_log_W = np.mean(ref_log_Ws)
        sd_log_W = np.std(ref_log_Ws) * np.sqrt(1 + 1/B)  # Tibshirani correction
        gap = E_log_W - log_W_k
        
        results.append({
            "k": k,
            "log_W_k": log_W_k,
            "E_log_W_ref": E_log_W,
            "Gap": gap,
            "s_k": sd_log_W,
        })
    
    df = pd.DataFrame(results)
    
    # Optimal k: smallest k where Gap(k) >= Gap(k+1) - s(k+1)
    df["gap_criterion"] = False
    for i in range(len(df) - 1):
        if df.loc[i, "Gap"] >= df.loc[i+1, "Gap"] - df.loc[i+1, "s_k"]:
            df.loc[i, "gap_criterion"] = True
            break
    
    return df


# ============================================================
# BOOTSTRAP STABILITY — Adjusted Rand Index
# ============================================================
def bootstrap_stability(X: np.ndarray, k: int, B: int = 100, 
                        seed: int = 42) -> dict:
    """
    Assess cluster stability via bootstrap.
    For B bootstrap samples, compute ARI between:
      1. Labels from full data
      2. Labels from bootstrap sample (evaluated on full data)
    
    High mean ARI (> 0.8) → stable clusters.
    """
    rng = np.random.RandomState(seed)
    n = X.shape[0]
    
    # Reference labels from full data
    km_ref = KMeans(n_clusters=k, n_init=50, max_iter=500, random_state=seed)
    labels_ref = km_ref.fit_predict(X)
    
    ari_scores = []
    for b in range(B):
        # Bootstrap sample (with replacement)
        idx = rng.choice(n, size=n, replace=True)
        X_boot = X[idx]
        
        # Fit on bootstrap, predict on original data
        km_boot = KMeans(n_clusters=k, n_init=20, max_iter=300, random_state=seed + b)
        km_boot.fit(X_boot)
        labels_boot = km_boot.predict(X)
        
        ari = adjusted_rand_score(labels_ref, labels_boot)
        ari_scores.append(ari)
    
    return {
        "k": k,
        "mean_ari": np.mean(ari_scores),
        "std_ari": np.std(ari_scores),
        "min_ari": np.min(ari_scores),
        "q25_ari": np.percentile(ari_scores, 25),
        "median_ari": np.median(ari_scores),
        "q75_ari": np.percentile(ari_scores, 75),
    }


# ============================================================
# 1. CARREGAR E PREPARAR
# ============================================================
print("=" * 70)
print("  K-MEANS CLUSTERING v2 — TCC ZFM (validação rigorosa)")
print("=" * 70)

df = pd.read_csv(os.path.join(PROCESSED_DIR, "painel_subsetor_ano.csv"))
print(f"\nPainel: {df.shape[0]} obs, {df['subsetor'].nunique()} subsetores")

# 3 variáveis estruturais (cada uma captura uma dimensão distinta)
CLUSTER_VARS = ["automacao", "salario_medio", "incentivo_faturamento"]
LABELS_MAP = {
    "automacao": "K/L (automação)",
    "salario_medio": "W/L (capital humano)",
    "incentivo_faturamento": "I/Fat (exposição fiscal)",
}

# Use subsetor time-averaged means (cross-section) for clustering
print("\nUsando MÉDIAS POR SUBSETOR (cross-section) para clustering...")
sub_means = df.groupby("subsetor")[CLUSTER_VARS].mean().reset_index()
print(f"  N DMUs para clustering: {len(sub_means)}")

X_raw = sub_means[CLUSTER_VARS].values
subsetor_names = sub_means["subsetor"].values

# Handle NaN/Inf
if np.any(~np.isfinite(X_raw)):
    print("  ⚠️ Valores não finitos encontrados, substituindo por mediana...")
    for j in range(X_raw.shape[1]):
        col = X_raw[:, j]
        bad = ~np.isfinite(col)
        if bad.any():
            col[bad] = np.nanmedian(col[~bad])

# Standardize
scaler = StandardScaler()
X = scaler.fit_transform(X_raw)
print(f"  Variáveis padronizadas: shape {X.shape}")


# ============================================================
# 2. SELEÇÃO DE k — 5 MÉTODOS
# ============================================================
print("\n2. SELEÇÃO DE k (5 métodos)...")

# 2a. Internal validation metrics
results = []
for k in K_RANGE:
    km = KMeans(n_clusters=k, n_init=50, max_iter=500, random_state=SEED)
    labels = km.fit_predict(X)
    wcss = km.inertia_
    sil = silhouette_score(X, labels) if k > 1 else 0
    ch = calinski_harabasz_score(X, labels) if k > 1 else 0
    db = davies_bouldin_score(X, labels) if k > 1 else np.inf
    results.append({
        "k": k, "WCSS": wcss, "Silhouette": sil,
        "Calinski_Harabasz": ch, "Davies_Bouldin": db
    })
    print(f"  k={k}: WCSS={wcss:.2f}, Sil={sil:.3f}, CH={ch:.1f}, DB={db:.3f}")

df_k = pd.DataFrame(results)

# Elbow (max 2nd derivative of WCSS)
wcss_vals = df_k["WCSS"].values
diffs = -np.diff(wcss_vals)
diffs2 = np.diff(diffs)
elbow_k = int(df_k["k"].values[1 + np.argmax(diffs2)])

# Best by each criterion
best_sil_k = int(df_k.loc[df_k["Silhouette"].idxmax(), "k"])
best_ch_k = int(df_k.loc[df_k["Calinski_Harabasz"].idxmax(), "k"])
best_db_k = int(df_k.loc[df_k["Davies_Bouldin"].idxmin(), "k"])  # minimize DB

print(f"\n  Cotovelo (max curvatura):     k = {elbow_k}")
print(f"  Melhor Silhouette:            k = {best_sil_k}")
print(f"  Melhor Calinski-Harabasz:     k = {best_ch_k}")
print(f"  Melhor Davies-Bouldin (min):  k = {best_db_k}")

# 2b. Gap Statistic
print("\n  Calculando Gap Statistic (B=50 referências uniformes)...")
df_gap = gap_statistic(X, K_RANGE, B=50, seed=SEED)
gap_criterion_rows = df_gap[df_gap["gap_criterion"]]
best_gap_k = int(gap_criterion_rows["k"].values[0]) if len(gap_criterion_rows) > 0 else best_sil_k
print(f"  Melhor Gap Statistic:         k = {best_gap_k}")
print(df_gap[["k", "Gap", "s_k", "gap_criterion"]].to_string(index=False))

df_gap.to_csv(os.path.join(TABLE_DIR, "tab_gap_statistic.csv"), index=False)

# Merge gap into main table
df_k = df_k.merge(df_gap[["k", "Gap", "s_k"]], on="k", how="left")
df_k.to_csv(os.path.join(TABLE_DIR, "tab_kmeans_validation.csv"), index=False)


# ============================================================
# 3. CONSENSO E ESCOLHA DE k*
# ============================================================
print("\n3. CONSENSO PARA ESCOLHA DE k*...")

# Vote system: each method votes for its best k
votes = {
    "Elbow": elbow_k,
    "Silhouette": best_sil_k,
    "Calinski-Harabasz": best_ch_k,
    "Davies-Bouldin": best_db_k,
    "Gap Statistic": best_gap_k,
}

print("  Votos:")
for method, k in votes.items():
    print(f"    {method}: k = {k}")

# Count votes
from collections import Counter
vote_counts = Counter(votes.values())
K_STAR = vote_counts.most_common(1)[0][0]  # Most voted k
print(f"\n  ★ k* por consenso (maioria dos 5 métodos) = {K_STAR}")

# If tie, prefer silhouette (Kaufman & Rousseeuw, 1990 — gold standard)
if vote_counts.most_common(1)[0][1] == 1:
    print("  ⚠️ Sem consenso claro. Usando Silhouette como desempate.")
    K_STAR = best_sil_k
    print(f"  ★ k* final = {K_STAR}")


# ============================================================
# 4. BOOTSTRAP STABILITY ANALYSIS
# ============================================================
print(f"\n4. BOOTSTRAP STABILITY (B={B_BOOT}) para k ∈ {{K_STAR-1, K_STAR, K_STAR+1}}...")

stability_results = []
for k_test in range(max(2, K_STAR - 1), min(max(K_RANGE) + 1, K_STAR + 2)):
    res = bootstrap_stability(X, k_test, B=B_BOOT, seed=SEED)
    stability_results.append(res)
    print(f"  k={k_test}: ARI médio = {res['mean_ari']:.3f} ± {res['std_ari']:.3f} "
          f"(min={res['min_ari']:.3f}, mediana={res['median_ari']:.3f})")

df_stab = pd.DataFrame(stability_results)
df_stab.to_csv(os.path.join(TABLE_DIR, "tab_bootstrap_stability.csv"), index=False)

# Stability check: if ARI < 0.6, warn
k_star_ari = df_stab[df_stab["k"] == K_STAR]["mean_ari"].values[0]
if k_star_ari < 0.6:
    print(f"  ⚠️ ARI={k_star_ari:.3f} para k*={K_STAR} → estabilidade FRACA (< 0.6)")
    print("     Interpretação: clusters devem ser usados com cautela")
elif k_star_ari < 0.8:
    print(f"  ✓ ARI={k_star_ari:.3f} para k*={K_STAR} → estabilidade MODERADA (0.6-0.8)")
else:
    print(f"  ✅ ARI={k_star_ari:.3f} para k*={K_STAR} → estabilidade BOA (≥ 0.8)")


# ============================================================
# 5. K-MEANS FINAL
# ============================================================
print(f"\n5. K-MEANS FINAL (k={K_STAR})...")

km_final = KMeans(n_clusters=K_STAR, n_init=100, max_iter=1000, random_state=SEED)
cluster_labels = km_final.fit_predict(X)
sub_means["cluster"] = cluster_labels

# Sort clusters by mean automacao (ascending)
cluster_prod = sub_means.groupby("cluster")["automacao"].mean().sort_values()
cluster_rename = {old: new for new, old in enumerate(cluster_prod.index)}
sub_means["cluster"] = sub_means["cluster"].map(cluster_rename)
cluster_labels = sub_means["cluster"].values

print("\nComposição dos clusters:")
for c in sorted(sub_means["cluster"].unique()):
    members = sub_means[sub_means["cluster"] == c]["subsetor"].tolist()
    print(f"  Cluster {c} ({len(members)} subsetores): {', '.join(members)}")


# ============================================================
# 6. PERFIS DOS CLUSTERS
# ============================================================
print("\n6. PERFIS DOS CLUSTERS...")

centroids_orig = sub_means.groupby("cluster")[CLUSTER_VARS].mean()
centroids_orig.columns = [LABELS_MAP[v] for v in CLUSTER_VARS]

# Add size stats
extra = sub_means.merge(
    df.groupby("subsetor").agg(
        fat_mean=("faturamento_real2023", "mean"),
        emp_mean=("emprego", "mean"),
    ).reset_index(),
    on="subsetor"
)
cluster_extra = extra.groupby("cluster").agg(
    n_subsetores=("subsetor", "count"),
    fat_total_bi=("fat_mean", lambda x: x.sum() / 1e9),
    emp_total=("emp_mean", "sum"),
).round(1)

profile = pd.concat([centroids_orig, cluster_extra], axis=1)
print(profile.to_string())
profile.to_csv(os.path.join(TABLE_DIR, "tab_perfil_clusters_v2.csv"))


# ============================================================
# 7. FIGURAS
# ============================================================
print("\n7. GERANDO FIGURAS...")

colors_cluster = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00",
                   "#a65628", "#f781bf", "#999999"][:K_STAR]

# ---- 7.1 Validation Panel (4 subplots: Elbow, Silhouette, CH, DB + Gap) ----
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# Elbow
ax = axes[0, 0]
ax.plot(df_k["k"], df_k["WCSS"], "o-", color="steelblue", linewidth=2)
ax.axvline(K_STAR, color="red", linestyle="--", alpha=0.7, label=f"k*={K_STAR}")
ax.set_xlabel("k")
ax.set_ylabel("WCSS")
ax.set_title("(a) Método do Cotovelo")
ax.legend()
ax.set_xticks(list(K_RANGE))

# Silhouette
ax = axes[0, 1]
ax.plot(df_k["k"], df_k["Silhouette"], "o-", color="darkorange", linewidth=2)
ax.axvline(K_STAR, color="red", linestyle="--", alpha=0.7, label=f"k*={K_STAR}")
ax.set_xlabel("k")
ax.set_ylabel("Silhouette Score")
ax.set_title("(b) Silhouette (Kaufman & Rousseeuw 1990)")
ax.legend()
ax.set_xticks(list(K_RANGE))

# Calinski-Harabasz
ax = axes[0, 2]
ax.plot(df_k["k"], df_k["Calinski_Harabasz"], "o-", color="forestgreen", linewidth=2)
ax.axvline(K_STAR, color="red", linestyle="--", alpha=0.7, label=f"k*={K_STAR}")
ax.set_xlabel("k")
ax.set_ylabel("Calinski-Harabasz")
ax.set_title("(c) Calinski-Harabasz (1974)")
ax.legend()
ax.set_xticks(list(K_RANGE))

# Davies-Bouldin
ax = axes[1, 0]
ax.plot(df_k["k"], df_k["Davies_Bouldin"], "o-", color="purple", linewidth=2)
ax.axvline(K_STAR, color="red", linestyle="--", alpha=0.7, label=f"k*={K_STAR}")
ax.set_xlabel("k")
ax.set_ylabel("Davies-Bouldin Index")
ax.set_title("(d) Davies-Bouldin (1979) — menor = melhor")
ax.legend()
ax.set_xticks(list(K_RANGE))

# Gap Statistic
ax = axes[1, 1]
ax.errorbar(df_k["k"], df_k["Gap"], yerr=df_k["s_k"], fmt="o-", color="brown",
            linewidth=2, capsize=4, label="Gap ± s_k")
ax.axvline(K_STAR, color="red", linestyle="--", alpha=0.7, label=f"k*={K_STAR}")
ax.set_xlabel("k")
ax.set_ylabel("Gap Statistic")
ax.set_title("(e) Gap Statistic (Tibshirani et al. 2001)")
ax.legend()
ax.set_xticks(list(K_RANGE))

# Bootstrap ARI
ax = axes[1, 2]
if len(df_stab) > 0:
    ax.bar(df_stab["k"], df_stab["mean_ari"], yerr=df_stab["std_ari"],
           color=["red" if k == K_STAR else "gray" for k in df_stab["k"]],
           capsize=5, alpha=0.8)
    ax.axhline(0.8, color="green", linestyle="--", alpha=0.5, label="ARI = 0.8 (bom)")
    ax.axhline(0.6, color="orange", linestyle="--", alpha=0.5, label="ARI = 0.6 (mín.)")
    ax.set_xlabel("k")
    ax.set_ylabel("Adjusted Rand Index")
    ax.set_title(f"(f) Bootstrap Stability (B={B_BOOT})")
    ax.legend(fontsize=8)
    ax.set_xticks(df_stab["k"].values)

fig.suptitle(f"Validação do Número de Clusters — k* = {K_STAR}", fontsize=14, y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_validation_panel.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_validation_panel.png")

# ---- 7.2 Clusters em 2D (PCA) ----
pca = PCA(n_components=2, random_state=SEED)
X_pca = pca.fit_transform(X)
explained = pca.explained_variance_ratio_

fig, ax = plt.subplots(figsize=(10, 7))
for c in range(K_STAR):
    mask = cluster_labels == c
    ax.scatter(X_pca[mask, 0], X_pca[mask, 1],
               c=colors_cluster[c], label=f"Cluster {c}",
               s=80, alpha=0.8, edgecolors="white", linewidth=0.5)
    for idx in np.where(mask)[0]:
        name = subsetor_names[idx]
        short = name[:15] + "..." if len(name) > 18 else name
        ax.annotate(short, (X_pca[idx, 0], X_pca[idx, 1]),
                    textcoords="offset points", xytext=(5, 5),
                    fontsize=7, alpha=0.8)

ax.set_xlabel(f"PC1 ({explained[0]:.1%} da variância)")
ax.set_ylabel(f"PC2 ({explained[1]:.1%} da variância)")
ax.set_title(f"Projeção PCA dos Subsetores — {K_STAR} Clusters K-means")
ax.legend(loc="best")
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_clusters_2d_v2.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_clusters_2d_v2.png")

# ---- 7.3 Radar chart ----
angles = np.linspace(0, 2 * np.pi, len(CLUSTER_VARS), endpoint=False).tolist()
angles += angles[:1]

centroids_std = []
for c in range(K_STAR):
    mask = cluster_labels == c
    centroid = X[mask].mean(axis=0).tolist()
    centroid += centroid[:1]
    centroids_std.append(centroid)

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
for c in range(K_STAR):
    ax.plot(angles, centroids_std[c], "o-", color=colors_cluster[c],
            label=f"Cluster {c}", linewidth=2, markersize=6)
    ax.fill(angles, centroids_std[c], alpha=0.1, color=colors_cluster[c])

ax.set_thetagrids(np.degrees(angles[:-1]), [LABELS_MAP[v] for v in CLUSTER_VARS])
ax.set_title(f"Perfil dos {K_STAR} Clusters (valores padronizados)", y=1.08)
ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.0))
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_clusters_radar_v2.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_clusters_radar_v2.png")


# ============================================================
# 8. EXPORTAR PAINEL COM CLUSTER
# ============================================================
print("\n8. EXPORTANDO PAINEL COM CLUSTERS...")

cluster_map = dict(zip(sub_means["subsetor"], sub_means["cluster"]))
df["cluster"] = df["subsetor"].map(cluster_map)

outpath = os.path.join(PROCESSED_DIR, "painel_com_cluster.csv")
df.to_csv(outpath, index=False)
print(f"  ✅ {outpath}")

sub_cluster = sub_means[["subsetor", "cluster"]].sort_values(["cluster", "subsetor"])
sub_cluster.to_csv(os.path.join(PROCESSED_DIR, "subsetor_cluster_map.csv"), index=False)
print(f"  ✅ subsetor_cluster_map.csv")


# ============================================================
# 9. RESUMO FINAL
# ============================================================
print("\n" + "=" * 70)
print("  RESUMO K-MEANS v2")
print("=" * 70)

print(f"\n  k* = {K_STAR} (consenso de 5 métodos)")
print(f"  Silhouette = {silhouette_score(X, cluster_labels):.3f}")
print(f"  Calinski-Harabasz = {calinski_harabasz_score(X, cluster_labels):.1f}")
print(f"  Davies-Bouldin = {davies_bouldin_score(X, cluster_labels):.3f}")
print(f"  Bootstrap ARI = {k_star_ari:.3f}")

for c in sorted(sub_means["cluster"].unique()):
    members = sub_means[sub_means["cluster"] == c]["subsetor"].tolist()
    cm = sub_means[sub_means["cluster"] == c]
    print(f"\n  Cluster {c}: {len(members)} subsetores")
    print(f"    I/Fat={cm['incentivo_faturamento'].mean():.4f}  "
          f"K/L={cm['automacao'].mean():,.0f}  "
          f"W/L={cm['salario_medio'].mean():,.0f}")
    for m in members:
        print(f"      - {m}")

print("\n  Votos por método:")
for method, k in votes.items():
    marker = " ← consenso" if k == K_STAR else ""
    print(f"    {method}: k={k}{marker}")
