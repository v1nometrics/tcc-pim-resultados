import pandas as pd

rows = [
    {"ano": 2018, "pib_manaus_mil_reais": 78155386, "vab_industria_mil_reais": 26393970},
    {"ano": 2019, "pib_manaus_mil_reais": 84566043, "vab_industria_mil_reais": 29810977},
    {"ano": 2020, "pib_manaus_mil_reais": 91773536, "vab_industria_mil_reais": 33271685},
    {"ano": 2021, "pib_manaus_mil_reais": 103281400, "vab_industria_mil_reais": 37697008},
]
ratio = 103281400 / 131531038  # Manaus/AM 2021
rows.append({"ano": 2022, "pib_manaus_mil_reais": round(145140465 * ratio), "vab_industria_mil_reais": None})
rows.append({"ano": 2023, "pib_manaus_mil_reais": round(161794976 * ratio), "vab_industria_mil_reais": None})

df = pd.DataFrame(rows)
outpath = "/Users/v1biu/Documents/UFPB/resultados/data/raw/pib_municipal_manaus.csv"
df.to_csv(outpath, index=False)
print(f"Saved: {outpath}")
print(df.to_string())
print(f"\nRatio Manaus/AM (2021): {ratio:.4f}")
print("NOTE: 2022-2023 estimated via 2021 ratio")
