"""
02_suframa_extract.py
Extrai tabelas da SUFRAMA (pdftotext output) em DataFrames estruturados.
Tabelas extraídas:
  1. Investimentos (CAPEX) por subsetor — 2018-2023 (US$)
  2. Faturamento por subsetor — 2018-2023 (R$ nominais)
  3. Mão-de-obra por subsetor — 2018-2023 (pessoas, média mensal)
  4. ICMS restituído por subsetor — 2018-2023 (R$ nominais) → proxy de incentivo fiscal
  5. Aquisição de insumos por subsetor — derivada das tabelas individuais (11/23 subsetores)
  6. Salários, Encargos e Benefícios Sociais por subsetor — 2018-2023 (R$ 1.000)
     → proxy de capital humano (massa salarial por empregado)

Salva CSVs em data/raw/suframa_*.csv
"""

import re
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
TXT_FILE = os.path.join(RAW_DIR, "suframa_2018_2023.txt")

# Load the text file
with open(TXT_FILE, "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Loaded {len(lines)} lines from SUFRAMA text file")

# ============================================================
# HELPERS
# ============================================================

SUBSETOR_ALIASES = {
    "Eletroeletrônico": "Eletroeletrônico",
    "Eletroeletrônico(***)": "Eletroeletrônico",
    "Eletroeletrônico(*)": "Eletroeletrônico",
    "Bens de informática": "Bens de Informática",
    "Relojoeiro": "Relojoeiro",
    "Duas rodas": "Duas Rodas",
    "Termoplástico": "Termoplástico",
    "Bebidas": "Bebidas",
    "Metalúrgico": "Metalúrgico",
    "Mecânico": "Mecânico",
    "Madeireiro": "Madeireiro",
    "Papel e papelão": "Papel e Papelão",
    "Couros e similares": "Couros e Similares",
    "Químico": "Químico",
    "Químico(*)": "Químico",
    "Material de limpeza e velas": "Material de Limpeza e Velas",
    "Vestuário e calçados": "Vestuário e Calçados",
    "Produtos Alimentícios": "Produtos Alimentícios",
    "Editorial e gráfico": "Editorial e Gráfico",
    "Têxtil": "Têxtil",
    "Mineral não metálico": "Mineral Não Metálico",
    "Mobiliário": "Mobiliário",
    "Beneficiamento de borracha": "Beneficiamento de Borracha",
    "Ótico": "Ótico",
    "Brinquedos": "Brinquedos",
    "Isqueiros, canetas e barbeadores descartáveis": "Isqueiros, Canetas e Barbeadores",
    "Isqueiros, canetas e": "Isqueiros, Canetas e Barbeadores",
    "Naval": "Naval",
    "DIVERSOS": "Diversos",
    "DIVERSOS(**)": "Diversos",
}

ANOS = [2018, 2019, 2020, 2021, 2022, 2023]

def clean_number(s):
    """Converte string numérica com pontos de milhar e vírgulas para float."""
    if not s or s.strip() in ("-", "...", ""):
        return 0.0
    s = s.strip()
    # Remove dots as thousand separators (Brazilian format uses . for thousands)
    s = s.replace(".", "")
    # Replace comma with dot for decimal (if any)
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0

def normalize_subsetor(name):
    """Normaliza nome do subsetor."""
    name = name.strip()
    # Remove parenthetical markers
    for alias, canonical in SUBSETOR_ALIASES.items():
        if name.lower().startswith(alias.lower()):
            return canonical
    return name


