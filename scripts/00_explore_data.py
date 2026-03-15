#!/usr/bin/env python3
"""Explore all data sources for ZFM TCC."""
import openpyxl
import warnings
warnings.filterwarnings("ignore")

BASE = "/Users/v1biu/Documents/UFPB/resultados/DADOS"

# ============ 1. Receita Federal ============
print("=" * 80)
print("RECEITA FEDERAL - Q III (ZFM rows)")
print("=" * 80)
wb = openpyxl.load_workbook(
    f"{BASE}/Receita Federal/DGT Bases efetivas 2020 - série 2018 a 2023 - Quadros I a XXXII.xlsx",
    read_only=True, data_only=True
)
ws = wb['Q III']
for i, row in enumerate(ws.iter_rows(min_row=1, max_row=120, values_only=True)):
    vals = [str(v)[:70] if v else '' for v in row[:3]]
    if any(v for v in vals):
        print(f"R{i+1}: {vals}")

print("\n\n" + "=" * 80)
print("RECEITA FEDERAL - Q VII (por tributo - ZFM rows)")
print("=" * 80)
ws = wb['Q VII']
for i, row in enumerate(ws.iter_rows(min_row=1, max_row=248, values_only=True)):
    row_vals = list(row[:10])
    found = False
    for v in row_vals:
        if v and isinstance(v, str) and 'zona franca' in v.lower():
            found = True
            break
    if found or (i+1 in range(15, 20)):
        vals = [str(v)[:60] if v else '' for v in row_vals]
        print(f"R{i+1}: {vals}")

# Check all years - rows ~50-70 in Q III should be year 2 etc.
print("\n\nQ III structure - rows around 30-70 (year transitions)")
for i, row in enumerate(ws.iter_rows(min_row=1, max_row=5, values_only=True)):
    print(f"Q VII R{i+1}: {[str(v)[:50] if v else '' for v in row[:10]]}")

wb.close()

# ============ 2. ComexStat ============
print("\n\n" + "=" * 80)
print("COMEXSTAT")
print("=" * 80)
wb2 = openpyxl.load_workbook(
    f"{BASE}/ComexStat (Balança Comercial por Subsetor)/ComexStat (Balança Comercial por Subsetor).xlsx",
    read_only=True, data_only=True
)
print(f"Sheets: {wb2.sheetnames}")
for sname in wb2.sheetnames[:3]:
    ws2 = wb2[sname]
    print(f"\n--- {sname} (rows={ws2.max_row}, cols={ws2.max_column}) ---")
    for i, row in enumerate(ws2.iter_rows(min_row=1, max_row=15, values_only=True)):
        vals = [str(v)[:40] if v else '' for v in row[:15]]
        print(f"R{i+1}: {vals}")
wb2.close()

# ============ 3. RAIS sample (REMOVIDO v3 — RAIS descartada) ============
# A seção abaixo foi desativada: RAIS integralmente removida do projeto.
# Emprego agora vem da SUFRAMA (média mensal). Ver 06_build_panel.py.
# print("\n\n" + "=" * 80)
# print("RAIS 2023 - listing 7z contents")
# print("=" * 80)
# import py7zr
# import os
#
# rais_path = f"{BASE}/RAIS/2023/RAIS_VINC_PUB_NORTE.7z"
# with py7zr.SevenZipFile(rais_path, 'r') as z:
#     names = z.getnames()
#     print(f"Files inside: {names}")
#     for n in names:
#         print(f"  {n}")

print("\nDone exploring all data sources.")
