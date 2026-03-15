"""Extract ALL industrial CNAE classes from RAIS 2023 for Manaus with counts.
Used to build the CNAE → SUFRAMA Subsetor crosswalk."""
import csv
import os

RAIS_FILE = '/tmp/rais_work/RAIS_VINC_PUB_NORTE.COMT'

cnae_counts = {}  # {cnae_classe: count_active_31_12}
cnae_ibge = {}    # {cnae_classe: ibge_subsetor}

with open(RAIS_FILE, 'r', encoding='latin-1') as f:
    reader = csv.reader(f, delimiter=',')
    header = next(reader)

    col_map = {h.strip().strip('"'): i for i, h in enumerate(header)}

    idx_cnae = col_map['CNAE 2.0 Classe - Código']
    idx_ativo = col_map['Ind Vínculo Ativo 31/12 - Código']
    idx_mun = col_map['Município - Código']
    idx_ibge = col_map['IBGE Subsetor - Código']

    for row in reader:
        mun = row[idx_mun].strip()
        if mun != '130260':
            continue
        ativo = row[idx_ativo].strip()
        if ativo != '1':
            continue
        cnae = row[idx_cnae].strip()
        try:
            div = int(cnae[:2])
        except ValueError:
            continue
        # Industrial = CNAE divisions 10–33
        if not (10 <= div <= 33):
            continue

        cnae_counts[cnae] = cnae_counts.get(cnae, 0) + 1
        cnae_ibge[cnae] = row[idx_ibge].strip()

print(f"Total industrial CNAE classes in Manaus: {len(cnae_counts)}")
print(f"Total industrial workers (active 31/12): {sum(cnae_counts.values()):,}")
print()

# CNAE 2.0 Division descriptions
div_names = {
    10: "Alimentos", 11: "Bebidas", 12: "Fumo", 13: "Têxteis",
    14: "Confecção/Vestuário", 15: "Couros/Calçados", 16: "Madeira",
    17: "Papel/Celulose", 18: "Impressão/Gravação", 19: "Coque/Petróleo",
    20: "Produtos Químicos", 21: "Farmoquímicos", 22: "Borracha/Plástico",
    23: "Min. não Metálicos", 24: "Metalurgia", 25: "Prod. Metal",
    26: "Equip. Informática/Eletrônicos", 27: "Equip. Elétricos",
    28: "Máquinas/Equipamentos", 29: "Veículos Automotores",
    30: "Outros Equip. Transporte", 31: "Móveis", 32: "Produtos Diversos",
    33: "Manutenção/Reparação",
}

# Print grouped by CNAE Division
by_div = {}
for cnae, n in cnae_counts.items():
    div = int(cnae[:2])
    if div not in by_div:
        by_div[div] = []
    by_div[div].append((cnae, n, cnae_ibge.get(cnae, '')))

print(f"{'Div':>3} {'Division Name':<35} {'Total':>7}  CNAE Classes")
print("-" * 100)
for div in sorted(by_div):
    classes = sorted(by_div[div], key=lambda x: -x[1])
    total = sum(x[1] for x in classes)
    detail = ", ".join(f"{c[0]}({c[1]:,})" for c in classes)
    print(f"{div:3d} {div_names.get(div, '?'):<35} {total:>7,}  {detail}")