# ============================================================
# 1. INVESTIMENTOS (CAPEX) POR SUBSETOR — US$ 1.00
# ============================================================
def extract_capex():
    """
    Tabela começa na linha 393 (0-indexed: 392).
    Formato: SUBSETORES | 2018 | 2019 | 2020 | 2021 | 2022 | 2023
    Valores em US$ com pontos como separador de milhar.
    """
    print("\n" + "=" * 60)
    print("1. EXTRAINDO INVESTIMENTOS (CAPEX) POR SUBSETOR")
    print("=" * 60)

    rows = []
    # Lines 397-449 approximately (0-indexed: 396-448)
    for i in range(396, 455):
        line = lines[i]
        # Skip empty, header, obs lines
        if not line.strip() or "TOTAIS" in line or "SUBSETORES" in line:
            if "TOTAIS" in line:
                # Parse total line too
                nums = re.findall(r'[\d.]+', line)
                if len(nums) >= 6:
                    rows.append({
                        "subsetor": "TOTAL",
                        **{str(ANOS[j]): clean_number(nums[j]) for j in range(6)}
                    })
            continue
        if "Obs." in line or "Fonte:" in line or "(*)" in line.strip()[:3]:
            continue

        # Try to parse: name followed by numbers
        # The format has subsetor name then 6 numbers separated by whitespace
        # Numbers have dots as thousand separators
        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) >= 2:
            name = parts[0].strip()
            nums = []
            for p in parts[1:]:
                p = p.strip()
                if p and re.match(r'^[\d.,]+$', p):
                    nums.append(clean_number(p))
            
            if len(nums) >= 6 and name not in ("TOTAL", ""):
                subsetor = normalize_subsetor(name)
                if subsetor and subsetor not in ("Sem subsetor(Polo)",):
                    rows.append({
                        "subsetor": subsetor,
                        **{str(ANOS[j]): nums[j] for j in range(6)}
                    })

    df = pd.DataFrame(rows)
    if not df.empty:
        # Melt to long format
        df_long = df.melt(id_vars=["subsetor"], var_name="ano", value_name="capex_usd")
        df_long["ano"] = df_long["ano"].astype(int)
        outpath = os.path.join(RAW_DIR, "suframa_capex_subsetor.csv")
        df_long.to_csv(outpath, index=False)
        print(f"✅ CAPEX salvo: {outpath} ({len(df_long)} linhas)")
        print(f"   Subsetores encontrados: {df_long['subsetor'].nunique()}")
        print(df.set_index("subsetor").to_string())
    else:
        print("⚠️ Nenhum dado de CAPEX extraído")
    
    return df


# ============================================================
# 2. FATURAMENTO POR SUBSETOR — R$ nominais
# ============================================================
def extract_faturamento():
    """
    Tabela começa na linha 1030 (0-indexed: 1029).
    Formato: SUBSETORES | valor1 %1 | valor2 %2 | ... para 6 anos
    Valores em R$ com pontos como separador de milhar.
    """
    print("\n" + "=" * 60)
    print("2. EXTRAINDO FATURAMENTO POR SUBSETOR (R$ nominais)")
    print("=" * 60)

    rows = []
    # Parse lines 1038-1089 approximately
    for i in range(1037, 1092):
        line = lines[i]
        if not line.strip() or "SUBSETORES" in line or "Valores" in line or "ANOS" in line:
            continue
        if "(*)" in line.strip()[:3] or "FONTE" in line or "Inclusive" in line:
            continue
        
        # Handle "Isqueiros..." which spans two lines
        if "descartáveis" in line.lower() and len(line.strip()) < 20:
            continue

        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) < 2:
            continue

        name = parts[0].strip()
        
        # Extract numbers from the remaining text
        num_text = ' '.join(parts[1:])
        
        # The PDF text format uses:
        #   - Dots as thousand separators in faturamento: 26.045.618.432
        #   - Commas as decimal separators in percentages: 27,65
        # Strategy: match tokens that are either faturamento or percentage,
        # then filter by type.
        # Match comma-containing tokens (percentages) and dot-only tokens (faturamento)
        tokens = re.findall(r'[\d.,]+', num_text)
        
        fat_values = []
        for tok in tokens:
            if ',' in tok:
                # This is a percentage (e.g., "27,65") — skip
                continue
            val = clean_number(tok)
            if val is not None:
                fat_values.append(val)
        
        if "TOTAIS" in line:
            if len(fat_values) >= 6:
                rows.append({
                    "subsetor": "TOTAL",
                    **{str(ANOS[j]): fat_values[j] for j in range(6)}
                })
            continue

        if len(fat_values) >= 6:
            subsetor = normalize_subsetor(name)
            if subsetor:
                rows.append({
                    "subsetor": subsetor,
                    **{str(ANOS[j]): fat_values[j] for j in range(6)}
                })

    df = pd.DataFrame(rows)
    if not df.empty:
        df_long = df.melt(id_vars=["subsetor"], var_name="ano", value_name="faturamento_brl")
        df_long["ano"] = df_long["ano"].astype(int)
        outpath = os.path.join(RAW_DIR, "suframa_faturamento_subsetor.csv")
        df_long.to_csv(outpath, index=False)
        print(f"✅ Faturamento salvo: {outpath} ({len(df_long)} linhas)")
        print(f"   Subsetores encontrados: {df_long['subsetor'].nunique()}")
        # Show wide format
        print(df.set_index("subsetor").to_string())
    else:
        print("⚠️ Nenhum dado de faturamento extraído")

    return df


