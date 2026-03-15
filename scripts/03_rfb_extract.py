"""
03_rfb_extract.py
Extrai dados de incentivos fiscais da ZFM do Excel da Receita Federal (DGT).
Arquivo: DGT Bases efetivas 2020 - série 2018 a 2023 - Quadros I a XXXII.xlsx

Objetivo: obter o total de gastos tributários da ZFM por tributo e ano (2018-2023).
Como os dados da RFB são AGREGADOS (não por subsetor), o rateio por subsetor 
será feito posteriormente usando dados da SUFRAMA (ICMS ou faturamento).

Salva em data/raw/rfb_*.csv
"""

import pandas as pd
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DADOS_DIR = os.path.join(BASE_DIR, "DADOS", "Receita Federal")

# Find the Excel file
excel_files = [f for f in os.listdir(DADOS_DIR) if f.endswith(".xlsx")]
if not excel_files:
    print("ERRO: Nenhum arquivo Excel encontrado em", DADOS_DIR)
    exit(1)

EXCEL_PATH = os.path.join(DADOS_DIR, excel_files[0])
print(f"Arquivo RFB: {EXCEL_PATH}")


# ============================================================
# 1. Explorar estrutura do Excel
# ============================================================
def explore_sheets():
    """Lista todas as abas e identifica as relevantes para ZFM."""
    xls = pd.ExcelFile(EXCEL_PATH)
    print(f"\nAbas encontradas ({len(xls.sheet_names)}):")
    
    relevant = []
    for sheet in xls.sheet_names:
        df = pd.read_excel(EXCEL_PATH, sheet_name=sheet, header=None, nrows=5)
        first_cell = str(df.iloc[0, 0]) if pd.notna(df.iloc[0, 0]) else ""
        print(f"  {sheet}: {first_cell[:80]}")
        
        # Check if ZFM is mentioned in this sheet
        df_full = pd.read_excel(EXCEL_PATH, sheet_name=sheet, header=None)
        has_zfm = df_full.apply(lambda col: col.astype(str).str.contains("ZFM|Zona Franca", case=False).any()).any()
        if has_zfm:
            relevant.append(sheet)
    
    print(f"\nAbas com dados ZFM: {relevant}")
    return relevant, xls


# ============================================================
# 2. Extrair Q III — Gastos tributários por função e modalidade
# ============================================================
def extract_q3(xls):
    """
    Q III tem gastos tributários por função orçamentária.
    ZFM aparece em múltiplas linhas (Agricultura, Comércio, Indústria).
    Colunas: Modalidade, 2018, 2019, 2020, 2021, 2022, 2023.
    """
    print("\n" + "=" * 60)
    print("EXTRAINDO Q III — Gastos por função orçamentária")
    print("=" * 60)
    
    df = pd.read_excel(EXCEL_PATH, sheet_name="Q III", header=None)
    
    # Find rows containing "ZFM" or "Zona Franca"
    zfm_rows = []
    for idx, row in df.iterrows():
        row_str = ' '.join([str(v) for v in row.values if pd.notna(v)])
        if re.search(r'ZFM|Zona Franca', row_str, re.IGNORECASE):
            zfm_rows.append(idx)
    
    print(f"Linhas com ZFM: {zfm_rows}")
    
    # Try to find year headers
    # Usually the first or second row has year columns
    for header_row in range(min(10, len(df))):
        row_vals = df.iloc[header_row].values
        has_years = sum(1 for v in row_vals if str(v).strip() in ['2018', '2019', '2020', '2021', '2022', '2023'])
        if has_years >= 4:
            print(f"Anos encontrados na linha {header_row}")
            break
    
    # Extract ZFM data
    results = []
    for idx in zfm_rows:
        row = df.iloc[idx]
        desc = str(row.iloc[0]) if pd.notna(row.iloc[0]) else ""
        if not desc:
            desc = str(row.iloc[1]) if pd.notna(row.iloc[1]) else ""
        
        # Get numeric values
        nums = []
        for v in row.values:
            if isinstance(v, (int, float)) and pd.notna(v) and v > 0:
                nums.append(v)
        
        if nums:
            results.append({
                "linha_excel": idx,
                "descricao": desc[:100],
                "valores": nums,
            })
            print(f"  Linha {idx}: {desc[:60]} → {len(nums)} valores")
    
    return results


# ============================================================
# 3. Extrair Q VII — Gastos por tributo
# ============================================================
def extract_q7(xls):
    """
    Q VII tem gastos tributários por tipo de tributo.
    ZFM aparece sob II, IPI, PIS/COFINS, IRPJ, etc.
    """
    print("\n" + "=" * 60)
    print("EXTRAINDO Q VII — Gastos por tributo")
    print("=" * 60)
    
    for sheet_name in ["Q VII", "Q VII REG"]:
        if sheet_name not in xls.sheet_names:
            continue
        
        df = pd.read_excel(EXCEL_PATH, sheet_name=sheet_name, header=None)
        print(f"\n--- {sheet_name} ({len(df)} linhas) ---")
        
        zfm_rows = []
        for idx, row in df.iterrows():
            row_str = ' '.join([str(v) for v in row.values if pd.notna(v)])
            if re.search(r'ZFM|Zona Franca', row_str, re.IGNORECASE):
                zfm_rows.append(idx)
        
        for idx in zfm_rows:
            row = df.iloc[idx]
            vals = [str(v)[:50] if pd.notna(v) else "" for v in row.values[:10]]
            print(f"  Linha {idx}: {' | '.join([v for v in vals if v])}")
    
    return True


