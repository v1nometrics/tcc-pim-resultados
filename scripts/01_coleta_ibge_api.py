"""
01_coleta_ibge_api.py
Coleta IPCA (T.1737) e PIB Municipal (T.5938) via API SIDRA/IBGE.
Salva em data/raw/.
"""

import requests
import pandas as pd
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)

HEADERS = {"User-Agent": "TCC-UFPB-Vinicius/1.0"}

# ============================================================
# 1. IPCA — Tabela 1737 (Número-índice, dez/93=100)
# ============================================================
def coleta_ipca():
    """
    Coleta IPCA mensal (variável 2266 = número-índice) para Brasil, 2017-2023.
    2017 incluído para permitir deflacionamento de valores de 2018 (base dez anterior).
    """
    print("=" * 60)
    print("COLETANDO IPCA — SIDRA T.1737")
    print("=" * 60)

    # API SIDRA format:
    # /t/TABELA/n/NIVEL_GEOGRAFICO/v/VARIAVEL/p/PERIODOS/d/DECIMAIS
    url = (
        "https://apisidra.ibge.gov.br/values"
        "/t/1737"        # Tabela 1737 — IPCA
        "/n1/all"        # Brasil
        "/v/2266"        # Variável: número-índice (dez/93=100)
        "/p/201701-202312"  # Período mensal: jan/2017 a dez/2023
        "/d/v2266%205"   # 5 casas decimais
    )

    print(f"URL: {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=60)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"ERRO na API SIDRA (IPCA): {e}")
        # Tentar formato alternativo
        url_alt = (
            "https://servicodados.ibge.gov.br/api/v3/agregados/1737"
            "/periodos/201701-202312"
            "/variaveis/2266"
            "?localidades=N1[all]"
            "&classificacao="
        )
        print(f"Tentando URL alternativa: {url_alt}")
        try:
            resp = requests.get(url_alt, headers=HEADERS, timeout=60)
            resp.raise_for_status()
            data_alt = resp.json()
            # Parse formato v3
            results = data_alt[0]["resultados"][0]["series"][0]["serie"]
            rows = []
            for periodo, valor in results.items():
                rows.append({
                    "periodo": periodo,
                    "ano": int(periodo[:4]),
                    "mes": int(periodo[4:]),
                    "ipca_indice": float(valor) if valor and valor != "..." else None
                })
            df = pd.DataFrame(rows)
            outpath = os.path.join(RAW_DIR, "ipca_mensal_2017_2023.csv")
            df.to_csv(outpath, index=False)
            print(f"✅ IPCA salvo: {outpath} ({len(df)} linhas)")
            print(df.head(10))
            print("...")
            print(df.tail(5))

            # Criar tabela de deflator anual (média do ano / média de 2023)
            df_anual = df.groupby("ano")["ipca_indice"].mean().reset_index()
            df_anual.columns = ["ano", "ipca_medio_anual"]
            base_2023 = df_anual.loc[df_anual["ano"] == 2023, "ipca_medio_anual"].values[0]
            df_anual["deflator_2023"] = base_2023 / df_anual["ipca_medio_anual"]
            outpath2 = os.path.join(RAW_DIR, "deflator_anual_2023.csv")
            df_anual.to_csv(outpath2, index=False)
            print(f"\n✅ Deflator anual salvo: {outpath2}")
            print(df_anual)
            return df
        except Exception as e2:
            print(f"ERRO na API v3 (IPCA): {e2}")
            return None

    # Parse formato SIDRA (lista de dicts)
    if isinstance(data, list) and len(data) > 1:
        header = data[0]
        rows = []
        for row in data[1:]:
            periodo = row.get("D3C", "")
            valor = row.get("V", "")
            rows.append({
                "periodo": periodo,
                "ano": int(periodo[:4]) if len(periodo) >= 4 else None,
                "mes": int(periodo[4:]) if len(periodo) >= 6 else None,
                "ipca_indice": float(valor) if valor and valor != "..." and valor != "-" else None
            })
        df = pd.DataFrame(rows)
    else:
        print("Formato inesperado da resposta SIDRA.")
        print(json.dumps(data[:3] if isinstance(data, list) else data, indent=2, ensure_ascii=False))
        return None

    outpath = os.path.join(RAW_DIR, "ipca_mensal_2017_2023.csv")
    df.to_csv(outpath, index=False)
    print(f"✅ IPCA salvo: {outpath} ({len(df)} linhas)")
    print(df.head(10))

    # Deflator anual (base 2023)
    df_anual = df.groupby("ano")["ipca_indice"].mean().reset_index()
    df_anual.columns = ["ano", "ipca_medio_anual"]
    base_2023 = df_anual.loc[df_anual["ano"] == 2023, "ipca_medio_anual"].values[0]
    df_anual["deflator_2023"] = base_2023 / df_anual["ipca_medio_anual"]
    outpath2 = os.path.join(RAW_DIR, "deflator_anual_2023.csv")
    df_anual.to_csv(outpath2, index=False)
    print(f"\n✅ Deflator anual salvo: {outpath2}")
    print(df_anual)
    return df


# ============================================================
# 2. PIB Municipal — Tabela 5938
# ============================================================
def coleta_pib_municipal():
    """
    Coleta PIB Municipal de Manaus (código IBGE 1302603).
    Tabela 5938: PIB a preços correntes, VAB por setor, impostos.
    """
    print("\n" + "=" * 60)
    print("COLETANDO PIB MUNICIPAL MANAUS — SIDRA T.5938")
    print("=" * 60)

    # Tentar API v3
    url = (
        "https://servicodados.ibge.gov.br/api/v3/agregados/5938"
        "/periodos/2018|2019|2020|2021|2022|2023"
        "/variaveis/37|513|517|521|525|6575"
        "?localidades=N6[1302603]"
    )
    # Variáveis:
    # 37 = PIB a preços correntes
    # 513 = VAB Agropecuária
    # 517 = VAB Indústria
    # 521 = VAB Serviços (excl. admin pública)
    # 525 = VAB Administração pública
    # 6575 = Impostos líquidos

    print(f"URL: {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        rows = []
        for var in data:
            var_id = var["id"]
            var_nome = var["variavel"]
            for result in var["resultados"]:
                for serie in result["series"]:
                    municipio = serie["localidade"]["nome"]
                    for periodo, valor in serie["serie"].items():
                        rows.append({
                            "ano": int(periodo),
                            "municipio": municipio,
                            "variavel_id": var_id,
                            "variavel_nome": var_nome,
                            "valor_mil_reais": float(valor) if valor and valor != "..." and valor != "-" else None
                        })
        df = pd.DataFrame(rows)

        if df.empty:
            print("⚠️ DataFrame PIB Municipal vazio. Pode ser que 2022-2023 ainda não estejam disponíveis.")
            print("Resposta da API:")
            print(json.dumps(data[:2], indent=2, ensure_ascii=False)[:2000])
        else:
            outpath = os.path.join(RAW_DIR, "pib_municipal_manaus.csv")
            df.to_csv(outpath, index=False)
            print(f"✅ PIB Municipal salvo: {outpath} ({len(df)} linhas)")
            print(df.pivot_table(index="ano", columns="variavel_nome", values="valor_mil_reais"))

        return df

    except Exception as e:
        print(f"ERRO na API v3 (PIB Municipal): {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status: {e.response.status_code}")
            print(f"Resposta: {e.response.text[:1000]}")
        return None


# ============================================================
# 3. PIB Estadual do Amazonas (backup para PIB)
# ============================================================
def coleta_pib_estadual():
    """
    Backup: PIB do estado do Amazonas caso o municipal não tenha 2022-2023.
    Tabela 5938 nível estadual.
    """
    print("\n" + "=" * 60)
    print("COLETANDO PIB ESTADUAL AMAZONAS — SIDRA T.5938 (backup)")
    print("=" * 60)

    url = (
        "https://servicodados.ibge.gov.br/api/v3/agregados/5938"
        "/periodos/2018|2019|2020|2021|2022|2023"
        "/variaveis/37|517"
        "?localidades=N3[13]"  # UF 13 = Amazonas
    )

    print(f"URL: {url}")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        rows = []
        for var in data:
            var_id = var["id"]
            var_nome = var["variavel"]
            for result in var["resultados"]:
                for serie in result["series"]:
                    uf = serie["localidade"]["nome"]
                    for periodo, valor in serie["serie"].items():
                        rows.append({
                            "ano": int(periodo),
                            "uf": uf,
                            "variavel_id": var_id,
                            "variavel_nome": var_nome,
                            "valor_mil_reais": float(valor) if valor and valor != "..." and valor != "-" else None
                        })
        df = pd.DataFrame(rows)

        if not df.empty:
            outpath = os.path.join(RAW_DIR, "pib_estadual_amazonas.csv")
            df.to_csv(outpath, index=False)
            print(f"✅ PIB Estadual salvo: {outpath} ({len(df)} linhas)")
            print(df.pivot_table(index="ano", columns="variavel_nome", values="valor_mil_reais"))
        else:
            print("⚠️ PIB Estadual vazio.")

        return df

    except Exception as e:
        print(f"ERRO: {e}")
        return None


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("📊 COLETA DE DADOS IBGE — TCC ZFM")
    print("=" * 60)

    df_ipca = coleta_ipca()
    df_pib_mun = coleta_pib_municipal()
    df_pib_est = coleta_pib_estadual()

    print("\n" + "=" * 60)
    print("RESUMO DA COLETA")
    print("=" * 60)
    for nome, df in [("IPCA", df_ipca), ("PIB Municipal", df_pib_mun), ("PIB Estadual", df_pib_est)]:
        if df is not None and not df.empty:
            print(f"  ✅ {nome}: {len(df)} registros")
        else:
            print(f"  ⚠️ {nome}: sem dados ou falha na coleta")