# ============================================================
# 3. MÃO-DE-OBRA POR SUBSETOR — Média mensal
# ============================================================
def extract_mao_de_obra():
    """
    Tabela na linha 4388 (0-indexed: 4387).
    Formato: SUBSETORES | 2018 | 2019 | 2020 | 2021 | 2022 | 2023
    Valores inteiros (pessoas).
    """
    print("\n" + "=" * 60)
    print("3. EXTRAINDO MÃO-DE-OBRA POR SUBSETOR")
    print("=" * 60)

    rows = []
    for i in range(4392, 4426):
        line = lines[i]
        if not line.strip() or "SUBSETORES" in line or "ANOS" in line:
            continue
        if "(*)" in line.strip()[:3] or "Fonte:" in line or "Dados" in line.strip()[:5]:
            continue

        parts = re.split(r'\s{2,}', line.strip())
        if len(parts) < 2:
            continue

        name = parts[0].strip()

        # Extract numbers
        all_nums = []
        for p in parts[1:]:
            p = p.strip()
            if p == "-":
                all_nums.append(0)
            elif re.match(r'^[\d.,]+$', p):
                all_nums.append(clean_number(p))

        if "TOTAIS" in line:
            if len(all_nums) >= 6:
                rows.append({
                    "subsetor": "TOTAL",
                    **{str(ANOS[j]): int(all_nums[j]) for j in range(6)}
                })
            continue

        if len(all_nums) >= 6 and name not in ("Sem subsetor(Polo)",):
            subsetor = normalize_subsetor(name)
            if subsetor and "Sem subsetor" not in subsetor:
                rows.append({
                    "subsetor": subsetor,
                    **{str(ANOS[j]): int(all_nums[j]) for j in range(6)}
                })

    df = pd.DataFrame(rows)
    if not df.empty:
        df_long = df.melt(id_vars=["subsetor"], var_name="ano", value_name="emprego_suframa")
        df_long["ano"] = df_long["ano"].astype(int)
        outpath = os.path.join(RAW_DIR, "suframa_emprego_subsetor.csv")
        df_long.to_csv(outpath, index=False)
        print(f"✅ Mão-de-obra salvo: {outpath} ({len(df_long)} linhas)")
        print(f"   Subsetores encontrados: {df_long['subsetor'].nunique()}")
        print(df.set_index("subsetor").to_string())
    else:
        print("⚠️ Nenhum dado de mão-de-obra extraído")

    return df