# ============================================================
# 4. Extrair totais ZFM por ano (abordagem pragmática)
# ============================================================
def extract_zfm_totals():
    """
    Busca diretamente os totais da ZFM em todas as abas.
    A estratégia é: encontrar linhas marcadas como "Total" que estejam
    próximas a linhas ZFM, e extrair os valores anuais.
    """
    print("\n" + "=" * 60)
    print("EXTRAINDO TOTAIS ZFM POR ANO (todas as abas)")
    print("=" * 60)
    
    all_results = []
    xls = pd.ExcelFile(EXCEL_PATH)
    
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(EXCEL_PATH, sheet_name=sheet_name, header=None)
        
        for idx, row in df.iterrows():
            row_str = ' '.join([str(v) for v in row.values if pd.notna(v)])
            
            # Look for lines with "ZFM" or "Zona Franca de Manaus" and numeric values
            if re.search(r'ZFM|Zona Franca', row_str, re.IGNORECASE):
                # Collect numeric values from this row
                nums = []
                for col_idx, v in enumerate(row.values):
                    if isinstance(v, (int, float)) and pd.notna(v) and abs(v) > 0:
                        nums.append({"col": col_idx, "valor": v})
                
                if nums:
                    desc = ""
                    for v in row.values[:3]:
                        if isinstance(v, str) and len(v) > 2:
                            desc = v
                            break
                    
                    all_results.append({
                        "aba": sheet_name,
                        "linha": idx,
                        "descricao": desc[:100],
                        "n_valores": len(nums),
                        "valores": [n["valor"] for n in nums],
                    })
    
    # Show results organized
    if all_results:
        print(f"\nEncontrados {len(all_results)} registros ZFM:")
        for r in all_results:
            vals_str = ", ".join([f"{v:,.0f}" for v in r["valores"][:6]])
            print(f"  {r['aba']} L{r['linha']}: {r['descricao'][:50]} → [{vals_str}]")
        
        # Try to identify the main aggregated ZFM total
        # Usually in Q I or Q III as "Total ZFM" or similar
        for r in all_results:
            if len(r["valores"]) >= 6 and any(v > 1e9 for v in r["valores"]):
                desc = r["descricao"]
                print(f"\n  *** POSSÍVEL TOTAL ZFM: {r['aba']} L{r['linha']}: {desc}")
                for i, v in enumerate(r["valores"][:6]):
                    year = 2018 + i
                    print(f"      {year}: R$ {v:,.0f}")
    
    # Save all results
    rows_out = []
    for r in all_results:
        for i, v in enumerate(r["valores"]):
            rows_out.append({
                "aba": r["aba"],
                "linha": r["linha"],
                "descricao": r["descricao"],
                "col_idx": i,
                "valor": v,
            })
    
    df_out = pd.DataFrame(rows_out)
    if not df_out.empty:
        outpath = os.path.join(RAW_DIR, "rfb_zfm_all_rows.csv")
        df_out.to_csv(outpath, index=False)
        print(f"\n✅ Dados RFB ZFM salvos: {outpath} ({len(df_out)} linhas)")
    
    return all_results


# ============================================================
# 5. Extrair Q IV — Gastos por tributo (série temporal)
# ============================================================
def extract_q4():
    """Extrair Q IV que pode ter a série temporal por tributo."""
    print("\n" + "=" * 60)
    print("EXTRAINDO Q IV — Gastos por modalidade")
    print("=" * 60)
    
    for sheet in ["Q IV", "Q IV REG"]:
        try:
            df = pd.read_excel(EXCEL_PATH, sheet_name=sheet, header=None)
            print(f"\n--- {sheet} ({df.shape}) ---")
            for idx, row in df.iterrows():
                row_str = ' '.join([str(v) for v in row.values if pd.notna(v)])
                if re.search(r'ZFM|Zona Franca', row_str, re.IGNORECASE):
                    nums = [v for v in row.values if isinstance(v, (int, float)) and pd.notna(v) and abs(v) > 0]
                    desc = ""
                    for v in row.values[:3]:
                        if isinstance(v, str) and len(v) > 2:
                            desc = v
                            break
                    print(f"  L{idx}: {desc[:50]} → {[f'{n:,.0f}' for n in nums[:6]]}")
        except Exception as e:
            print(f"  Erro ao ler {sheet}: {e}")


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 70)
    print("  EXTRAÇÃO DE DADOS RFB (DGT) — INCENTIVOS FISCAIS ZFM")
    print("=" * 70)
    
    xls = pd.ExcelFile(EXCEL_PATH)
    print(f"Abas: {xls.sheet_names}")
    
    extract_q4()
    extract_q7(xls)
    results = extract_zfm_totals()
    
    print("\n" + "=" * 70)
    print("  CONCLUSÃO RFB")
    print("=" * 70)
    print("""
NOTA IMPORTANTE: Os dados da RFB (DGT) são AGREGADOS para toda a ZFM.
Não há desagregação por subsetor industrial.

Para construir o input 'Incentivo Fiscal (I)' por subsetor no modelo DEA,
usaremos o ICMS Restituído da SUFRAMA como proxy principal do benefício
fiscal usufruído por cada subsetor. O ICMS Restituído é:
  - Específico por subsetor (dados confirmados)
  - Proporcional ao benefício real usufruído
  - Coerente com a legislação (ICMS é o principal instrumento estadual da ZFM)

O total federal (II, IPI, PIS/COFINS) da RFB será usado para validação
e pode ser rateado proporcionalmente se necessário.
""")
