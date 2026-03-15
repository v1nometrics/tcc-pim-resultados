"""
07_descriptive_stats.py
Gera estatísticas descritivas e tabelas exploratórias para o TCC.
Outputs:
  - outputs/tables/tab_descritivas.csv (Tabela 1 — estatísticas descritivas)
  - outputs/tables/tab_media_subsetor.csv (Tabela 2 — médias por subsetor)
  - outputs/tables/tab_media_ano.csv (Tabela 3 — médias por ano)
  - outputs/tables/tab_correlacao.csv (Tabela 4 — correlações)
  - outputs/figures/fig_boxplot_vars.png (dispersão das variáveis-chave)
  - outputs/figures/fig_evolucao_temporal.png (séries temporais médias por ano)
  - outputs/figures/fig_heatmap_correlacao.png (heatmap de correlações)
  - outputs/figures/fig_scatter_matrix.png (scatter K-means inputs)
  - outputs/figures/fig_concentracao_pim.png (participação % no faturamento)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
TABLE_DIR = os.path.join(BASE_DIR, "outputs", "tables")
FIG_DIR = os.path.join(BASE_DIR, "outputs", "figures")
os.makedirs(TABLE_DIR, exist_ok=True)
os.makedirs(FIG_DIR, exist_ok=True)

# ============================================================
# CONFIG
# ============================================================
plt.rcParams.update({
    "figure.dpi": 150,
    "figure.figsize": (10, 6),
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
})
sns.set_style("whitegrid")

# ============================================================
# 1. CARREGAR PAINEL
# ============================================================
print("=" * 70)
print("  ESTATÍSTICAS DESCRITIVAS — TCC ZFM")
print("=" * 70)

df = pd.read_csv(os.path.join(PROCESSED_DIR, "painel_subsetor_ano.csv"))
print(f"\nPainel: {df.shape[0]} obs, {df['subsetor'].nunique()} subsetores, {sorted(df['ano'].unique())}")

# Key variables for analysis (v2 — sem VA)
KEY_VARS = [
    "faturamento_real2023",
    "emprego",
    "capex_real2023",
    "icms_restituido_real2023",
]

DERIVED_VARS = [
    "incentivo_faturamento",    # I/Fat
    "incentivo_emprego",        # I/E
    "produtividade_trabalho",   # Fat/E
    "automacao",                # K/L (CAPEX/Emprego)
    "salario_medio",            # W/L (Massa Salarial/Emprego)
]

# Nice labels for display
LABELS = {
    "faturamento_real2023": "Faturamento (R$ 2023)",
    "emprego": "Emprego SUFRAMA (média mensal)",
    "capex_real2023": "CAPEX (R$ 2023)",
    "icms_restituido_real2023": "ICMS Restituído (R$ 2023)",
    "incentivo_faturamento": "Incentivo/Faturamento",
    "incentivo_emprego": "Incentivo/Emprego",
    "produtividade_trabalho": "Produtividade (Fat/E)",
    "automacao": "Automação (K/L)",
    "salario_medio": "Salário Médio (W/L)",
}

# Unit multipliers for display (divide by these for table readability)
UNITS = {
    "faturamento_real2023": ("R$ milhões", 1e6),
    "emprego": ("pessoas", 1),
    "capex_real2023": ("R$ milhões", 1e6),
    "icms_restituido_real2023": ("R$ milhões", 1e6),
    "incentivo_faturamento": ("razão", 1),
    "incentivo_emprego": ("R$ mil/trabalhador", 1e3),
    "produtividade_trabalho": ("R$ mil/trabalhador", 1e3),
    "automacao": ("R$ mil/trabalhador", 1e3),
    "salario_medio": ("R$/trabalhador", 1),
}

# ============================================================
# 2. TABELA 1 — ESTATÍSTICAS DESCRITIVAS
# ============================================================
print("\n1. TABELA DESCRITIVA...")

all_vars = KEY_VARS + DERIVED_VARS
desc_raw = df[all_vars].describe().T

# Create a nicer table
tab1 = pd.DataFrame({
    "Variável": [LABELS[v] for v in all_vars],
    "Unidade": [UNITS[v][0] for v in all_vars],
    "N": desc_raw["count"].values.astype(int),
    "Média": [desc_raw.loc[v, "mean"] / UNITS[v][1] for v in all_vars],
    "D.P.": [desc_raw.loc[v, "std"] / UNITS[v][1] for v in all_vars],
    "Mín.": [desc_raw.loc[v, "min"] / UNITS[v][1] for v in all_vars],
    "P25": [desc_raw.loc[v, "25%"] / UNITS[v][1] for v in all_vars],
    "Mediana": [desc_raw.loc[v, "50%"] / UNITS[v][1] for v in all_vars],
    "P75": [desc_raw.loc[v, "75%"] / UNITS[v][1] for v in all_vars],
    "Máx.": [desc_raw.loc[v, "max"] / UNITS[v][1] for v in all_vars],
})
tab1 = tab1.round(2)
tab1.to_csv(os.path.join(TABLE_DIR, "tab_descritivas.csv"), index=False)
print(tab1.to_string(index=False))

# ============================================================
# 3. TABELA 2 — MÉDIAS POR SUBSETOR (painel médio 2018-2023)
# ============================================================
print("\n\n2. MÉDIAS POR SUBSETOR...")

sub_means = df.groupby("subsetor")[all_vars].mean()
# Convert units
tab2 = pd.DataFrame(index=sub_means.index)
tab2["Fat. (R$ mi)"] = sub_means["faturamento_real2023"] / 1e6
tab2["Emprego"] = sub_means["emprego"].round(0).astype(int)
tab2["CAPEX (R$ mi)"] = sub_means["capex_real2023"] / 1e6
tab2["ICMS Rest. (R$ mi)"] = sub_means["icms_restituido_real2023"] / 1e6
tab2["K/L (R$ mil)"] = sub_means["automacao"] / 1e3
tab2["W/L (R$)"] = sub_means["salario_medio"]
tab2["I/Fat"] = sub_means["incentivo_faturamento"]
tab2["I/E (R$ mil)"] = sub_means["incentivo_emprego"] / 1e3
tab2["Fat/E (R$ mil)"] = sub_means["produtividade_trabalho"] / 1e3
tab2 = tab2.round(2).sort_values("Fat. (R$ mi)", ascending=False)

tab2.to_csv(os.path.join(TABLE_DIR, "tab_media_subsetor.csv"))
print(tab2.to_string())

# Share of PIM total
tab2_share = pd.DataFrame(index=sub_means.index)
total_fat = sub_means["faturamento_real2023"].sum()
total_emp = sub_means["emprego"].sum()
total_capex = sub_means["capex_real2023"].sum()
total_inc = sub_means["icms_restituido_real2023"].sum()
tab2_share["% Fat."] = (sub_means["faturamento_real2023"] / total_fat * 100).round(1)
tab2_share["% Emprego"] = (sub_means["emprego"] / total_emp * 100).round(1)
tab2_share["% CAPEX"] = (sub_means["capex_real2023"] / total_capex * 100).round(1)
tab2_share["% ICMS Rest."] = (sub_means["icms_restituido_real2023"] / total_inc * 100).round(1)
tab2_share = tab2_share.sort_values("% Fat.", ascending=False)
print("\nParticipação (% do total PIM, média 2018-2023):")
print(tab2_share.to_string())

# ============================================================
# 4. TABELA 3 — EVOLUÇÃO TEMPORAL (MÉDIAS POR ANO)
# ============================================================
print("\n\n3. EVOLUÇÃO TEMPORAL...")

yr_means = df.groupby("ano")[KEY_VARS].sum()
tab3 = pd.DataFrame(index=yr_means.index)
tab3["Fat. Total (R$ bi)"] = yr_means["faturamento_real2023"] / 1e9
tab3["Emprego Total"] = yr_means["emprego"].round(0).astype(int)
tab3["CAPEX Total (R$ bi)"] = yr_means["capex_real2023"] / 1e9
tab3["ICMS Rest. Total (R$ bi)"] = yr_means["icms_restituido_real2023"] / 1e9
tab3 = tab3.round(2)
tab3.to_csv(os.path.join(TABLE_DIR, "tab_media_ano.csv"))
print(tab3.to_string())

# Growth rates
print("\nVariação anual (%):")
for col in tab3.columns:
    pct = tab3[col].pct_change() * 100
    print(f"  {col}: {[f'{v:+.1f}%' for v in pct.dropna()]}")

# ============================================================
# 5. TABELA 4 — CORRELAÇÕES
# ============================================================
print("\n\n4. CORRELAÇÕES...")

corr_vars = DERIVED_VARS + ["emprego"]
corr = df[corr_vars].corr()
corr_labels = [LABELS.get(v, v) for v in corr_vars]
corr.index = corr_labels
corr.columns = corr_labels
corr = corr.round(3)
corr.to_csv(os.path.join(TABLE_DIR, "tab_correlacao.csv"))
print(corr.to_string())

# ============================================================
# 6. FIGURAS
# ============================================================
print("\n\n5. GERANDO FIGURAS...")

# ---- 6.1 Boxplots das variáveis-chave (em log) ----
fig, axes = plt.subplots(1, 3, figsize=(12, 5))
boxplot_vars = [
    ("automacao", "Automação (K/L)\nR$/trabalhador"),
    ("salario_medio", "Salário Médio (W/L)\nR$/trabalhador"),
    ("incentivo_faturamento", "Incentivo/Faturamento\nrazão"),
]
for ax, (var, label) in zip(axes, boxplot_vars):
    data = df[var].dropna()
    ax.boxplot(data, vert=True)
    ax.set_title(label)
    ax.set_xticks([])
fig.suptitle("Distribuição das Variáveis Estruturais (K-means v3)", fontsize=13)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_boxplot_vars.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_boxplot_vars.png")

# ---- 6.2 Evolução temporal ----
fig, axes = plt.subplots(3, 3, figsize=(16, 12))
yr_agg = df.groupby("ano").agg({
    "faturamento_real2023": "sum",
    "emprego": "sum",
    "capex_real2023": "sum",
    "icms_restituido_real2023": "sum",
    "produtividade_trabalho": "mean",
    "automacao": "mean",
    "salario_medio": "mean",
}).reset_index()

plot_configs = [
    ("faturamento_real2023", "Faturamento Total\n(R$ bi 2023)", 1e9),
    ("emprego", "Emprego Total SUFRAMA\n(média mensal)", 1),
    ("capex_real2023", "CAPEX Total\n(R$ bi 2023)", 1e9),
    ("icms_restituido_real2023", "ICMS Restituído Total\n(R$ bi 2023)", 1e9),
    ("produtividade_trabalho", "Produtividade Média\n(Fat/E, R$/trab.)", 1),
    ("automacao", "Automação Média\n(K/L, R$/trab.)", 1),
    ("salario_medio", "Salário Médio\n(W/L, R$/trab.)", 1),
]

for ax, (var, title, div) in zip(axes.flat, plot_configs):
    vals = yr_agg[var] / div
    ax.plot(yr_agg["ano"], vals, "o-", linewidth=2, markersize=6, color="steelblue")
    ax.set_title(title)
    ax.set_xticks(yr_agg["ano"])
    ax.set_xticklabels([str(y) for y in yr_agg["ano"]], fontsize=8)
    ax.grid(True, alpha=0.3)
    # Annotate values
    for x, y in zip(yr_agg["ano"], vals):
        ax.annotate(f"{y:.1f}", (x, y), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=7)

# Hide unused subplots
for idx in range(len(plot_configs), len(axes.flat)):
    axes.flat[idx].set_visible(False)

fig.suptitle("Evolução do PIM — 2018 a 2023 (R$ constantes 2023)", fontsize=13, y=1.02)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_evolucao_temporal.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_evolucao_temporal.png")

# ---- 6.3 Heatmap de correlação ----
fig, ax = plt.subplots(figsize=(8, 6))
corr_num = df[corr_vars].corr()
mask = np.triu(np.ones_like(corr_num, dtype=bool), k=1)
sns.heatmap(corr_num, mask=mask, annot=True, fmt=".2f", cmap="RdBu_r",
            center=0, vmin=-1, vmax=1,
            xticklabels=[LABELS.get(v, v).split("(")[0].strip() for v in corr_vars],
            yticklabels=[LABELS.get(v, v).split("(")[0].strip() for v in corr_vars],
            ax=ax)
ax.set_title("Correlação entre Variáveis Estruturais e Emprego")
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_heatmap_correlacao.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_heatmap_correlacao.png")

# ---- 6.4 Scatter matrix das variáveis K-means (v3: 3 variáveis estruturais) ----
scatter_vars = ["automacao", "salario_medio", "incentivo_faturamento"]
fig, axes = plt.subplots(len(scatter_vars), len(scatter_vars), figsize=(10, 10))
for i, vi in enumerate(scatter_vars):
    for j, vj in enumerate(scatter_vars):
        ax = axes[i][j]
        if i == j:
            ax.hist(df[vi].dropna(), bins=15, color="steelblue", alpha=0.7, edgecolor="white")
        else:
            ax.scatter(df[vj], df[vi], alpha=0.4, s=12, color="steelblue")
        if i == len(scatter_vars) - 1:
            lbl = LABELS.get(vj, vj).split("(")[0].strip()
            ax.set_xlabel(lbl, fontsize=7)
        if j == 0:
            lbl = LABELS.get(vi, vi).split("(")[0].strip()
            ax.set_ylabel(lbl, fontsize=7)
        ax.tick_params(labelsize=6)

fig.suptitle("Scatter Matrix — Variáveis para K-means", fontsize=13, y=1.01)
fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_scatter_matrix.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_scatter_matrix.png")

# ---- 6.5 Concentração do PIM (participação no faturamento) ----
fig, ax = plt.subplots(figsize=(12, 6))
sub_fat = df.groupby("subsetor")["faturamento_real2023"].mean().sort_values(ascending=True)
sub_fat_pct = sub_fat / sub_fat.sum() * 100
colors = ["#2166ac" if v > 5 else "#b2182b" if v < 1 else "#67a9cf" for v in sub_fat_pct]
ax.barh(range(len(sub_fat_pct)), sub_fat_pct.values, color=colors, edgecolor="white")
ax.set_yticks(range(len(sub_fat_pct)))
ax.set_yticklabels(sub_fat_pct.index, fontsize=8)
ax.set_xlabel("% do Faturamento Total do PIM (média 2018-2023)")
ax.set_title("Concentração da Produção Industrial no PIM por Subsetor")

# Add percentage labels
for i, v in enumerate(sub_fat_pct.values):
    ax.text(v + 0.3, i, f"{v:.1f}%", va="center", fontsize=7)

# Add legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#2166ac", label="> 5% do PIM"),
    Patch(facecolor="#67a9cf", label="1-5% do PIM"),
    Patch(facecolor="#b2182b", label="< 1% do PIM"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=8)

fig.tight_layout()
fig.savefig(os.path.join(FIG_DIR, "fig_concentracao_pim.png"), bbox_inches="tight")
plt.close(fig)
print("  ✅ fig_concentracao_pim.png")

# ============================================================
# 7. DIAGNÓSTICOS
# ============================================================
print("\n\n6. DIAGNÓSTICOS...")

# Check for outliers (>3 std from mean)
print("\nOutliers (>3 D.P. da média):")
for var in all_vars:
    mean = df[var].mean()
    std = df[var].std()
    outliers = df[(df[var] > mean + 3*std) | (df[var] < mean - 3*std)]
    if len(outliers) > 0:
        for _, row in outliers.iterrows():
            print(f"  {LABELS.get(var, var)}: {row['subsetor']} ({row['ano']}) = {row[var]:.2e}")

# Check incentivo_faturamento > 1 (incentive exceeds faturamento — suspicious)
suspicious = df[df["incentivo_faturamento"] > 1]
if len(suspicious) > 0:
    print("\n⚠️ Incentivo/Faturamento > 1 (incentivo excede faturamento):")
    for _, row in suspicious.iterrows():
        print(f"  {row['subsetor']} ({row['ano']}): I/Fat = {row['incentivo_faturamento']:.2f}, "
              f"ICMS = R${row['icms_restituido_real2023']/1e6:.1f}M, Fat = R${row['faturamento_real2023']/1e6:.1f}M")

# Check zero faturamento
zero_fat = df[df["faturamento_real2023"] <= 0]
if len(zero_fat) > 0:
    print("\n⚠️ Faturamento zero ou negativo:")
    for _, row in zero_fat.iterrows():
        print(f"  {row['subsetor']} ({row['ano']}): Fat = R${row['faturamento_real2023']/1e6:.1f}M")

print("\n" + "=" * 70)
print("  DESCRITIVAS CONCLUÍDAS")
print("=" * 70)