# ============================================================
# 4. ICMS POR SUBSETOR — R$ nominais (Recolhido, Restituído, Devido)
# ============================================================
def extract_icms():
    """
    Tabelas de ICMS por ano (R$):
      2018: linha 4500
      2019: linha 4536
      2020: linha 4573
      2021: linha 4610
      2022: linha 4647
      2023: linha 4684
    Cada tabela tem ~30 linhas: SUBSETORES | ICMS Recolhido | ICMS Restituído | ICMS Devido
    """
    print("\n" + "=" * 60)
    print("4. EXTRAINDO ICMS POR SUBSETOR (R$ nominais)")
    print("=" * 60)

    icms_starts = {
        2018: 4499,  # 0-indexed
        2019: 4535,
        2020: 4572,
        2021: 4609,
        2022: 4646,
        2023: 4683,
    }

    all_rows = []
    for year, start in icms_starts.items():
        for i in range(start + 3, start + 32):
            if i >= len(lines):
                break
            line = lines[i]
            if not line.strip() or "SUBSETORES" in line or "Valores" in line or "SETOR" in line:
                continue
            if "OBS" in line or "Fonte:" in line or "Tributação" in line:
                continue
            if "ICMS" in line and ("Recolhido" in line or "Restituído" in line):
                continue

            parts = re.split(r'\s{2,}', line.strip())
            if len(parts) < 2:
                continue

            name = parts[0].strip()
            nums = []
            for p in parts[1:]:
                p = p.strip()
                if re.match(r'^[\d.,]+$', p):
                    nums.append(clean_number(p))
                elif p == "0" or p == "-":
                    nums.append(0.0)

            if "TOTAIS" in line:
                if len(nums) >= 3:
                    all_rows.append({
                        "ano": year,
                        "subsetor": "TOTAL",
                        "icms_recolhido": nums[0],
                        "icms_restituido": nums[1],
                        "icms_devido": nums[2],
                    })
                continue

            if len(nums) >= 3:
                subsetor = normalize_subsetor(name)
                if subsetor:
                    all_rows.append({
                        "ano": year,
                        "subsetor": subsetor,
                        "icms_recolhido": nums[0],
                        "icms_restituido": nums[1],
                        "icms_devido": nums[2],
                    })

    df = pd.DataFrame(all_rows)
    if not df.empty:
        outpath = os.path.join(RAW_DIR, "suframa_icms_subsetor.csv")
        df.to_csv(outpath, index=False)
        print(f"✅ ICMS salvo: {outpath} ({len(df)} linhas)")
        print(f"   Subsetores encontrados: {df['subsetor'].nunique()}")
        print(f"   Anos: {sorted(df['ano'].unique())}")
        # Summary pivot
        pivot = df[df["subsetor"] != "TOTAL"].pivot_table(
            index="subsetor", columns="ano", values="icms_restituido", aggfunc="sum"
        )
        print("\nICMS Restituído por subsetor (R$):")
        print(pivot.to_string())
    else:
        print("⚠️ Nenhum dado de ICMS extraído")

    return df


