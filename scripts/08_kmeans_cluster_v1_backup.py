"""
08_kmeans_cluster.py
Clusterização K-means dos subsetores do PIM.

Variáveis de entrada (padronizadas via StandardScaler):
  1. Automação (A = K/L = CAPEX / Emprego)
  2. Incentivo/VA (I/VA)
  3. Incentivo/Emprego (I/E)
  4. Porte — ln(CAPEX)

Etapas:
  1. Padronização (StandardScaler)
  2. Seleção de k  via Elbow, Silhouette, Calinski-Harabasz
  3. K-means final com k* escolhido
  4. Perfis dos clusters (centróides em escala original)
  5. Exporta painel com rótulo de cluster

Outputs:
  - outputs/tables/tab_elbow_silhouette.csv
  - outputs/tables/tab_perfil_clusters.csv
  - outputs/figures/fig_elbow_silhouette.png
  - outputs/figures/fig_clusters_2d.png (projeção PCA)
  - outputs/figures/fig_clusters_radar.png (radar chart dos centróides)
  - data/processed/painel_com_cluster.csv
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score
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

# ============================================================
# 1. CARREGAR E PREPARAR
# ============================================================
print("=" * 70)
print("  K-MEANS CLUSTERING — TCC ZFM")
print("=" * 70)

df = pd.read_csv(os.path.join(PROCESSED_DIR, "painel_subsetor_ano.csv"))
print(f"\nPainel: {df.shape[0]} obs, {df['subsetor'].nunique()} subsetores")

# Variables for clustering
CLUSTER_VARS = ["automacao", "incentivo_va", "incentivo_emprego", "porte_ln_capex"]
LABELS_MAP = {
    "automacao": "Automação (K/L)",
    "incentivo_va": "Incentivo/VA",
    "incentivo_emprego": "Incentivo/E",
    "porte_ln_capex": "ln(CAPEX)",
}

# ============================================================
# DECISION: USE SUBSETOR MEANS (cross-section) FOR CLUSTERING
# ============================================================
# Rationale: K-means groups DMUs (subsetores), not panel obs.
# We use the time-averaged profile of each subsetor.
# The cluster label is then applied to all years of that subsetor.
# This follows standard practice in DEA+clustering literature.

print("\nUsando MÉDIAS POR SUBSETOR (cross-section) para clustering...")
sub_means = df.groupby("subsetor")[CLUSTER_VARS].mean().reset_index()
print(f"  N DMUs para clustering: {len(sub_means)}")

X_raw = sub_means[CLUSTER_VARS].values
subsetor_names = sub_means["subsetor"].values

# Check for NaN/Inf
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
print(f"  Médias padronizadas: {X.mean(axis=0).round(6)}")
print(f"  Desvios padronizados: {X.std(axis=0).round(6)}")

# ============================================================
# 2. SELEÇÃO DE k
# ============================================================
print("\n2. SELEÇÃO DE k...")

results = []
for k in K_RANGE:
    km = KMeans(n_clusters=k, n_init=50, max_iter=500, random_state=SEED)
    labels = km.fit_predict(X)
    wcss = km.inertia_
    sil = silhouette_score(X, labels) if k > 1 else 0
    ch = calinski_harabasz_score(X, labels) if k > 1 else 0
    results.append({"k": k, "WCSS": wcss, "Silhouette": sil, "Calinski-Harabasz": ch})
    print(f"  k={k}: WCSS={wcss:.2f}, Silhouette={sil:.3f}, CH={ch:.1f}")

df_k = pd.DataFrame(results)
df_k.to_csv(os.path.join(TABLE_DIR, "tab_elbow_silhouette.csv"), index=False)

# Determine optimal k
# Heuristic: highest silhouette, with CH as tiebreaker
best_sil_k = df_k.loc[df_k["Silhouette"].idxmax(), "k"]
best_ch_k = df_k.loc[df_k["Calinski-Harabasz"].idxmax(), "k"]

# Also compute elbow (biggest WCSS drop)
wcss_vals = df_k["WCSS"].values
diffs = -np.diff(wcss_vals)  # drops
diffs2 = np.diff(diffs)  # acceleration
elbow_k = int(df_k["k"].values[1 + np.argmax(diffs2)])  # point of max curvature

print(f"\n  Melhor Silhouette: k={best_sil_k}")
print(f"  Melhor Calinski-Harabasz: k={best_ch_k}")
print(f"  Cotovelo (max curvatura): k={elbow_k}")

# ============================================================
# CHOOSE k*
# ============================================================
# Priority: silhouette > elbow > CH
# Literature expectation: 3-5 clusters
K_STAR = int(best_sil_k)
# If all methods agree on different k, prefer silhouette within [3,5]
if K_STAR < 3:
    K_STAR = max(3, elbow_k)
if K_STAR > 5:
    # Check if k=3 or k=4 have silhouette close to best
    sil_3 = df_k[df_k["k"] == 3]["Silhouette"].values[0] if 3 in df_k["k"].values else 0
    sil_4 = df_k[df_k["k"] == 4]["Silhouette"].values[0] if 4 in df_k["k"].values else 0
    best_sil = df_k["Silhouette"].max()
    if sil_3 > 0.8 * best_sil:
        K_STAR = 3
    elif sil_4 > 0.8 * best_sil:
        K_STAR = 4
    else:
        K_STAR = int(best_sil_k)

print(f"\n  ★ k* escolhido = {K_STAR}")

# ============================================================
# 3. K-MEANS FINAL
# ============================================================
print(f"\n3. K-MEANS FINAL (k={K_STAR})...")

km_final = KMeans(n_clusters=K_STAR, n_init=100, max_iter=1000, random_state=SEED)
cluster_labels = km_final.fit_predict(X)

sub_means["cluster"] = cluster_labels

# Sort clusters by mean automação (so cluster 0 = least automated)
cluster_automacao = sub_means.groupby("cluster")["automacao"].mean().sort_values()
cluster_rename = {old: new for new, old in enumerate(cluster_automacao.index)}
sub_means["cluster"] = sub_means["cluster"].map(cluster_rename)
cluster_labels = sub_means["cluster"].values

# Cluster names based on profile
print("\nComposição dos clusters:")
for c in sorted(sub_means["cluster"].unique()):
    members = sub_means[sub_means["cluster"] == c]["subsetor"].tolist()
    print(f"  Cluster {c} ({len(members)} subsetores): {', '.join(members)}")

# ============================================================
# 4. PERFIS DOS CLUSTERS (escala original)
# ============================================================
print("\n4. PERFIS DOS CLUSTERS...")

# Centroids in original scale
centroids_orig = sub_means.groupby("cluster")[CLUSTER_VARS].mean()
centroids_orig.columns = [LABELS_MAP[v] for v in CLUSTER_VARS]

# Also add size stats
extra = sub_means.merge(
    df.groupby("subsetor").agg(
        fat_mean=("faturamento_real2023", "mean"),
        emp_mean=("emprego_suframa", "mean"),
    ).reset_index(),
    on="subsetor"
)
cluster_extra = extra.groupby("cluster").agg(
    n_subsetores=("subsetor", "count"),
    fat_total_bi=("fat_mean", lambda x: x.sum() / 1e9),
    emp_total=("emp_mean", "sum"),
).round(1)

profile = pd.concat([centroids_orig, cluster_extra], axis=1)

# Format nicely
profile["Automação (K/L)"] = profile["Automação (K/L)"].map(lambda x: f"R${x:,.0f}")
profile["Incentivo/VA"] = profile["Incentivo/VA"].map(lambda x: f"{x:.2%}")
profile["Incentivo/E"] = profile["Incentivo/E"].map(lambda x: f"R${x:,.0f}")
profile["ln(CAPEX)"] = profile["ln(CAPEX)"].map(lambda x: f"{x:.1f}")
profile["fat_total_bi"] = profile["fat_total_bi"].map(lambda x: f"R${x:.1f}B")
profile["emp_total"] = profile["emp_total"].map(lambda x: f"{x:,.0f}")

print(profile.to_string())
profile.to_csv(os.path.join(TABLE_DIR, "tab_perfil_clusters.csv"))

# ============================================================
# 5. FIGURAS
# ============================================================
print("\n5. GERANDO FIGURAS...")

colors_cluster = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00"][:K_STAR]

# ---- 5.1 Elbow + Silhouette ----
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(df_k["k"], df_k["WCSS"], "o-", color="steelblue", linewidth=2)
ax1.axvline(K_STAR, color="red", linestyle="--", alpha=0.7, label=f"k*={K_STAR}")
ax1.set_xlabel("Número de clusters (k)")
ax1.set_ylabel("WCSS (Within-Cluster Sum of Squares)")
ax1.set_title("Método do Cotovelo")
ax1.legend()
ax1.set_xticks(list(K_RANGE))

ax2.plot(df_k["k"], df_k["Silhouette"], "o-", color="darkorange", linewidth=2)
ax2.axvline(K_STAR, color="red", linestyle="--", alpha=0.7, label=f"k*={K_STAR}")
ax2.set_xlabel("Número de clusters (k)")
ax2.set_ylabel("Coeficiente de Silhueta")
ax2.set_title("Método da Silhueta")
ax2.legend()
ax2.set_xticks(list(K_RANGE))

fig.suptitle("Seleção do Número Ótimo de Clusters", fontsize=13, y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_elbow_silhouette.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_elbow_silhouette.png")

# ---- 5.2 Clusters em 2D (PCA) ----
pca = PCA(n_components=2, random_state=SEED)
X_pca = pca.fit_transform(X)
explained = pca.explained_variance_ratio_

fig, ax = plt.subplots(figsize=(10, 7))
for c in range(K_STAR):
    mask = cluster_labels == c
    ax.scatter(X_pca[mask, 0], X_pca[mask, 1], 
               c=colors_cluster[c], label=f"Cluster {c}", 
               s=80, alpha=0.8, edgecolors="white", linewidth=0.5)
    # Label points
    for idx in np.where(mask)[0]:
        name = subsetor_names[idx]
        # Abbreviate long names
        short = name[:15] + "..." if len(name) > 18 else name
        ax.annotate(short, (X_pca[idx, 0], X_pca[idx, 1]),
                   textcoords="offset points", xytext=(5, 5),
                   fontsize=7, alpha=0.8)

ax.set_xlabel(f"PC1 ({explained[0]:.1%} da variância)")
ax.set_ylabel(f"PC2 ({explained[1]:.1%} da variância)")
ax.set_title(f"Projeção PCA dos Subsetores — {K_STAR} Clusters K-means")
ax.legend(loc="best")
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_clusters_2d.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_clusters_2d.png")

# ---- 5.3 Radar chart dos centróides ----
angles = np.linspace(0, 2 * np.pi, len(CLUSTER_VARS), endpoint=False).tolist()
angles += angles[:1]  # complete the circle

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
fig.savefig(os.path.join(FIG_DIR, "fig_clusters_radar.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_clusters_radar.png")

# ============================================================
# 6. EXPORTAR PAINEL COM CLUSTER
# ============================================================
print("\n6. EXPORTANDO PAINEL COM CLUSTERS...")

# Map cluster labels back to full panel (each subsetor gets its cluster)
cluster_map = dict(zip(sub_means["subsetor"], sub_means["cluster"]))
df["cluster"] = df["subsetor"].map(cluster_map)

outpath = os.path.join(PROCESSED_DIR, "painel_com_cluster.csv")
df.to_csv(outpath, index=False)
print(f"  ✅ {outpath}")

# Also save subsetor-cluster mapping
sub_cluster = sub_means[["subsetor", "cluster"]].sort_values(["cluster", "subsetor"])
sub_cluster.to_csv(os.path.join(PROCESSED_DIR, "subsetor_cluster_map.csv"), index=False)
print(f"  ✅ subsetor_cluster_map.csv")

# Final summary
print("\n" + "=" * 70)
print("  RESUMO K-MEANS")
print("=" * 70)
for c in sorted(sub_means["cluster"].unique()):
    members = sub_means[sub_means["cluster"] == c]["subsetor"].tolist()
    mean_a = sub_means[sub_means["cluster"] == c]["automacao"].mean()
    mean_iva = sub_means[sub_means["cluster"] == c]["incentivo_va"].mean()
    mean_ie = sub_means[sub_means["cluster"] == c]["incentivo_emprego"].mean()
    mean_ln = sub_means[sub_means["cluster"] == c]["porte_ln_capex"].mean()
    print(f"\nCluster {c}: {len(members)} subsetores")
    print(f"  K/L={mean_a:,.0f}  I/VA={mean_iva:.2%}  I/E={mean_ie:,.0f}  ln(K)={mean_ln:.1f}")
    for m in members:
        print(f"    - {m}")

print(f"\nSilhouette Score: {silhouette_score(X, cluster_labels):.3f}")
print(f"Calinski-Harabasz: {calinski_harabasz_score(X, cluster_labels):.1f}")
