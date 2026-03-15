"""Quick peek at RAIS 2023 data for Manaus to understand structure."""
import csv

count = 0
manaus_count = 0
manaus_active = 0
cnae_sample = {}

with open('/tmp/rais_work/RAIS_VINC_PUB_NORTE.COMT', 'r', encoding='latin-1') as f:
    reader = csv.reader(f, delimiter=',')
    header = next(reader)

    col_map = {}
    for i, h in enumerate(header):
        h_clean = h.strip().strip('"')
        col_map[h_clean] = i

    # Debug: print all column names to find encoding issues
    print("=== ALL COLUMNS ===")
    for k, v in col_map.items():
        print(f"  [{v:2d}] '{k}'")

    # Find columns by partial match (encoding-safe)
    def find_col(pattern):
        for k, v in col_map.items():
            if pattern.lower() in k.lower():
                return v
        return -1

    idx_cnae = find_col('cnae 2.0 classe')
    idx_ativo = find_col('ativo 31/12')
    idx_mun = find_col('munic\xedpio - c')  # try raw latin1
    if idx_mun < 0:
        idx_mun = find_col('municipio - c')
    if idx_mun < 0:
        # Just find any "Município" column that's not "Trab"
        for k, v in col_map.items():
            if 'pio' in k.lower() and 'trab' not in k.lower() and 'digo' in k.lower():
                idx_mun = v
                break
    idx_subsetor = find_col('ibge subsetor')
    idx_cnae_sub = find_col('cnae 2.0 subclasse')

    print(f"\nidx_cnae={idx_cnae}, idx_ativo={idx_ativo}, idx_mun={idx_mun}, idx_subsetor={idx_subsetor}, idx_cnae_sub={idx_cnae_sub}")

    for row in reader:
        count += 1
        mun = row[idx_mun].strip().strip('"') if idx_mun < len(row) else ''
        if mun == '130260':  # Manaus
            manaus_count += 1
            ativo = row[idx_ativo].strip().strip('"')
            if ativo == '1':  # active on Dec 31
                manaus_active += 1
                cnae = row[idx_cnae].strip().strip('"')
                subsetor_ibge = row[idx_subsetor].strip().strip('"') if idx_subsetor < len(row) else ''
                key = (cnae, subsetor_ibge)
                cnae_sample[key] = cnae_sample.get(key, 0) + 1

print(f"\nTotal Norte records: {count:,}")
print(f"Manaus (130260) records: {manaus_count:,}")
print(f"Manaus active 31/12: {manaus_active:,}")
print(f"\nUnique CNAE classes in Manaus: {len(set(k[0] for k in cnae_sample))}")
print(f"Unique IBGE subsetor codes: {sorted(set(k[1] for k in cnae_sample))}")

print(f"\nTop 40 CNAE classes (active in Manaus, 2023):")
for (cnae, sub), n in sorted(cnae_sample.items(), key=lambda x: -x[1])[:40]:
    print(f"  CNAE {cnae:8s}  IBGE_Sub={sub:4s}  n={n:>7,}")

# Also show industrial CNAE (10-33) totals
print(f"\nIndustrial CNAE (Division 10-33) summary:")
ind_total = 0
ind_by_ibge = {}
for (cnae, sub), n in cnae_sample.items():
    try:
        div = int(cnae[:2])
        if 10 <= div <= 33:
            ind_total += n
            ind_by_ibge[sub] = ind_by_ibge.get(sub, 0) + n
    except ValueError:
        pass
print(f"  Total industrial workers (active 31/12 Manaus): {ind_total:,}")
print(f"  By IBGE Subsetor code:")
for sub, n in sorted(ind_by_ibge.items(), key=lambda x: -x[1]):
    print(f"    IBGE_Sub={sub:4s}  n={n:>7,}")