# ============================================================
# 5. INSUMOS POR SUBSETOR — Extrair das tabelas individuais
# ============================================================
def extract_insumos_subsetor():
    """
    Cada subsetor tem uma tabela individual com Aquisição de Insumos e Faturamento.
    Tabelas individuais começam na linha 509 (Eletroeletrônico).
    Vou extrair o total de insumos de cada tabela.
    
    A abordagem: encontrar cada header "AQUISIÇÃO DE INSUMOS E FATURAMENTO DO SUBSETOR X"
    e parsear os dados.
    """
    print("\n" + "=" * 60)
    print("5. EXTRAINDO INSUMOS POR SUBSETOR (R$ nominais)")
    print("=" * 60)

    # Find all individual subsetor table headers
    subsetor_tables = []
    for i, line in enumerate(lines):
        m = re.search(r'AQUISIÇÃO DE INSUMOS E FATURAMENTO DO SUBSETOR\s+(.*)', line)
        if m:
            subsetor_name = m.group(1).strip()
            # Clean up
            subsetor_name = re.sub(r'\(\*+\)', '', subsetor_name).strip()
            subsetor_tables.append((i, subsetor_name))

    print(f"Encontradas {len(subsetor_tables)} tabelas de subsetor")

    all_rows = []
    for idx, (start_line, raw_name) in enumerate(subsetor_tables):
        subsetor = normalize_subsetor(raw_name)
        
        # Each subsetor table has TWO blocks: R$ first, then US$.
        # We only want the R$ block. Detect "US$" marker to stop.
        in_brl_block = False
        
        for i in range(start_line + 2, min(start_line + 50, len(lines))):
            line = lines[i]
            stripped = line.strip()
            
            # Detect R$ block header
            if "R$ 1,00" in stripped or "R$1,00" in stripped:
                in_brl_block = True
                continue
            
            # Stop at US$ block header
            if "US$ 1,00" in stripped or "US$1,00" in stripped:
                break
            
            if not in_brl_block:
                continue
            
            # Look for year at the beginning
            year_match = re.match(r'^\s*(2018|2019|2020|2021|2022|2023)\b', stripped)
            if not year_match:
                continue
            
            year = int(year_match.group(1))
            
            # Extract all numbers from the line
            nums = re.findall(r'[\d.]+', stripped[4:])  # Skip the year
            float_nums = [clean_number(n) for n in nums]
            
            # Large numbers (>1000) are values, small (<100) are percentages
            # First large num = total insumos R$, second = total faturamento R$
            large_nums = [n for n in float_nums if n > 1000]
            
            if len(large_nums) >= 2:
                all_rows.append({
                    "ano": year,
                    "subsetor": subsetor,
                    "insumos_brl": large_nums[0],
                    "faturamento_check_brl": large_nums[1] if len(large_nums) >= 2 else None,
                })
            elif len(large_nums) == 1:
                all_rows.append({
                    "ano": year,
                    "subsetor": subsetor,
                    "insumos_brl": large_nums[0],
                    "faturamento_check_brl": None,
                })

    df = pd.DataFrame(all_rows)
    if not df.empty:
        outpath = os.path.join(RAW_DIR, "suframa_insumos_subsetor.csv")
        df.to_csv(outpath, index=False)
        print(f"✅ Insumos salvo: {outpath} ({len(df)} linhas)")
        print(f"   Subsetores encontrados: {df['subsetor'].nunique()}")
        print(f"   Anos: {sorted(df['ano'].unique())}")
        pivot = df.pivot_table(index="subsetor", columns="ano", values="insumos_brl", aggfunc="sum")
        print("\nInsumos por subsetor (R$):")
        print(pivot.to_string())
    else:
        print("⚠️ Nenhum dado de insumos extraído")

    return df


