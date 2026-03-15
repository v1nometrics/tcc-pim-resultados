"""Update PIB municipal Manaus with real IBGE SIDRA APISIDRA data."""
import requests, csv, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "data", "raw", "pib_municipal_manaus.csv")

# PIB total (v37)
url = "https://apisidra.ibge.gov.br/values/t/5938/n6/1302603/v/37/p/2018,2019,2020,2021,2022,2023"
r = requests.get(url, timeout=30)
r.raise_for_status()
data = r.json()[1:]
pib = {int(d["D3C"]): int(d["V"]) for d in data}

# VAB industria (v517)
url2 = "https://apisidra.ibge.gov.br/values/t/5938/n6/1302603/v/517/p/2018,2019,2020,2021,2022,2023"
r2 = requests.get(url2, timeout=30)
r2.raise_for_status()
data2 = r2.json()[1:]
vab = {}
for d in data2:
    try:
        v = d["V"]
        vab[int(d["D3C"])] = int(v) if v and v not in ("...", "-") else ""
    except:
        vab[int(d["D3C"])] = ""

with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ano", "pib_manaus_mil_reais", "vab_industria_mil_reais"])
    for yr in range(2018, 2024):
        w.writerow([yr, pib.get(yr, ""), vab.get(yr, "")])

print("PIB atualizado com dados REAIS IBGE SIDRA T.5938:")
for yr in range(2018, 2024):
    v = vab.get(yr, "N/A")
    print(f"  {yr}: PIB={pib.get(yr):>15,}  VAB_ind={v}")
print(f"\nSalvo em: {OUT}")