# ============================================================
# 6. SALÁRIOS, ENCARGOS E BENEFÍCIOS SOCIAIS POR SUBSETOR — R$ 1.000
# ============================================================
def extract_salarios():
    """
    Tab 24: SALÁRIOS, ENCARGOS E BENEFÍCIOS SOCIAIS × MÃO-DE-OBRA OCUPADA
    Bloco em R$ 1.000 (segundo bloco: linhas 3428–3680 do TXT).
    Uma tabela por ano (2018-2023).

    Colunas por tabela:
      (A) Salários, Encargos e Benefícios em R$ 1.000 (média mensal)
      (B) Mão-de-Obra Ocupada
      (C=A/B) Relação (custo salarial médio por trabalhador)

    Nota: "(*) Exceto mão-de-obra terceirizada e temporária" — refere-se à MdO
    desta tabela, não à tabela de Mão-de-Obra Ocupada (que inclui todos).
    A variável principal extraída é a massa salarial (A) × 1000 → R$ nominais.

    2018: 22 subsetores (sem "Couros e similares")
    2019-2023: 23 subsetores
    """
    print("\n" + "=" * 60)
    print("6. EXTRAINDO SALÁRIOS, ENCARGOS E BENEFÍCIOS POR SUBSETOR (R$ 1.000)")
    print("=" * 60)

    # Offsets 0-indexed para cada tabela anual (bloco R$)
    salarios_starts = {
        2018: 3427,   # linha 3428 (1-indexed)
        2019: 3468,   # linha 3469
        2020: 3510,   # linha 3511
        2021: 3552,   # linha 3553
        2022: 3594,   # linha 3595
        2023: 3636,   # linha 3637
    }

    all_rows = []
    for year, start in salarios_starts.items():
        row_count = 0
        for i in range(start + 7, start + 38):  # Cabeçalho ~7 linhas, dados ~26 linhas
            if i >= len(lines):
                break
            line = lines[i]
            stripped = line.strip()

            if not stripped:
                continue
            # Pular cabeçalhos e rodapés — nota: NÃO filtrar por "(*)" ou "(**)"
            # no meio da string, pois subsetores como "Eletroeletrônico(**)" os contêm.
            if any(kw in stripped for kw in ["SUBSETORES", "Valores", "Salários,",
                                              "Benefícios", "Média Mensal",
                                              "FONTE", "/ 113", "Mão-de-Obra Ocupada"]):
                continue
            if stripped.startswith("(A)") or stripped.startswith("(*)") or stripped.startswith("(**)"):
                continue
            if stripped.startswith("Relação"):
                continue

            # Extrair tokens: nome do subsetor + números
            # Formato: "Nome do subsetor                  123.456,7            1.234     5.678,90"
            # Números usam ponto como milhar, vírgula como decimal
            parts = re.split(r'\s{2,}', stripped)
            if len(parts) < 2:
                continue

            name = parts[0].strip()

            # Extrair números da parte restante
            nums = []
            for p in parts[1:]:
                p = p.strip()
                if re.match(r'^[\d.,]+$', p):
                    nums.append(clean_number(p))
                elif p == "-":
                    nums.append(0.0)

            is_total = "TOTAL" in name.upper() or "TOTAIS" in name.upper()

            if is_total:
                if len(nums) >= 1:
                    all_rows.append({
                        "ano": year,
                        "subsetor": "TOTAL",
                        "massa_salarial_mil": nums[0],
                        "mao_de_obra_check": int(nums[1]) if len(nums) >= 2 else None,
                        "salario_medio_check": nums[2] if len(nums) >= 3 else None,
                    })
                    row_count += 1
                continue

            if len(nums) >= 1:
                subsetor = normalize_subsetor(name)
                if subsetor and "Sem subsetor" not in subsetor:
                    all_rows.append({
                        "ano": year,
                        "subsetor": subsetor,
                        "massa_salarial_mil": nums[0],
                        "mao_de_obra_check": int(nums[1]) if len(nums) >= 2 else None,
                        "salario_medio_check": nums[2] if len(nums) >= 3 else None,
                    })
                    row_count += 1

        print(f"  {year}: {row_count} linhas extraídas")

    df = pd.DataFrame(all_rows)
    if not df.empty:
        # Converter de R$ 1.000 → R$ para consistência com as demais variáveis
        df["massa_salarial_brl"] = df["massa_salarial_mil"] * 1000

        outpath = os.path.join(RAW_DIR, "suframa_salarios_subsetor.csv")
        df[["ano", "subsetor", "massa_salarial_brl", "mao_de_obra_check", "salario_medio_check"]].to_csv(
            outpath, index=False
        )
        print(f"\n✅ Salários salvo: {outpath} ({len(df)} linhas)")
        print(f"   Subsetores encontrados: {df['subsetor'].nunique()}")
        print(f"   Anos: {sorted(df['ano'].unique())}")

        # Pivot para visualização
        pivot = df[df["subsetor"] != "TOTAL"].pivot_table(
            index="subsetor", columns="ano", values="massa_salarial_brl", aggfunc="sum"
        )
        print("\nMassa salarial por subsetor (R$ nominais):")
        print(pivot.round(0).to_string())
    else:
        print("⚠️ Nenhum dado de salários extraído")

    return df


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 70)
    print("  EXTRAÇÃO DE DADOS SUFRAMA — TCC ZFM")
    print("=" * 70)

    df_capex = extract_capex()
    df_fat = extract_faturamento()
    df_emp = extract_mao_de_obra()
    df_icms = extract_icms()
    df_insumos = extract_insumos_subsetor()
    df_salarios = extract_salarios()

    print("\n" + "=" * 70)
    print("  RESUMO DA EXTRAÇÃO")
    print("=" * 70)
    for nome, df in [("CAPEX", df_capex), ("Faturamento", df_fat), 
                     ("Emprego", df_emp), ("ICMS", df_icms), ("Insumos", df_insumos),
                     ("Salários", df_salarios)]:
        if df is not None and not df.empty:
            n_sub = df["subsetor"].nunique() - (1 if "TOTAL" in df["subsetor"].values else 0)
            print(f"  ✅ {nome}: {len(df)} linhas, {n_sub} subsetores")
        else:
            print(f"  ⚠️ {nome}: sem dados")
