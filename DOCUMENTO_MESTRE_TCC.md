# DOCUMENTO MESTRE — TCC Vinícius Torres Nóbrega Gomes

## Eficiência Relativa e Alocação de Incentivos Fiscais na Zona Franca de Manaus: Uma Análise com DEA e Clusterização K-means

**Universidade Federal da Paraíba — Ciências Econômicas**

**Orientador:** Prof. Dr. Aléssio Tony Cavalcanti de Almeida


---

## 1. VISÃO GERAL DO PROJETO

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PIPELINE METODOLÓGICO                            │
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐      │
│  │  DADOS   │───▶│ K-MEANS  │───▶│ DEA-VRS  │───▶│MALMQUIST │      │
│  │  PAINEL  │    │ Cluster  │    │ por Clust│    │  PTF     │      │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘      │
│       │                                               │             │
│       │          ┌──────────┐    ┌──────────┐         │             │
│       └─────────▶│  META-   │───▶│ SIMAR-   │◀────────┘             │
│                  │ FRONTEIRA│    │ WILSON   │                       │
│                  └──────────┘    └──────────┘                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Pergunta de Pesquisa
> Como a heterogeneidade produtiva dos subsetores do PIM afeta a eficiência de conversão dos incentivos fiscais em faturamento e empregos ao longo de 2018-2023, e quais segmentos evidenciam maior ineficiência relativa no ano-base de 2023?

### Hipótese Central
> Hipótese original (pré-revisão): maior automação (A = CAPEX/E) → maior eficiência em faturamento, menor eficiência em emprego (trade-off).

### 1.3 Objetivo Geral e Objetivos Específicos (versão final operacional)

**Objetivo geral**

Avaliar a eficiência relativa dos subsetores do Polo Industrial de Manaus na conversão de incentivos fiscais em faturamento e emprego no período 2018-2023, identificando heterogeneidades estruturais e seus determinantes.

**Objetivos específicos**

1. Construir e auditar um painel subsetor-ano (2018-2023), com variáveis em preços reais de 2023 e documentação de regras de tratamento.
2. Identificar perfis produtivos homogêneos entre subsetores via clusterização K-means com validação interna e teste de estabilidade.
3. Estimar eficiência técnica relativa por DEA (VRS como modelo principal e CRS como comparação), incluindo leitura de eficiência de escala.
4. Mensurar dinâmica de produtividade por Índice de Malmquist e decompor variação em EC, TC, PEC e SC.
5. Estimar determinantes da eficiência por regressão truncada com bootstrap (Simar-Wilson), com robustez comparativa em OLS.
6. Integrar uma leitura ambiental interpretativa por subsetor (BCCAS), sem alterar a especificação do DEA principal.
7. Derivar implicações de política pública com foco em condicionalidade de incentivos, segmentação produtiva e limites de inferência do desenho empírico.

### 1.5 Estrutura do Trabalho (versão final operacional)

O trabalho está organizado em sete capítulos. O Capítulo 1 apresenta o problema, os objetivos e a delimitação do estudo. O Capítulo 2 desenvolve o referencial teórico sobre incentivos regionais, eficiência produtiva, DEA, produtividade dinâmica e determinantes de eficiência. O Capítulo 3 descreve dados, fontes e critérios de construção do painel. O Capítulo 4 detalha a estratégia metodológica integrada (K-means, DEA, metafronteira, Malmquist e Simar-Wilson). O Capítulo 5 reporta os resultados empíricos com base nas tabelas e figuras geradas. O Capítulo 6 discute os achados à luz da literatura, das implicações de política e das limitações do desenho. O Capítulo 7 conclui o estudo, responde à pergunta de pesquisa e apresenta agenda de pesquisa futura.

---

## 2. ESTRUTURA COMPLETA DO TCC (Capítulos & Seções)

### Elementos Pré-Textuais
| # | Elemento | Status | Responsável |
|---|----------|--------|-------------|
| 0.1 | Capa | ⬜ Não feito | Vinícius |
| 0.2 | Folha de rosto | ⬜ Não feito | Vinícius |
| 0.3 | Folha de aprovação | ⬜ Não feito | Vinícius |
| 0.4 | Dedicatória (opcional) | ⬜ Não feito | Vinícius |
| 0.5 | Agradecimentos | ⬜ Não feito | Vinícius |
| 0.6 | Epígrafe (opcional) | ⬜ Não feito | Vinícius |
| 0.7 | **RESUMO** (pt-BR, 150-500 palavras) | ⬜ Não feito | Vinícius+IA |
| 0.8 | **ABSTRACT** (inglês) | ⬜ Não feito | Vinícius+IA |
| 0.9 | Lista de Figuras | ⬜ Não feito | Automático |
| 0.10 | Lista de Tabelas | ⬜ Não feito | Automático |
| 0.11 | Lista de Quadros | ⬜ Não feito | Automático |
| 0.12 | Lista de Siglas e Abreviaturas | ⬜ Não feito | Vinícius+IA |
| 0.13 | Sumário | ⬜ Não feito | Automático |

### Capítulo 1 — INTRODUÇÃO
| # | Seção | Status | Observações |
|---|-------|--------|-------------|
| 1.0 | Contextualização geral | ✅ Escrito | Redundâncias a eliminar |
| 1.1 | Formulação do problema | ✅ Escrito | OK |
| 1.2 | Objetivo geral | ✅ Escrito | OK |
| 1.3 | **Objetivos específicos** | ✅ Definido | Consolidado na Seção 1.3 do Documento Mestre |
| 1.4 | Justificativa / Relevância | ✅ Implícito na intro | Separar como seção |
| 1.5 | Estrutura do trabalho | ✅ Definido | Consolidado na Seção 1.5 do Documento Mestre |

### Capítulo 2 — FUNDAMENTAÇÃO TEÓRICA
| # | Seção | Status | Observações |
|---|-------|--------|-------------|
| 2.1 | ZFM e incentivos fiscais (place-based) | ✅ Escrito | Remover achados empíricos → mover p/ cap. 3 |
| 2.2 | Eficiência produtiva e DEA | ✅ Escrito | Sólido |
| 2.3 | Clusterização — K-means | ✅ Escrito | Sólido |
| 2.4 | Interação entre segmentação e eficiência | ✅ Escrito | Redundante com cap. 4 — enxugar |

### Capítulo 3 — REVISÃO DE LITERATURA
| # | Seção | Status | Observações |
|---|-------|--------|-------------|
| 3.1 | DEA no PIM e ZFM (2010-2024) | ✅ Escrito | Quadro comparativo OK |
| 3.2 | K-means em contextos produtivos | ✅ Escrito | OK |
| 3.3 | Panorama da literatura sobre a ZFM | ✅ Escrito | OK |
| 3.4 | Lacunas e contribuição | ✅ Escrito | Redundante com intro — enxugar |

### Capítulo 4 — METODOLOGIA
| # | Seção | Status | Observações |
|---|-------|--------|-------------|
| 4.1 | Tipo e delineamento | ✅ Escrito | OK |
| 4.2 | Fontes, período e critérios | ✅ Escrito | OK |
| 4.3 | Construção e tratamento de variáveis | ✅ Escrito | OK |
| 4.4 | K-means: especificação | ✅ Escrito | OK |
| 4.5 | DEA-VRS: especificação | ✅ Escrito | OK |
| 4.6 | Índice de Malmquist | ✅ Escrito | OK |
| 4.7 | Metafronteira e TGR | ✅ Escrito | OK |
| 4.8 | Simar-Wilson (2ª etapa) | ✅ Escrito | OK |
| 4.9 | Robustez e software | ✅ Escrito | OK |

### Capítulo 5 — RESULTADOS
| # | Seção | Status | Observações |
|---|-------|--------|-------------|
| 5.1 | Estatísticas descritivas do painel 2018-2023 | 🔶 **DADOS PRONTOS** | 5 tabelas + 5 figuras geradas — falta redigir texto |
| 5.2 | Resultados da clusterização K-means | 🔶 **DADOS PRONTOS** | k*=3, Silhouette=0.501, perfis completos |
| 5.3 | Escores DEA-VRS por cluster e ano | 🔶 **DADOS PRONTOS** | VRS+CRS+escala, metafronteira TGR |
| 5.4 | Índice de Malmquist: decomposição catch-up vs. shift | 🔶 **DADOS PRONTOS** | M=0.831, EC=0.829, TC=1.003 |
| 5.5 | Metafronteira e TGR (entre clusters) | 🔶 **DADOS PRONTOS** | TGR: C0=1.00, C1=0.99, C2=0.72 |
| 5.6 | Determinantes da eficiência (Simar-Wilson) | 🔶 **DADOS PRONTOS** | B=2000 bootstrap, I/Fat, K/L, W/L, Cluster 2 significativos |

### Capítulo 6 — DISCUSSÃO
| # | Seção | Status | Observações |
|---|-------|--------|-------------|
| 6.1 | Interpretação à luz da fundamentação teórica | 🔄 Rascunho pronto | Consolidado em §22, pendente edição no texto final |
| 6.2 | Confronto com a literatura (Gouvêa, Fernandes, CPI) | 🔄 Rascunho pronto | Consolidado em §22, pendente edição no texto final |
| 6.3 | Implicações para política pública | 🔄 Rascunho pronto | Consolidado em §22, pendente edição no texto final |
| 6.4 | Limitações do estudo | 🔄 Rascunho pronto | Consolidado em §22, pendente edição no texto final |

### Capítulo 7 — CONCLUSÃO
| # | Seção | Status | Observações |
|---|-------|--------|-------------|
| 7.1 | Síntese dos achados | 🔄 Rascunho pronto | Consolidado em §22, pendente edição no texto final |
| 7.2 | Contribuições | 🔄 Rascunho pronto | Consolidado em §22, pendente edição no texto final |
| 7.3 | Sugestões de pesquisa futura | 🔄 Rascunho pronto | Consolidado em §22, pendente edição no texto final |

### Elementos Pós-Textuais
| # | Elemento | Status |
|---|----------|--------|
| R | Referências bibliográficas | 🔶 Parcial — precisa revisão ABNT |
| A | Apêndice A — Variáveis e Fontes de Dados | ⬜ Reescrever |
| B | Apêndice B — Código Python | ⬜ Não feito |
| C | Apêndice C — Tabelas completas de escores | ⬜ Não feito |

---

## 3. DMUs — SUBSETORES DO PIM (Unidades de Análise)

Conforme identificado nos Relatórios da SUFRAMA (2018-2023), os subsetores do PIM são:

| # | Subsetor | Código |
|---|----------|--------|
| 1 | Eletroeletrônico (inc. Bens de Informática) | ELET |
| 2 | Duas Rodas | DROD |
| 3 | Termoplástico | TERM |
| 4 | Químico | QUIM |
| 5 | Metalúrgico | META |
| 6 | Mecânico | MECA |
| 7 | Isqueiros, Canetas e Barbeadores Descartáveis | ISQU |
| 8 | Relojoeiro | RELO |
| 9 | Bebidas | BEBI |
| 10 | Papel e Papelão | PAPE |
| 11 | Ótico | OTIC |
| 12 | Produtos Alimentícios | ALIM |
| 13 | Beneficiamento de Borracha | BORR |
| 14 | Naval | NAVA |
| 15 | Mobiliário | MOBI |
| 16 | Mineral Não Metálico | MINE |
| 17 | Brinquedos | BRIN |
| 18 | Editorial e Gráfico | EDIT |
| 19 | Têxtil | TEXT |
| 20 | Madeireiro | MADE |
| 21 | Vestuário e Calçados | VEST |
| 22 | Couros e Similares | COUR |
| 23 | Material de Limpeza e Velas | LIMP |
| 24 | Diversos | DIVE |

**Nota:** "Bens de Informática" foi **consolidado** com Eletroeletrônico (dados de investimento/mão-de-obra já vem agregados). Couros e Similares (#22) não teve operação industrial em 2018 (faturamento=0, emprego=0, CAPEX=0) — **zero estrutural**, não dado faltante. A observação Couros-2018 é excluída do painel conforme critério de positividade DEA ($I > 0$, $Fat > 0$, $E > 0$). O subsetor permanece no painel com 5 anos (2019-2023).

**Total de DMUs:** **23 subsetores, painel ligeiramente desbalanceado: 137 observações** (22 sub × 6 anos + Couros × 5 anos). Material de Limpeza e Velas reintegrado com dados completos.

---

## 4. TABELA MESTRA DE VARIÁVEIS (Especificação Final)

| Variável | Símbolo | Papel no Modelo | Fonte | Unidade |
|----------|---------|-----------------|-------|---------|
| ICMS Restituído | $I$ | **Input 1 (DEA)** | SUFRAMA (ICMS por subsetor) | R$ constantes 2023 |
| CAPEX (Máq. e Equip.) | $K$ | **Input 2 (DEA)** | SUFRAMA (investimentos, USD→BRL via PTAX) | R$ constantes 2023 |
| Faturamento | $Fat$ | **Output 1 (DEA)** | SUFRAMA (faturamento por subsetor) | R$ constantes 2023 |
| Emprego Direto | $E$ | **Output 2 (DEA)** | **SUFRAMA** (mão-de-obra ocupada: efetiva + temporária + terceirizada, média mensal) | Pessoas |
| Automação | $K/L$ | **Cluster (K-means) + Simar-Wilson** | Calculada: CAPEX/Emprego | R$/pessoa |
| Salário Médio | $W/L$ | **Cluster (K-means) + Simar-Wilson** | SUFRAMA Tab 24: (Salários+Encargos+Benefícios)/Emprego | R$/pessoa |
| Incentivo/Faturamento | $I/Fat$ | **Cluster (K-means) + Simar-Wilson** | Calculada: ICMS/Faturamento | Razão |
| Cluster dummies | $D_c$ | **Determinante (Simar-Wilson)** | K-means (k* endógeno) | Dummy (0/1) |
| Tendência Temporal | $t$ | **Determinante (Simar-Wilson)** | Ano − 2020.5 (centrada) | Inteiro |
| COVID dummy | $D_{covid}$ | **Determinante (Simar-Wilson estendido)** | 1 se ano ∈ {2020, 2021} | Dummy |
| Massa Salarial | $W$ | **Intermediária** | SUFRAMA Tab 24: Salários, Encargos e Benefícios Sociais (R$ 1.000 × 1000) | R$ nominais |
| IPCA (Número-Índice) | $P_t$ | Deflacionamento | IBGE SIDRA T.1737 | Índice |
| PIB Manaus | $PIB_{MAN}$ | Controle (disponível) | IBGE SIDRA T.5938 (2018–2023) | R$ constantes 2023 |
| Câmbio PTAX | $e_t$ | Conversão USD→BRL (CAPEX) | BCB API PTAX | R$/USD |
| Incentivo Federal (rateio) | $I_{fed}$ | **Descritivo apenas (Tab. 1)** | RFB DGT Q XXVI + rateio ∝ Fat | R$ constantes 2023 |

**NOTA CRÍTICA — Especificação DEA Final:**
- **Inputs**: I (ICMS restituído) + K (CAPEX) — proxy de custo fiscal observado + investimento produtivo
- **Outputs**: Fat (Faturamento) + E (Emprego SUFRAMA) — resultados econômicos observados
- **Emprego**: Fonte = SUFRAMA (média mensal, inclui efetiva, temporária e terceirizada). Mesma fonte/universo que Faturamento, ICMS e CAPEX. Sem necessidade de crosswalk.
- **Justificativa SUFRAMA sobre RAIS**: (1) mesmo universo estatístico que os demais outputs (firmas incentivadas do PIM); (2) inclui terceirizados e temporários (RAIS só conta CLT diretos); (3) não exige crosswalk CNAE→Subsetor (elimina fricção taxonômica); (4) dado autoritativo da SUFRAMA. Ver §5.3 para discussão completa.
- **Justificativa VA→Faturamento**: VA eliminado — insumos disponíveis para apenas 11/23 subsetores. Faturamento validado por Gouvêa (2024), Bolognese (2024), Morais (2019), Fernandes (2019).
- **Rule of thumb**: n=23 ≥ 3×(2+2) = 12 ✔️ (Cooper, Seiford & Tone, 2007)
- **Uso dual do CAPEX**: Nível K no DEA (escala de investimento) vs. razão K/L no Simar-Wilson/K-means (densidade tecnológica). Construtos distintos (cf. Simar & Wilson 2007 — z_i devem ser razões, não níveis dos inputs/outputs).

### Diagrama de Papéis (Especificação Final)

```
                    CLUSTERIZAÇÃO (K-means, k* endógeno)
                    ┌──────────────────────┐
                    │  Variáveis Estruturais│
                    │  • K/L (automação)   │
                    │  • W/L (sal. médio)  │
                    │  • I/Fat (exposição) │
                    │  Validação: 5 métodos│
                    │  + Gap + bootstrap   │
                    └──────────┬───────────┘
                               │
                               ▼
           ┌───────────────────────────────────┐
           │  DEA-BCC (VRS) Output-Oriented    │
           │  Input 1:  I (ICMS restituído)    │
           │  Input 2:  K (CAPEX real)         │
           │  Output 1: Fat (Faturamento real) │
           │  Output 2: E (Emprego SUFRAMA)    │
           │  → Escore θ ∈ (0,1]               │
           └───────────────┬───────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        ┌──────────┐ ┌──────────┐ ┌───────────┐
        │MALMQUIST │ │  META-   │ │ SIMAR-    │
        │ CRS      │ │FRONTEIRA │ │ WILSON    │
        │ EC + TC  │ │  TGR     │ │ θ~f(I/Fat,│
        └──────────┘ └──────────┘ │ K/L,W/L,  │
                                  │ D,t,covid) │
                                  └───────────┘
```

---

## 5. MAPA DAS FONTES DE DADOS

### 5.1 SUFRAMA — Relatórios do PIM (PDFs)

| Arquivo | Período | Dados Extraíveis |
|---------|---------|-------------------|
| DESEMPENHO_PIM_2018-2023.pdf | 2018-2023 | ✅ Faturamento por subsetor; ✅ Investimentos (CAPEX) por subsetor; ✅ Mão-de-obra por subsetor; ✅ Aquisição de insumos por subsetor (11/23 sub); ✅ ICMS por subsetor; ✅ Salários, Encargos e Benefícios por subsetor |
| DESEMPENHO_PIM_2019-2024.pdf | 2019-2024 | Backup/validação cruzada |
| DESEMPENHO_PIM_2017-2022.pdf | 2017-2022 | Backup/validação cruzada |
| DESEMPENHO_PIM_2016-2021.pdf | 2016-2021 | Backup/validação cruzada |

**Decisao metodologica sobre VA:** O Valor Adicionado nao foi adotado no modelo principal, pois os dados de insumos estao disponiveis para apenas 11/23 subsetores. Assim, o Faturamento real foi utilizado diretamente como output DEA, em linha com a literatura aplicada (Gouvea 2024, Bolognese 2024, Morais 2019, Fernandes 2019).

### 5.2 Receita Federal — DGT (Excel)

| Arquivo | Conteúdo |
|---------|----------|
| DGT Bases efetivas 2020 - série 2018 a 2023 | 32 quadros de gastos tributários |

**Quadros relevantes para ZFM:**
- **Q III:** Gastos por função orçamentária e modalidade — ZFM aparece em Agricultura (R21), Comércio e Serviço (R57), Indústria (R116)
- **Q VII:** Gastos por tributo — ZFM no II (R17), IPI (R97), IRPJ (R109), PIS/COFINS (R153+)
- **Q VII (REG):** Gastos por tributo e região — ZFM com abertura regional

**Limitação CRÍTICA:** Os dados da RFB estão **agregados** para toda a ZFM, **não** desagregados por subsetor industrial (art. 198 CTN — sigilo fiscal). O incentivo fiscal $I$ por subsetor utiliza:
1. **(Adotado no DEA)** ICMS restituído da SUFRAMA — dado observado diretamente por subsetor
2. **(Apenas descritivo)** Rateio proporcional do total RFB pelo faturamento — $I_{fed}(s) = I_{total} \times Fat_s / \sum Fat$ — usado SOMENTE para tabela descritiva de custo fiscal. **NÃO entra no DEA** (circularidade: $I_{fed}/Fat = constante$ $\forall s$).

### 5.3 Emprego — Decisão SUFRAMA vs. RAIS

#### Decisão Final: SUFRAMA como fonte única de emprego

O emprego utilizado como **Output 2 do DEA** é extraído diretamente dos Cadernos de Indicadores da SUFRAMA (Tab 18: "Mão-de-Obra Ocupada"). O dado representa a **média mensal** de trabalhadores (efetiva + temporária + terceirizada) por subsetor, declarada pelas firmas com Projeto aprovado.

**Alternativa descartada:** Foi construído um crosswalk CNAE 2.0 → Subsetor SUFRAMA para extrair emprego da RAIS (estoque 31/12, MTE). O crosswalk envolveu 372 classes CNAE mapeadas em 4 níveis hierárquicos (Classe→Grupo→Divisão→Exclusão), com refinamentos (Div 33 excluída, padarias excluídas). Apesar de funcional, a abordagem RAIS foi **integralmente descartada** pelas seguintes razões:

| Critério | SUFRAMA | RAIS |
|----------|---------|------|
| **Universo** | Firmas incentivadas (mesmo das demais variáveis) | Todo emprego formal (inclui não-incentivados) |
| **Cobertura** | Efetiva + Temporária + Terceirizada | Apenas CLT diretos |
| **Crosswalk** | Desnecessário (subsetor nativo) | Exige CNAE→Subsetor (fricção taxonômica) |
| **Consistência** | Output provém da mesma fonte que Inputs | Output de fonte diferente dos Inputs |
| **Série** | Média mensal | ponto em 31/12 |

**Justificativa técnica:** Em DEA, todos os inputs e outputs devem compartilhar o **mesmo universo de referência** para que as razões de eficiência sejam interpretáveis. Se Faturamento, ICMS e CAPEX provêm de firmas incentivadas (SUFRAMA), o emprego também deve provir da mesma população. Caso contrário, o denominador (Output Emprego) e o numerador (Inputs ICMS+CAPEX) referem-se a populações estatísticas diferentes, violando a premissa de comparabilidade do DEA.

**O que foi removido:** Todos os scripts RAIS (`05_rais_extract.py`, `05b_cnae_crosswalk.py`, auxiliares), todos os dados brutos (RAIS 7z, ~1.2GB) e todos os artefatos intermediários (crosswalk CSV/MD, emprego RAIS CSV) foram integralmente excluídos do projeto.

### 5.3.1 Salários, Encargos e Benefícios Sociais (SUFRAMA Tab 24)

Variavel incorporada no modelo final: massa salarial extraida da Tab 24 do Caderno de Indicadores ("Salarios, Encargos e Beneficios Sociais x Mao-de-Obra Ocupada").

| Item | Detalhe |
|------|---------|
| **Tabela de origem** | Tab 24 (R$ 1.000), linhas 3428-3680 do TXT |
| **Cobertura** | 23-25 subsetores × 6 anos = 149 linhas |
| **Colunas extraídas** | (A) Massa salarial em R$ 1.000 (média mensal), (B) Mão-de-obra (check), (C=A/B) Relação |
| **Nota** | "(*) Exceto mão-de-obra terceirizada e temporária" refere-se à MdO *desta* tabela, não à Tab 18 |
| **Uso** | `salario_medio = massa_salarial_real2023 / emprego` → variável W/L para K-means e Simar-Wilson |
| **Spot check** | Eletroeletrônico 2023: R$ 247.697.400 ✓; TOTAL 2023: R$ 725.965.200 ✓ |

### 5.3.2 Aquisição de Insumos — Limitação Conhecida

Os dados de aquisição de insumos por subsetor estão disponíveis para apenas **11/23 subsetores** nos Cadernos de Indicadores. Essa limitação é estrutural da publicação SUFRAMA (os demais 12 subsetores não têm tabela individual de insumos no PDF).

| Item | Detalhe |
|------|---------|
| **Subsetores com dados** | 11: Eletroeletrônico, Duas Rodas, Mecânico, Metalúrgico, Químico, Termoplástico, Isqueiros, Papel e Papelão, Relojoeiro, Madeireiro, Ótico |
| **Total de linhas** | 66 (11 sub × 6 anos) — somente bloco R$, sem duplicação USD |
| **Ajuste de extração** | O parser detecta o marcador "R$ 1,00" antes de extrair e interrompe ao encontrar "US$ 1,00" (evita duplicacao BRL/USD) |
| **Consequência** | VA = Fat − Insumos inviável como variável DEA. Faturamento utilizado diretamente como Output 1. |
| **Mesma limitação em** | Bolognese (2024), Gouvêa (2024), Morais (2019) — nenhum resolveu insumos desagregados |

---

### 5.4 ComexStat (Complementar)

| Arquivo | Conteúdo |
|---------|----------|
| ComexStat.xlsx | Exportações de Manaus por SH4, mês, país (2018-2023) |

Uso: variável de controle ou contexto; não entra diretamente no modelo DEA.

### 5.5 IBGE — APIs

| Variável | API | Endpoint |
|----------|-----|----------|
| PIB Municipal Manaus | SIDRA T.5938 | `servicodados.ibge.gov.br/api/v3/agregados/5938/...` |
| IPCA (Número-Índice) | SIDRA T.1737 | `servicodados.ibge.gov.br/api/v3/agregados/1737/...` |

**Nota:** PIB Municipal disponível até 2023 na T.5938. Câmbio PTAX obtido via API do BCB (olinda.bcb.gov.br).

### 5.6 BCB — API PTAX (Câmbio)

| Variável | API | Endpoint |
|----------|-----|----------|
| Câmbio PTAX (venda, média anual) | BCB/Olinda | `olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarPeriodo` |

**Uso:** Conversao de CAPEX (reportado em USD pela SUFRAMA) para BRL com fonte oficial.

---

## 6. DECISÕES METODOLÓGICAS — RESOLVIDAS (Especificação Final)

| # | Decisão | Estado final adotado | Status |
|---|---------|----------------------|--------|
| D1 | Incentivo por subsetor | ICMS restituido no DEA; rateio federal apenas descritivo | ✅ |
| D2 | Eletroeletronico vs. Bens de Informatica | Consolidacao em uma unica DMU (Eletroeletronico) | ✅ |
| D3 | DMUs com dados incompletos | Couros 2018 tratado como zero estrutural (excluido por positividade); Limpeza reintegrado; painel final com 23 subsetores e 137 observacoes | ✅ |
| D4 | Metafronteira e segundo estagio | TGR + Simar-Wilson com bootstrap (B=2000) | ✅ |
| D5 | Outputs DEA | Faturamento real + Emprego SUFRAMA | ✅ |
| D6 | Inputs DEA | ICMS restituido real + CAPEX real | ✅ |
| D7 | K-means | k selecionado por validacao interna e regra de desempate por Silhouette | ✅ |
| D8 | Cambio | Conversao USD/BRL via API PTAX (BCB) | ✅ |
| D9 | PIB Manaus | Serie real via IBGE SIDRA T.5938 | ✅ |
| D10 | Incentivo federal agregado | Uso restrito a contexto descritivo (evita circularidade no DEA) | ✅ |
| D11 | Emprego (SUFRAMA vs RAIS) | SUFRAMA adotado como fonte unica para consistencia de universo estatistico | ✅ |
| D12 | Variaveis de clusterizacao | 3 razoes: K/L, W/L e I/Fat | ✅ |
| D13 | Regressores Simar-Wilson | ln(I/Fat), ln(K/L), ln(W/L), dummies de cluster e tendencia; extensao com COVID e scale_eff | ✅ |
| D14 | Salarios | Massa salarial da Tab 24 incorporada para construir W/L | ✅ |

---

## 7. CRONOGRAMA DETALHADO (4 SEMANAS)

### Semana 1: DADOS (01-07/mar)

| Dia | Tarefa | Checklist | Status |
|-----|--------|-----------|--------|
| 01/mar | Explorar todas as fontes de dados | ✅ | ✅ FEITO |
| 01/mar | Criar Documento Mestre | ✅ | ✅ FEITO |
| 01/mar | Instalar dependências Python | ✅ | ✅ FEITO |
| 01/mar | Coletar IPCA e PIB via API IBGE | ✅ | ✅ FEITO |
| 01/mar | Extrair dados SUFRAMA dos PDFs | ✅ | ✅ FEITO (6 datasets inc. Salários) |
| 01/mar | Processar RFB Excel (incentivos ZFM) | ✅ | ✅ FEITO (272 linhas) |
| 02/mar | Montar painel final: merge de todas as fontes | ✅ | ✅ FEITO (23 sub, 137 obs — painel desbalanceado, Couros 2018 excluído) |
| 02/mar | Deflacionar séries, calcular variáveis derivadas | ✅ | ✅ FEITO |
| 02/mar | Descompactar e extrair RAIS (6 anos) | ❌ | Não executado no modelo final (emprego SUFRAMA adotado) |
| 02/mar | Crosswalk CNAE→Subsetor PIM | ❌ | Não executado no modelo final |

### Semana 2: ANÁLISE (08-14/mar) — **CONCLUÍDA EM 02/mar** 🎉

| Dia | Tarefa | Status |
|-----|--------|--------|
| 02/mar | Estatísticas descritivas do painel (5 tabelas + 5 figuras) | ✅ FEITO |
| 02/mar | K-means: padronização, cotovelo, silhouette, k*=3 | ✅ FEITO |
| 02/mar | Perfilação dos clusters (centróides, radar, 2D scatter) | ✅ FEITO |
| 02/mar | DEA-VRS + CRS + eficiência de escala (HiGHS solver) | ✅ FEITO |
| 02/mar | Metafronteira + TGR por cluster | ✅ FEITO |
| 02/mar | Malmquist CRS: PTF por cluster, EC + TC | ✅ FEITO |
| 02/mar | Simar-Wilson: regressão truncada + bootstrap B=2000 | ✅ FEITO |

### Semana 3: ESCRITA RESULTADOS (15-21/mar)

| Dia | Tarefa | Status |
|-----|--------|--------|
| 15-16/mar | Escrever Cap. 5 — Resultados (estat. descritivas + clusters) | ⬜ |
| 16-17/mar | Escrever Cap. 5 — Resultados (DEA + Malmquist) | ⬜ |
| 17-18/mar | Escrever Cap. 5 — Resultados (metafronteira + Simar-Wilson) | ⬜ |
| 18-19/mar | Escrever Cap. 6 — Discussão | ⬜ |
| 19-20/mar | Escrever Cap. 7 — Conclusão | ⬜ |
| 20-21/mar | Revisar e eliminar redundâncias nos caps. 1-4 existentes | ⬜ |
| 21/mar | Criar objetivos específicos (seção 1.3) | ✅ FEITO (consolidado no mestre) |

### Semana 4: FINALIZAÇÃO (22-31/mar)

| Dia | Tarefa | Status |
|-----|--------|--------|
| 22-23/mar | Resumo e Abstract | ⬜ |
| 23-24/mar | Lista de siglas, lista de figuras/tabelas | ⬜ |
| 24-25/mar | Referências ABNT — revisão completa | ⬜ |
| 25-26/mar | Formatação UFPB/ABNT (margens, espaçamento, numeração) | ⬜ |
| 26-27/mar | Apêndices (crosswalk, código, tabelas completas) | ⬜ |
| 27-28/mar | Revisão integral do texto (coerência, ortografia, fluxo) | ⬜ |
| 29-30/mar | Revisão final com orientador | ⬜ |
| 31/mar | Entrega | ⬜ |

---

## 8. AJUSTES TEXTUAIS NO TEXTO EXISTENTE

### 8.1 Redundâncias a Eliminar

| Local | Problema | Ação |
|-------|----------|------|
| Intro (cap. 1) | Pipeline K-means→DEA→Malmquist descrito 3 vezes | Manter 1 menção concisa |
| Seção 2.4 | Repete quase toda a seção 4.1 | Enxugar para 1 página conceitual |
| Seção 3.4 | Repete lacunas já descritas na intro + 3.1.5 | Consolidar em 1 lugar |
| "Comparar iguais com iguais" | Aparece 8× no texto inteiro | Manter ≤2 ocorrências |
| "Vazamento de informação" | Aparece 5× quase textualmente | Manter 1 definição + remissões |

### 8.2 Seções a Criar

| Seção | Conteúdo | Extensão aprox. |
|-------|----------|-----------------|
| 1.3 Objetivos específicos | 7 itens mapeáveis ao pipeline final (já definidos no mestre) | ½ página |
| 1.5 Estrutura do trabalho | Parágrafo descrevendo capítulos (já definido no mestre) | ½ página |
| Cap. 5 Resultados | 6 subseções com tabelas e figuras | 15-20 páginas |
| Cap. 6 Discussão | 4 subseções | 5-8 páginas |
| Cap. 7 Conclusão | 3 subseções | 2-3 páginas |
| Resumo + Abstract | 150-500 palavras cada | 1 página cada |

### 8.3 Problemas de Fronteira entre Capítulos

| Trecho | Capítulo atual | Deveria estar em |
|--------|---------------|------------------|
| Achados de Holland et al., TCU, Banco Mundial, CPI | 2.1 (Fund. Teórica) | 3.3 (Revisão de Literatura) |
| Explicação detalhada do pipeline | 2.4 + 3.1.5 + 3.4 | 4.1 (Metodologia) |

### 8.4 Varredura de Consistência (executada em 14/03/2026)

Escopo da varredura: linguagem legada, alinhamento metodologico e coerencia entre secoes de status e secoes de conteudo.

| Item auditado | Resultado | Acao remanescente |
|---|---|---|
| Seção 1.3 (objetivos específicos) | ✅ Definida e integrada ao quadro de status | Nenhuma |
| Seção 1.5 (estrutura do trabalho) | ✅ Definida e integrada ao quadro de status | Nenhuma |
| Versionamento tecnico no corpo principal (`v1`, `v2`, `v3`) | ✅ Removido de trechos tese-facing | Manter somente em anexos tecnicos de auditoria |
| Blocos riscados e linguagem de rascunho | ✅ Eliminados das secoes principais | Nenhuma |
| Coerencia do nucleo metodologico (I,K -> Fat,E; K/L,W/L,I/Fat) | ✅ Uniformizado nas secoes centrais | Revisao final ao migrar para monografia oficial |
| Status de Cap. 6 e 7 | ✅ Atualizado para "rascunho pronto" | Converter rascunhos em texto final no documento da monografia |

Resultado operacional: o Documento Mestre esta coerente para servir como fonte unica de redacao dos capitulos finais.

### 8.5 Protocolo Cirurgico de Enxugamento (Cap. 2-4)

Objetivo: reduzir repeticao entre teoria, revisao e metodologia sem perda de rigor, preservando a sequencia logica pergunta -> dados -> metodo -> resultado.

| Origem | Acao | Destino recomendado | Criterio de corte |
|---|---|---|---|
| Cap. 2.4 (interacao entre segmentacao e eficiencia) | Manter apenas justificativa conceitual em 3-4 paragrafos | Cap. 2 (encerramento teorico) | Remover descricao operacional de pipeline e detalhes de estimacao |
| Cap. 3.4 (lacunas e contribuicao) | Consolidar em 1 secao curta (5-7 pontos) | Cap. 3 (fecho da revisao) | Eliminar repeticao de lacunas ja declaradas na introducao |
| Trechos de pipeline espalhados (2.4, 3.1.5, 3.4) | Unificar descricao tecnica | Cap. 4.1 (delineamento) | Manter uma unica versao do fluxo K-means -> DEA -> Metafronteira -> Malmquist -> SW |
| Trechos de policy em cap. teorico | Realocar para discussao | Cap. 6 | Em Cap. 2 manter teoria; em Cap. 6 manter implicacao aplicada |

Regra de aceitacao do enxugamento:

1. Cada conceito aparece uma vez como definicao principal.
2. Cada metodo aparece uma vez como especificacao principal.
3. Nao ha explicacao tecnica detalhada fora do Cap. 4.
4. Nao ha conclusao de politica fora dos Cap. 6-7.

Checklist rapido de edicao final (Cap. 2-4):

1. Cap. 2 com foco em conceitos e fundamentos (sem numeros de resultados).
2. Cap. 3 com foco em literatura e lacunas (sem formula de estimacao).
3. Cap. 4 com foco em especificacao, equacoes e criterios de inferencia.
4. Conferencia final de terminologia: I, K, Fat, E, K/L, W/L, I/Fat.

### 8.6 Textos-Substitutos (Cap. 2.4 e 3.4)

Uso: blocos curtos para substituir trechos redundantes sem perder coerencia metodologica.

**Texto sugerido para Cap. 2.4 (Interacao entre segmentacao e eficiencia):**

Neste estudo, a segmentacao setorial e tratada como etapa complementar a mensuracao de eficiencia relativa. A literatura de fronteiras nao parametricas indica que comparacoes entre unidades estruturalmente heterogeneas podem reduzir a interpretabilidade economica dos escores, sobretudo em amostras pequenas e com composicao setorial diversa. Por essa razao, a clusterizacao e empregada para identificar perfis produtivos comparaveis, enquanto a analise DEA mensura a eficiencia relativa de conversao de incentivos em resultados. A formalizacao operacional desse encadeamento analitico e apresentada no Capitulo 4, com especificacao completa de variaveis, equacoes e criterios de inferencia.

**Texto sugerido para Cap. 3.4 (Lacunas e contribuicao):**

A revisao evidencia tres lacunas centrais. Primeiro, a literatura aplicada ao PIM tende a analisar eficiencia sem segmentacao estrutural explicita entre subsetores. Segundo, os estudos raramente combinam leitura estatica de eficiencia e dinamica de produtividade no mesmo desenho empirico. Terceiro, o tratamento dos determinantes de eficiencia com inferencia robusta de segundo estagio ainda e limitado no contexto regional. Este trabalho contribui ao integrar segmentacao produtiva, DEA, metafronteira, Malmquist e regressao truncada com bootstrap em um mesmo painel setorial, preservando rastreabilidade empirica e limites de inferencia.

Regra de uso dos textos-substitutos:

1. Nao incluir numeros de resultados nesses paragrafos (reservar para Cap. 5 em diante).
2. Nao repetir descricao operacional de pipeline fora do Cap. 4.
3. Manter 1-2 paragrafos por secao para evitar inflacao textual.

### 8.7 Texto-Substituto (Cap. 4.1 — Tipo e Delineamento)

**Texto sugerido para Cap. 4.1:**

O delineamento empirico e observacional, quantitativo e aplicado, com painel subsetor-ano para o periodo 2018-2023. A estrategia metodologica integra cinco etapas complementares: (i) segmentacao estrutural por K-means; (ii) mensuracao de eficiencia relativa por DEA (VRS como modelo principal e CRS como comparacao de escala); (iii) avaliacao de lacuna tecnologica por metafronteira e TGR; (iv) dinamica de produtividade via indice de Malmquist com decomposicao em EC, TC, PEC e SC; e (v) analise de determinantes da eficiencia por regressao truncada com bootstrap (Simar-Wilson). O desenho privilegia comparabilidade interna entre subsetores, rastreabilidade de resultados e prudencia inferencial, sem pretensao de identificacao causal forte.

Regra de uso:

1. Este paragrafo substitui descricoes fragmentadas do pipeline em outras secoes.
2. Equacoes e detalhes de implementacao devem permanecer nas subsecoes metodologicas especificas.
3. Qualquer extensao metodologica fora do nucleo deve ser registrada como robustez complementar.

---

## 9. TABELAS E FIGURAS GERADAS (Cap. 5)

> **Todas as tabelas e figuras abaixo já foram geradas e estão em `outputs/tables/` e `outputs/figures/`.** Ver Seção 13.8 para inventário completo com mapeamento de uso no TCC.

### Tabelas Geradas (14 CSVs)

| ID | Título | Arquivo | Status |
|----|--------|---------|--------|
| T1 | Estatísticas descritivas do painel (N, média, dp, min, max) | tab_descritivas.csv | ✅ |
| T2 | Médias por subsetor | tab_media_subsetor.csv | ✅ |
| T3 | Médias por ano | tab_media_ano.csv | ✅ |
| T4 | Matriz de correlação | tab_correlacao.csv | ✅ |
| T5 | Validação K-means (5 métodos, k=2…8) | tab_kmeans_validation.csv | ✅ |
| T6 | Gap Statistic (k=2…8) | tab_gap_statistic.csv | ✅ |
| T7 | Bootstrap stability (ARI, k=2…8) | tab_bootstrap_stability.csv | ✅ |
| T8 | Perfil dos clusters (centróides modelo final) | tab_perfil_clusters_v2.csv | ✅ |
| T9 | Escores DEA-VRS — resumo por subsetor | tab_dea_summary.csv | ✅ |
| T10 | TGR — Technology Gap Ratio por cluster | tab_metafrontier_tgr.csv | ✅ |
| T11 | Malmquist — EC/TC/M por cluster e período | tab_malmquist_summary.csv | ✅ |
| T12 | Simar-Wilson — coeficientes + bootstrap IC | tab_simar_wilson.csv | ✅ |
| T13 | Robustez OLS + modelo estendido | tab_tobit_comparison.csv | ✅ |
| T14 | Custo fiscal total por subsetor | tab_custo_fiscal_total.csv | ✅ |

### Figuras Geradas (17 PNGs)

| ID | Título | Arquivo | Status |
|----|--------|---------|--------|
| F1 | Boxplots das variáveis-chave | fig_boxplot_vars.png | ✅ |
| F2 | Evolução temporal do PIM | fig_evolucao_temporal.png | ✅ |
| F3 | Heatmap de correlação | fig_heatmap_correlacao.png | ✅ |
| F4 | Scatter matrix | fig_scatter_matrix.png | ✅ |
| F5 | Concentração do faturamento PIM | fig_concentracao_pim.png | ✅ |
| F6 | Painel de validação K-means (5 métricas) | fig_validation_panel.png | ✅ |
| F7 | Clusters 2D (scatter PCA) | fig_clusters_2d_v2.png | ✅ |
| F8 | Radar dos clusters | fig_clusters_radar_v2.png | ✅ |
| F9 | Escores DEA por subsetor | fig_dea_scores.png | ✅ |
| F10 | Boxplot DEA por cluster | fig_dea_by_cluster.png | ✅ |
| F11 | Scatter da fronteira | fig_frontier_scatter.png | ✅ |
| F12 | Eficiência vs. variáveis contextuais | fig_eff_vs_contextual.png | ✅ |
| F13 | Evolução TGR por cluster | fig_tgr_evolution.png | ✅ |
| F14 | Decomposição Malmquist | fig_malmquist_decomp.png | ✅ |
| F15 | EC vs. TC por DMU | fig_malmquist_ec_tc.png | ✅ |
| F16 | Evolução temporal Malmquist | fig_malmquist_evolution.png | ✅ |
| F17 | Coeficientes Simar-Wilson (IC bootstrap) | fig_simar_wilson_coefs.png | ✅ |

---

## 10. SCRIPTS PYTHON — ESTRUTURA ATUALIZADA (Modelo Final)

```
resultados/
├── DOCUMENTO_MESTRE_TCC.md          ← ESTE ARQUIVO
├── scripts/
│   ├── 00_explore_data.py           ✅ Exploração inicial das fontes
│   ├── 01_coleta_ibge_api.py        ✅ IPCA + PIB Manaus via API SIDRA
│   ├── _save_pib.py                 ✅ Auxiliar para salvar PIB estadual
│   ├── 02_suframa_extract.py        ♻️ Extrair 6 datasets dos PDFs SUFRAMA (+salarios, extracao BRL insumos)
│   ├── 03_rfb_extract.py            ✅ Processar Excel RFB (272 linhas ZFM)
│   ├── 04_rateio_federal.py         ✅ Rateio descritivo (IPI/II/IRPJ/PIS-COFINS → por subsetor)
│   ├── 06_build_panel.py            ♻️ Painel final (emprego SUFRAMA, +salario_medio, +automacao)
│   ├── 06_build_panel_v1_backup.py  📦 Backup da versão anterior
│   ├── 07_descriptive_stats.py      ♻️ Modelo final: labels SUFRAMA, K-means 3 vars, +salario medio
│   ├── 08_kmeans_cluster.py         ♻️ K-means modelo final: 3 vars (automacao, salario_medio, incentivo_faturamento)
│   ├── 08_kmeans_cluster_v1_backup.py 📦 Backup da versão anterior
│   ├── 09_dea_vrs.py                ✅ DEA final: I(ICMS)+K → Fat+E (HiGHS solver)
│   ├── 10_malmquist.py              ✅ Malmquist: mesmos I/O que DEA (CRS, Färe 1994)
│   ├── 11_simar_wilson.py           ♻️ Simar-Wilson final: z=[ln(I/Fat), ln(K/L), ln(W/L), cluster, trend]
│   └── _audit_data.py               ✅ Script de auditoria de qualidade
├── data/
│   ├── raw/                         ← CSVs originais (IBGE+SUFRAMA+RFB+Salários)
│   ├── interim/                     ← Dados intermediários + rateio descritivo
│   └── processed/                   ← CSVs processados (painel+clusters+DEA+Malmquist)
└── outputs/
    ├── tables/                      ← Tabelas CSV para o TCC
    └── figures/                     ← Figuras PNG para o TCC
```

### Legenda
- ✅ = Inalterado ou com correções menores
- ♻️ = Reescrito/reespecificado
- 📦 = Backup

**Scripts removidos (modelo final):**
- `05_rais_extract.py` — extração RAIS (removido: emprego agora vem da SUFRAMA)
- `05b_cnae_crosswalk.py` — crosswalk CNAE→Subsetor (removido: desnecessário)
- `_debug_crosswalk.py`, `_final_crosswalk_report.py`, `export_crosswalk_grouped.py` — auxiliares RAIS (removidos)

---

## 11. PONTOS DE ATENÇÃO CRÍTICOS

### ✅ Resolvidos
1. **Incentivo fiscal por subsetor:** ICMS restituído (SUFRAMA) usado como proxy. RFB confirmada como somente agregada.
2. **PIB Municipal 2022-2023:** serie atualizada com dados reais do IBGE SIDRA T.5938.
3. **"Bens de Informática":** Consolidado com Eletroeletrônico em todos os datasets.
4. **Solver DEA:** cvxpy/SCS dava eficiências >1 → substituído por scipy.optimize.linprog (HiGHS).
5. **Malmquist VRS:** Infeasibility para DMUs de fronteira em cross-period → migrado para CRS conforme Färe et al. (1994).
6. **Insumos com cobertura parcial (11/23):** VA nao adotado; Faturamento mantido como output direto.
7. **Extracao de faturamento:** ajuste no parser para preservar observacoes com zero estrutural sem perda indevida de registros.
8. **Câmbio hardcoded:** Substituído por BCB API PTAX com fallback automático.
9. **K-means k* determinado endogenamente:** 5 métodos votaram k's diferentes (Elbow=6, Sil=3, CH=8, DB=7, Gap=4). Sem consenso → **Silhouette tiebreaker** (Kaufman & Rousseeuw 1990, gold standard). k*=3, Silhouette=0.501, ARI bootstrap=0.621.
10. **Circularidade do rateio federal:** Comprovada matematicamente ($I_{fed}/Fat = cte$ $\forall s$). Rateio relegado a tabela descritiva apenas.
11. **Emprego RAIS:** abordagem descartada; emprego SUFRAMA adotado como fonte definitiva (mesmo universo de Fat/I/K).
12. **Insumos BRL/USD:** parser configurado para extrair apenas o bloco em R$, evitando duplicacao com bloco em US$.
13. **Salarios (Tab 24):** variavel incorporada ao painel para construir W/L com consistencia operacional.

### ⚠️ Risco Médio (Remanescentes)
1. **ICMS como proxy único de incentivo:** Representa ~25% do custo fiscal total (federal = ~75%). Documentado como limitação explícita.
2. **Escala de eficiência:** Interpretação pode mudar com nova especificação (2 inputs × 2 outputs em vez de 2×1).
3. **Malmquist parcial:** Algumas DMUs de fronteira podem ter <5 períodos por inviabilidade cross-period.
4. **Couros e Similares — 2018 zero estrutural:** Não é dado faltante (NaN) — o subsetor não operou em 2018 (faturamento=0, emprego=0, CAPEX=0, sem salários). Obs excluída pelo filtro de positividade. Painel desbalanceado: 137 obs (22×6 + 1×5). Malmquist: sem transição 2018→2019 para Couros (4 janelas em vez de 5).

---

## 12. REVISÃO DA TABELA DE VARIÁVEIS (Especificação Final)

| Variável | Definição no modelo final | Status |
|----------|---------------------------|--------|
| Incentivo Fiscal ($I$) — **Input DEA** | ICMS restituido real por subsetor-ano | ✅ |
| Faturamento ($Fat$) — **Output DEA** | Faturamento real por subsetor-ano | ✅ |
| Emprego ($E$) — **Output DEA** | SUFRAMA (media mensal: efetiva + temporaria + terceirizada) | ✅ |
| CAPEX ($K$) — **Input DEA** | Investimento em maquinas/equipamentos convertido por PTAX e deflacionado | ✅ |
| PIB Manaus — Controle | Serie real via IBGE SIDRA T.5938 | ✅ |
| Câmbio — Conversão | API PTAX (BCB/Olinda) | ✅ |
| Automação ($K/L$) — **K-means + SW** | Razao capital-trabalho (automacao) | ✅ |
| Salário médio ($W/L$) — **K-means + SW** | Massa salarial (Tab 24) dividida por emprego | ✅ |
| Incentivo/Faturamento ($I/Fat$) — **K-means + SW** | Exposicao fiscal relativa | ✅ |
| Valor Adicionado ($VA$) | Nao adotado no modelo principal por cobertura parcial de insumos (11/23) | ❌ |
| I/VA | Nao adotado no modelo principal | ❌ |

**Evolucao da especificacao (resumo):**
1. O modelo convergiu para Inputs=(ICMS, CAPEX) e Outputs=(Faturamento, Emprego SUFRAMA), com foco explicito em eficiencia de conversao de incentivos.
2. O emprego foi unificado em SUFRAMA para garantir consistencia de universo estatistico com os demais componentes do DEA.
3. O bloco de heterogeneidade adotou tres razoes estruturais (K/L, W/L e I/Fat) em K-means e no segundo estagio.
4. O Valor Adicionado e a razao I/VA foram retirados do nucleo empirico por cobertura parcial de insumos.

---

## 13. RESULTADOS EMPÍRICOS — Modelo Final (Pipeline executado 02/03/2026)

> **✅ Resultados validados (modelo final).** Pipeline completo re-executado com especificação final:
> Inputs=(ICMS, CAPEX) → Outputs=(Faturamento, Emprego SUFRAMA). K-means 3 vars. Simar-Wilson 3 regressores + cluster + trend.
> Todos os números abaixo correspondem à execução definitiva.

---

### 13.1 PAINEL DE DADOS

| Item | Valor |
|------|-------|
| DMUs | 23 subsetores industriais do PIM |
| Período | 2018-2023 (6 anos) |
| Observações | **137** (painel desbalanceado — Couros 2018 excluído: zero estrutural) |
| Colunas | 30 variáveis |
| Base de preços | R$ constantes de 2023 (deflator IPCA) |
| Deflators | 2018: 1.325, 2019: 1.278, 2020: 1.238, 2021: 1.143, 2022: 1.046, 2023: 1.000 |
| Emprego | SUFRAMA (média mensal: efetiva + temporária + terceirizada) |

**Subsetores excluídos:** Couros e Similares 2018 — zero estrutural (faturamento=0, emprego=0, CAPEX=0, sem salários). Não é dado faltante: o subsetor não teve operação industrial naquele ano. Mantido com 5/6 obs completas (2019-2023).
**Subsetores consolidados:** Bens de Informática → Eletroeletrônico.
**Insumos:** 11/23 subsetores com dados diretos (tabela descritiva apenas — não entra no DEA).
**Salários:** 25 subsetores na fonte → 23 após consolidação (Couros NaN em 2018 coerente com zero estrutural).

### 13.2 ESTATÍSTICAS DESCRITIVAS — DESTAQUES

#### Resumo Global (N=137)

| Variável | Média | D.P. | Mediana | Mín. | Máx. |
|----------|-------|------|---------|------|------|
| Faturamento (R$ mi 2023) | 6.933 | 16.228 | 602 | 21 | 89.898 |
| Emprego SUFRAMA | 4.389 | 8.376 | 1.149 | 40 | 42.440 |
| CAPEX (R$ mi 2023) | 1.966 | 3.440 | 283 | 2 | 15.316 |
| ICMS Restituído (R$ mi 2023) | 520 | 1.361 | 42 | 0 | 8.338 |
| Automação K/L (R$ mil/trab.) | 386 | 371 | 264 | 10 | 1.643 |
| Salário Médio W/L (R$/trab.) | 5.339 | 2.387 | 5.053 | 2.073 | 14.268 |
| Incentivo/Faturamento | 0.09 | 0.18 | 0.04 | 0.00 | 1.23 |

#### Concentração do PIM
- **Eletroeletrônico:** ~48% do faturamento total, ~39% do emprego, ~54% dos incentivos (ICMS)
- **Top 6 subsetores:** ~93% do faturamento total do PIM
- $CV(Fat) > 200\%$ — dispersão extrema, poucos subsetores dominam

#### Alertas de Qualidade
- Brinquedos: I/Fat até **1.23** (123%) — incentivo fiscal MAIOR que o faturamento em alguns anos. Explica isolamento como cluster singleto.
- ICMS restituído mínimo = 0 em algumas observações — subsetores muito pequenos.

---

### 13.3 K-MEANS CLUSTERING

#### Especificação

| Parâmetro | Valor |
|-----------|-------|
| Variáveis | $K/L$ (automação), $W/L$ (salário médio), $I/Fat$ (exposição fiscal) — padronizadas via StandardScaler (z-score) |
| Unidade de observação | 23 subsetores (médias temporais) |
| Faixa de k testada | k = 2 a 8 |

#### Resultado da Validação — 5 Métodos Internos

Foram aplicados 5 critérios de seleção de k* recomendados pela literatura (Kaufman & Rousseeuw 1990; Tibshirani et al. 2001; Caliński & Harabasz 1974):

| Método | k* votado | Critério de decisão |
|--------|-----------|---------------------|
| **Elbow (WCSS)** | k = 6 | Maior curvatura na inércia |
| **Silhouette** | k = 3 | $\max \bar{s}(k)$ — coesão intra-cluster vs. separação inter-cluster |
| **Calinski-Harabasz (CH)** | k = 8 | $\max CH(k)$ — razão variância between/within |
| **Davies-Bouldin (DB)** | k = 7 | $\min DB(k)$ — razão dispersão/separação |
| **Gap Statistic** | k = 4 | $Gap(k) \geq Gap(k+1) - s_{k+1}$ (Tibshirani et al. 2001) |

**Resultado: nenhum consenso.** Os 5 métodos votaram 5 valores diferentes de k (3, 4, 6, 7, 8). Nenhum k obteve maioria simples.

#### Mecanismo de Desempate — Silhouette Tiebreaker

Diante da ausência de consenso, o script aplica a regra de desempate: **o k com maior Silhouette médio prevalece** (Kaufman & Rousseeuw 1990, considerado gold standard para validação de clusters).

| k testado | Silhouette | CH | DB |
|-----------|-----------|-----|------|
| 2 | 0.435 | — | — |
| **3** | **0.501** ★ | **24.7** | **0.602** |
| 4 | 0.422 | — | — |
| 5 | 0.395 | — | — |
| 6 | 0.397 | — | — |
| 7 | 0.380 | — | — |
| 8 | 0.361 | — | — |

**k* = 3 com Silhouette = 0.501** — classificação como "reasonable structure" (Kaufman & Rousseeuw 1990: $\bar{s} > 0.50$ indica estrutura real nos dados).

#### Bootstrap Stability

Para avaliar robustez da partição, foram realizadas 100 reamostragens bootstrap:

| k | ARI bootstrap médio | Interpretação |
|---|---------------------|---------------|
| 2 | 0.549 | Moderada |
| **3** | **0.621** | Moderada (melhor da faixa) |
| 4 | 0.449 | Fraca-moderada |

ARI (Adjusted Rand Index) = 0.621 indica que ~62% da estrutura de clusters é recoverable sob reamostragem. Estabilidade moderada, compatível com n=23 (amostra pequena para K-means).

#### Gap Statistic — Detalhe

| k | Gap | Gap_se |
|---|-----|--------|
| 2 | 0.269 | 0.068 |
| 3 | 0.282 | 0.055 |
| **4** | **0.342** | 0.067 |
| 5 | 0.336 | 0.054 |

O critério formal do Gap seleciona k=4. Porém, k=3 e k=4 estão dentro do erro-padrão um do outro. A preferência por k=3 via Silhouette é justificável.

#### Perfil dos Clusters (modelo final)

| Cluster | N | Rótulo proposto | K/L médio | W/L médio | I/Fat médio | Fat. total (R$ bi) | Emp. total | Membros |
|---------|---|-----------------|-----------|-----------|-------------|---------------------|-----------|---------|
| **C0** | 1 | Outlier-incentivado | R$ 49 mil | R$ 5.112 | **63,1%** | — | — | Brinquedos |
| **C1** | 16 | Diversificado | R$ 225 mil | R$ 4.259 | 5,7% | 104,2 | 64.249 | Bebidas, Borracha, Couros, Diversos, Editorial, **Eletroeletrônico**, Madeireiro, Mecânico, Metalúrgico, Mobiliário, Naval, Papel, Alimentícios, Relojoeiro, Têxtil, Vestuário |
| **C2** | 6 | Capital-intensivo | R$ 867 mil | R$ 8.188 | 7,1% | 53,8 | 34.596 | Duas Rodas, Isqueiros, Mineral Não Metálico, Químico, Termoplástico, Ótico |

**Leitura dos perfis:**
- **C0 (Brinquedos):** Singleto. Automação baixa (K/L = R$ 49 mil), salário moderado, mas dependência fiscal altíssima (63% do faturamento vem de incentivo ICMS). Subsetor estruturalmente distinto dos demais.
- **C1 (Diversificado, n=16):** Maioria do PIM. Automação moderada (R$ 225 mil/trabalhador), salário médio na faixa de R$ 4,3 mil, baixa dependência fiscal (5,7%). Fat. total de R$ 104 bi e 64 mil empregos — é o coração industrial da ZFM. Inclui Eletroeletrônico.
- **C2 (Capital-intensivo, n=6):** Alta automação (R$ 867 mil/trabalhador — quase 4× C1), salários elevados (R$ 8,2 mil — quase 2× C1), baixa dependência fiscal (7,1%). Concentra Duas Rodas, Químico, Termoplástico.

#### ACHADO RELEVANTE — Eletroeletrônico em C1

O Eletroeletrônico — maior subsetor do PIM em faturamento absoluto — classifica-se em C1 (diversificado), não em C2 (capital-intensivo). Isso ocorre porque o modelo usa variáveis-razão (intensidade por trabalhador), não níveis absolutos. O K/L do Eletroeletrônico (≈ R$ 363 mil) é **moderado** na escala do PIM — abaixo da média de C2 (R$ 867 mil). Subsetores como Duas Rodas, Químico e Termoplástico têm K/L significativamente maior.

**Implicação:** C2 não é "cluster tech" mas "cluster capital-intensivo". O uso de variáveis-razão (Simar & Wilson 2007) separa escala de intensidade — o Eletroeletrônico é grande em volume, mas não é o mais capital-intensivo *por trabalhador*.

---

### 13.4 DEA — ANÁLISE ENVOLTÓRIA DE DADOS

#### Especificação (Modelo Final)

| Item | Detalhe |
|------|---------|
| Modelo | BCC (VRS) output-oriented |
| Inputs | $I$ (ICMS restituído real) + $K$ (CAPEX real) |
| Outputs | $Fat$ (Faturamento real) + $E$ (Emprego SUFRAMA) |
| Solver | scipy.optimize.linprog — HiGHS |
| Modelos estimados | VRS (BCC), CRS (CCR), Eficiência de Escala, Metafronteira, TGR |
| Rule of thumb | $n = 23 \geq 3 \times (2+2) = 12$ ✔️ |

#### Escores VRS — Resumo Global

| Estatística | Valor |
|-------------|-------|
| Média global | **0.821** |
| Mediana | **0.995** |
| DMUs eficientes (θ ≥ 0.999) | **68 / 137 (50%)** |
| DMUs eficientes por ano | 9-13 (média ≈ 11) |

| Ano | Eficientes | DMUs na fronteira |
|-----|-----------|-------------------|
| 2018 | 9 / 22 | Eletroeletrônico, Relojoeiro, Duas Rodas, Bebidas, Mecânico, Madeireiro, Têxtil, Brinquedos, Diversos |
| 2019 | 11 / 23 | + Papel, Couros, Mobiliário |
| 2020 | 11 / 23 | + Metalúrgico, Isqueiros; − Relojoeiro, Couros, Mobiliário |
| 2021 | 12 / 23 | + Borracha, Naval, Isqueiros |
| 2022 | 13 / 23 | Máx. de eficientes no período |
| 2023 | 12 / 23 | Mecânico retorna; Bebidas, Metalúrgico saem |

#### Top 5 Subsetores (média θ_VRS 2018-2023)

| Subsetor | θ_VRS médio | Cluster | Sempre eficiente? |
|----------|------------|---------|-------------------|
| Eletroeletrônico | **1.000** | C1 | Sim |
| Brinquedos | **1.000** | C0 | Sim |
| Diversos | **1.000** | C1 | Sim |
| Madeireiro | **1.000** | C1 | Sim |
| Têxtil | **1.000** | C1 | Sim |
| Duas Rodas | **1.000** | C2 | Sim |
| Mecânico | **0.997** | C1 | Quase (1 ano < 1) |
| Bebidas | **0.983** | C1 | Quase |

#### Bottom 5 Subsetores

| Subsetor | θ_VRS médio | Cluster |
|----------|------------|---------|
| Mineral Não Metálico | **0.341** | C2 |
| Ótico | **0.383** | C2 |
| Couros e Similares | **0.454** | C1 |
| Vestuário e Calçados | **0.513** | C1 |
| Químico | **0.547** | C2 |

#### ⚠️ NOTA — 50% de DMUs na fronteira VRS

68/137 observações são eficientes (θ=1). Isso é comum em modelos BCC com n pequeno e múltiplos inputs/outputs. Com 2 inputs + 2 outputs e 22-23 DMUs por cross-section, o BCC tem dimensionalidade efetiva alta → muitas DMUs formam sua própria faceta da fronteira convexa.

**Discriminação insuficiente?** Possível. Porém:
1. O modelo CRS (mais restritivo) produz média muito menor, com bem menos eficientes → a questão é VRS, não o modelo inteiro.
2. A eficiência de escala ($SE = \theta_{CRS}/\theta_{VRS}$) complementa a análise: DMUs VRS-eficientes mas com SE baixo operam em escala subótima.
3. A metafronteira + Simar-Wilson usam o θ_VRS como variável dependente contínua — a regressão consegue explicar variação mesmo com muitas DMUs na fronteira.

**Discussão com orientador:** Considerar se a alta proporção de eficientes é aceitável para TCC ou se é necessário robustez adicional (e.g., super-efficiency, modelo CRS puro, ou redução dimensional).

#### Metafronteira — Technology Gap Ratio (TGR)

A TGR é calculada por subsetor-ano como $TGR_{it} = \theta^{meta}_{it} / \theta^{grupo}_{it}$.

| Cluster | TGR médio | Interpretação |
|---------|-----------|---------------|
| C0 (Brinquedos) | **1.000** | Singleto — fronteira de grupo = metafronteira |
| C1 (Diversificado, n=16) | **0.990** | 1% de gap em relação à metafronteira |
| C2 (Capital-intensivo, n=6) | **0.719** | **28% de gap** — C2 é o cluster mais distante da metafronteira |

**Achado relevante (modelo final vs. especificação anterior):** Na especificação anterior (4 variáveis incluindo ln(CAPEX) como nível), C2 (tech) era o mais próximo da metafronteira (TGR=0.89). No modelo final, C2 (capital-intensivo, sem Eletroeletrônico) é o **mais distante**. Inversão completa. Isso ocorre porque:
1. Eletroeletrônico (sempre eficiente) saiu de C2 → C1, elevando a fronteira de C1.
2. C2 agora contém subsetores capital-intensivos com eficiências moderadas-baixas (Mineral 0.34, Ótico 0.38, Químico 0.55).
3. A metafronteira é dominada por DMUs de C1 (que inclui Eletroeletrônico, Diversos, Têxtil, Madeireiro — sempre eficientes).

---

### 13.5 ÍNDICE DE MALMQUIST (CRS)

#### Decomposição Global (média geométrica, transições válidas)

| Componente | Valor | Interpretação |
|------------|-------|---------------|
| **M (Malmquist)** | **0.831** | **Declínio de 17% na PTF** |
| **EC (Efficiency Change)** | **0.829** | DMUs se afastaram da fronteira |
| **PEC (Pure Efficiency Change)** | **0.982** | Leve perda de eficiência pura |
| **SC (Scale Change)** | **0.844** | **Perda de escala** (principal componente da queda de EC) |
| **TC (Technical Change)** | **1.003** | Fronteira permaneceu estável |
| Transições válidas | 91 / 114 (80%) | 23 transições com infeasibility CRS |

**Achado-chave:** A queda de produtividade é explicada por perda de eficiência técnica (EC), *não* por regressão da fronteira tecnológica (TC ≈ 1). Ao decompor EC em PEC×SC, observa-se que a principal fonte de perda é **escala** (SC=0.844), e não eficiência pura (PEC=0.982).

**Leitura por cluster (média geométrica):**
- C0: PEC=1.000, SC=0.918
- C1: PEC=0.969, SC=0.877
- C2: PEC=1.005, SC=0.775

Conclusão: o cluster C2 sofre principalmente com ineficiência de escala dinâmica, não com perda de eficiência pura.

#### DMUs sem transições Malmquist válidas (0 períodos)

| Subsetor | Cluster | Motivo |
|----------|---------|--------|
| Diversos | C1 | Sempre na fronteira CRS cross-period → EC indefinido |
| Madeireiro | C1 | Idem |
| Têxtil | C1 | Idem |

Estas 3 DMUs são VRS-eficientes em todos os anos e, ao resolver os programas lineares CRS cross-period, retornam infeasible para todas as 5 transições. Limitação conhecida do Malmquist CRS (Färe et al. 1994). Excluídas das médias geométricas.

#### Subsetores com melhor/pior PTF (geomean M)

| Top 3 (catching-up) | M | Bottom 3 (declining) | M |
|---------------------|---|----------------------|---|
| Papel e Papelão | 1.278 | Químico | 0.585 |
| Vestuário e Calçados | 1.071 | Eletroeletrônico | 0.631 |
| Editorial e Gráfico | 1.022 | Mecânico | 0.688 |

**Nota:** Eletroeletrônico, apesar de sempre VRS-eficiente, apresenta M=0.631 — 37% de declínio de PTF total. Isso ocorre porque (a) a fronteira CRS e VRS divergem para DMUs com forte deseconomia de escala (SE=0.138), e (b) o Malmquist usa CRS por necessidade metodológica.

---

### 13.6 SIMAR-WILSON — DETERMINANTES DA EFICIÊNCIA

#### Modelo Principal (Regressão Truncada, B=2000 bootstrap)

$$\theta_{VRS} = f\left(\ln(I/Fat),\; \ln(K/L),\; \ln(W/L),\; D_{c0},\; D_{c2},\; t\right) + \varepsilon$$

| Variável | β | IC 95% Bootstrap | Signif. |
|----------|---|-------------------|---------|
| Constante | −2.184 | [−4.329, +0.505] | Não |
| **ln(I/Fat)** | **−0.139** | [−0.150, −0.049] | **Sim** ★ |
| **ln(K/L)** | **−0.508** | [−0.607, −0.296] | **Sim** ★ |
| **ln(W/L)** | **+1.105** | [+0.677, +1.389] | **Sim** ★ |
| Cluster 0 (Brinquedos) | −0.039 | [−0.572, +0.603] | Não |
| **Cluster 2 (Capital-intensivo)** | **−0.411** | [−0.695, −0.143] | **Sim** ★ |
| Tendência temporal | −0.006 | [−0.039, +0.036] | Não |

**4 variáveis significativas, 3 não significativas.** Modelo com bom poder explicativo.

#### Interpretação dos Achados Centrais

1. **ln(I/Fat) negativo e significativo (β = −0.139):**
   - Maior intensidade de incentivo fiscal → **menor** eficiência.
   - Interpretação: subsetores dependentes de incentivo (I/Fat alto) são menos eficientes. Possível moral hazard: incentivos generosos reduzem pressão por eficiência.
   - **Achado-chave para política pública** — na v1 o incentivo era não significativo (nível absoluto). Com razão I/Fat, o efeito aparece.

2. **ln(K/L) negativo e significativo (β = −0.508):**
   - Maior automação (capital por trabalhador) → **menor** eficiência VRS.
   - Consistente com retornos decrescentes de capital: DMUs muito mecanizadas não convertem investimento em faturamento/emprego proporcionalmente.
   - O sinal não significa que CAPEX é ruim — significa que o *excesso* relativo de capital não gera eficiência proporcional.

3. **ln(W/L) positivo e significativo (β = +1.105):**
   - Maior salário por trabalhador → **maior** eficiência. Efeito robusto (maior coeficiente).
   - Interpretação como **proxy de capital humano**: subsetores que pagam mais atraem/retêm trabalhadores mais qualificados, gerando mais faturamento e emprego produtivo.
   - Alternativa: efeito *efficiency wage* (Shapiro & Stiglitz 1984) — salários acima do mercado induzem maior esforço.

4. **Cluster 2 negativo e significativo (β = −0.411):**
   - Pertencer ao cluster capital-intensivo **reduz** eficiência em relação a C1 (referência).
   - Corrobora a TGR: C2 é o cluster mais distante da metafronteira (TGR=0.720).
   - Inversão da v1: na especificação anterior, "cluster tech" tinha β positivo. Agora, com Eletroeletrônico em C1, C2 = capital-intensivo tem β negativo.

5. **Tendência e Cluster 0 não significativos** — consistente com Malmquist (TC ≈ 1) e com Brinquedos sendo singleto (pouca potência estatística).

#### Robustez (OLS comparativo)

| Variável | SW β | OLS β | OLS p |
|----------|------|-------|-------|
| ln(I/Fat) | −0.139 | −0.052 | 0.0001 |
| ln(K/L) | −0.508 | −0.138 | 0.0002 |
| ln(W/L) | +1.105 | +0.462 | <0.0001 |
| Cluster 2 | −0.411 | −0.258 | 0.009 |
| Tendência | −0.006 | +0.005 | 0.60 |

**Todas as variáveis significativas no SW são também significativas no OLS.** Sinais idênticos. Magnitudes SW maiores (efeito da censura no OLS). Coerência robusta.

#### Modelo Estendido (OLS + COVID + Eficiência de Escala)

| Resultado | Valor |
|-----------|-------|
| COVID dummy | Não significativo |
| Eficiência de Escala | **Significativo** (β negativo, p < 0.001) |

Interpretação: DMUs mais próximas da escala CRS ótima são mais eficientes. O efeito COVID é absorvido pelas demais variáveis — impacto pandêmico heterogêneo, capturado por cluster/automação.

---

### 13.7 SÍNTESE PARA O TCC — MENSAGENS-CHAVE

#### Achado Principal (resposta à pergunta de pesquisa)

> A heterogeneidade produtiva dos subsetores do PIM é **determinante** na eficiência de conversão de incentivos fiscais em faturamento e empregos. O cluster diversificado (C1, 16 subsetores incluindo Eletroeletrônico) domina a fronteira eficiente (TGR = 0.99), enquanto o cluster capital-intensivo (C2, 6 subsetores) apresenta gap de 28% (TGR = 0.72). **A intensidade de incentivo fiscal (I/Fat) tem efeito negativo significativo sobre a eficiência** (β = −0.139): mais incentivo relativo associa-se a menor eficiência. Salários (proxy de capital humano) são o determinante mais forte da eficiência (β = +1.105).

#### Confronto com a Hipótese Central

| Hipótese Original | Resultado observado | Veredicto |
|-------------------|-------------|-----------|
| Maior automação (K/L) → maior eficiência em faturamento | β(K/L) = −0.508 (negativo, signif.) | **REJEITADA** — automação isolada reduz eficiência |
| Maior automação → menor eficiência em emprego (trade-off) | DEA inclui emprego como output → o modelo captura ambos simultaneamente | **PARCIALMENTE TESTADA** |

**Reinterpretação sugerida:** A hipótese assume relação linear automação→eficiência. Os dados sugerem que:
1. O efeito da automação é **mediado pelo capital humano** (W/L): subsetores que investem em capital físico E humano simultaneamente são eficientes.
2. O excesso de capital sem qualificação correspondente gera retornos decrescentes.
3. A eficiência é função do **equilíbrio** entre K/L e W/L, não da maximização de K/L isoladamente.

#### Implicações para Política Pública
1. **Incentivo condicional:** I/Fat negativo e significativo → incentivos deveriam ser vinculados a contrapartidas de produtividade, não apenas presença no PIM.
2. **Capital humano como alavanca:** W/L é o preditor mais forte de eficiência (+1.105). Investimento em qualificação pode ter retorno superior a isenções fiscais.
3. **Catching-up:** 3 subsetores de C2 (Mineral, Ótico, Químico) persistentemente ineficientes — diagnóstico individual necessário.
4. **Monitoramento:** Declínio de 17% na PTF (M=0.831) exige atenção — eficiência caindo sem regressão da fronteira sugere subutilização de capacidade.

---

### 13.8 INVENTÁRIO DE OUTPUTS GERADOS

#### Tabelas (outputs/tables/) — 14 arquivos

| Arquivo | Conteúdo | Uso no TCC |
|---------|----------|------------|
| tab_descritivas.csv | Estatísticas descritivas | Tabela 1 (Cap. 5.1) |
| tab_media_subsetor.csv | Médias por subsetor | Tabela 2 (Cap. 5.1) |
| tab_media_ano.csv | Médias por ano | Tabela 3 (Cap. 5.1) |
| tab_correlacao.csv | Matriz de correlação | Tabela 4 (Cap. 5.1) |
| tab_kmeans_validation.csv | Validação K-means (5 métodos, k=2…8) | Tabela 5 (Cap. 5.2) |
| tab_gap_statistic.csv | Gap Statistic (k=2…8) | Tabela 5b (Cap. 5.2) |
| tab_bootstrap_stability.csv | Bootstrap ARI (k=2…8) | Tabela 5c (Cap. 5.2) |
| tab_perfil_clusters_v2.csv | Perfil clusters modelo final | Tabela 6 (Cap. 5.2) |
| tab_dea_summary.csv | Resumo DEA por subsetor | Tabela 7 (Cap. 5.3) |
| tab_metafrontier_tgr.csv | TGR por subsetor-ano | Tabela 8 (Cap. 5.5) |
| tab_malmquist_summary.csv | Malmquist EC/TC/M | Tabela 9 (Cap. 5.4) |
| tab_simar_wilson.csv | Simar-Wilson bootstrap | Tabela 10 (Cap. 5.6) |
| tab_tobit_comparison.csv | Robustez OLS (SW vs OLS) | Tabela 11 (Cap. 5.6) |
| tab_custo_fiscal_total.csv | Custo fiscal total por subsetor | Tabela 12 (Cap. 5.1) |

#### Figuras (outputs/figures/) — 17 arquivos

| Arquivo | Conteúdo | Uso no TCC |
|---------|----------|------------|
| fig_boxplot_vars.png | Boxplots variáveis-chave | Figura 1 |
| fig_evolucao_temporal.png | Séries temporais PIM | Figura 2 |
| fig_heatmap_correlacao.png | Heatmap correlações | Figura 3 |
| fig_scatter_matrix.png | Matriz de dispersão | Figura 4 |
| fig_concentracao_pim.png | Concentração faturamento | Figura 5 |
| fig_validation_panel.png | Painel de validação K-means (5 métricas) | Figura 6 |
| fig_clusters_2d_v2.png | Scatter 2D clusters (PCA) | Figura 7 |
| fig_clusters_radar_v2.png | Radar dos clusters | Figura 8 |
| fig_dea_scores.png | Escores DEA por subsetor | Figura 9 |
| fig_dea_by_cluster.png | Boxplot DEA por cluster | Figura 10 |
| fig_frontier_scatter.png | Scatter fronteira | Figura 11 |
| fig_eff_vs_contextual.png | Eficiência vs. contextuais | Figura 12 |
| fig_tgr_evolution.png | Evolução TGR por cluster | Figura 13 |
| fig_malmquist_decomp.png | Decomposição Malmquist | Figura 14 |
| fig_malmquist_ec_tc.png | EC vs. TC por DMU | Figura 15 |
| fig_malmquist_evolution.png | Evolução temporal Malmquist | Figura 16 |
| fig_simar_wilson_coefs.png | Coeficientes SW bootstrap | Figura 17 |

#### Dados Processados — Corretos e Auditados
Nenhum débito técnico pendente nos outputs. Todos os arquivos foram regenerados em 02/03/2026.

---

### 13.9 DADOS PROCESSADOS (data/processed/)

| Arquivo | Observações | Colunas-chave |
|---------|-------------|---------------|
| painel_subsetor_ano.csv | 137 (23 sub, desbalanceado) | subsetor, ano, faturamento_real2023, emprego, capex_real2023, icms_restituido_real2023, automacao, salario_medio, incentivo_faturamento |
| painel_subsetor_ano_full.csv | 137 | Versão com todas as 30 colunas |
| painel_com_cluster.csv | 137 | + cluster (K-means final) |
| subsetor_cluster_map.csv | 23 | subsetor → cluster |
| dea_scores.csv | 137 | + eff_vrs, eff_crs, scale_eff, eff_group_vrs, tgr |
| malmquist_results.csv | 114 (91 válidas) | + EC, TC, M por DMU-período |
| suframa_salarios_subsetor.csv | 149 (25×6) | massa salarial R$ 1.000 nominal |
| suframa_insumos_subsetor.csv | 66 (11×6) | insumos R$, apenas BRL |

---

## 14. PLANO DE FECHAMENTO (Modelo Final, atualizado 14/03/2026)

> **Diretriz central da reta final:** preservar o motor empírico já validado e adicionar apenas a robustez metodológica necessária para banca/publicação, sem inflar escopo.

### 14.1 O que já está fechado (não reabrir sem evidência forte)

| Bloco | Status | Observação |
|------|--------|------------|
| Pipeline 01→11 reexecutado | ✅ | Outputs regenerados e auditados |
| K-means (3 variáveis-razão) | ✅ | k*=3 por tiebreaker de Silhouette |
| DEA estático (VRS + CRS + scale_eff) | ✅ | Escores validados |
| Metafronteira (TGR) | ✅ | C1≈0.99, C2≈0.72 |
| Malmquist principal (CRS) | ✅ | M, EC, TC calculados |
| Simar-Wilson (bootstrap) | ✅ | Modelo principal validado |
| Inventário de outputs (17 figs, 14 tabs) | ✅ | Nomes e contagens consistentes |

### 14.2 Pendências obrigatórias (prioridade máxima)

| # | Entrega obrigatória | Objetivo | Estimativa | Prioridade | Status |
|---|--------------------|----------|------------|------------|--------|
| 1 | **Adicionar decomposição dinâmica completa no texto (EC, TC, PEC, SC)** | Atender conselho do orientador sobre componente de escala | 3-4h | 🔴 ALTA | ✅ |
| 2 | **Tabela de robustez enxuta de especificações** (modelo principal + comparativos) | Blindar defesa metodológica sem redundância | 3-4h | 🔴 ALTA | ✅ |
| 3 | **Redigir Cap. 5 (Resultados)** com numeração final de tabelas/figuras | Converter outputs em narrativa acadêmica | 2 dias | 🔴 ALTA | 🔄 (rascunho pronto em §21) |
| 4 | **Redigir Cap. 6 (Discussão)** com literatura + implicações | Explicar mecanismos, trade-offs e limites | 1-2 dias | 🔴 ALTA | 🔄 (rascunho pronto em §22) |
| 5 | **Redigir Cap. 7 (Conclusão)** | Fechar contribuição e agenda futura | 1 dia | 🔴 ALTA | 🔄 (rascunho pronto em §22) |

### 14.3 Pendências estratégicas (alta relevância, menor risco)

| # | Entrega estratégica | Objetivo | Estimativa | Prioridade | Status |
|---|--------------------|----------|------------|------------|--------|
| 6 | **Seção ambiental (proxy qualitativa) em Discussão + Anexo** | Agregar valor para tema Amazônia sem alterar DEA base | 1 dia | 🟠 MÉDIA-ALTA | ✅ (base consolidada BCCAS + cruzamentos concluídos) |
| 7 | **Criar Seção 1.3 — Objetivos Específicos** | Coerência entre pergunta, método e resultados | 30 min | 🟠 MÉDIA | ✅ (definido no mestre) |
| 8 | **Revisar/enxugar Caps. 1-4** | Reduzir redundância e alinhar linguagem | 1 dia | 🟠 MÉDIA | 🔄 (protocolo de enxugamento definido em §8.5) |
| 9 | **Resumo + Abstract (versão final)** | Síntese para banca e submissão | 2h | 🟡 BAIXA (final) | ⬜ |
| 10 | **Formatação ABNT/UFPB + checklist final** | Entrega formal | 1 dia | 🟡 BAIXA (final) | ⬜ |
| 11 | **Apêndices e anexos técnicos** | Reprodutibilidade e robustez | 1/2 dia | 🟡 BAIXA (final) | ⬜ |

### 14.4 Matriz de Convergência (TCC1 legado → Modelo Final)

> Objetivo: garantir que o texto final não herde inconsistências do rascunho TCC1 (`METODOLOGIA_ZFM_TCC1.txt`) e permaneça 100% alinhado ao pipeline validado.

| Tema | TCC1 legado | Modelo Final (obrigatório) | Ação textual pendente |
|------|-------------|-----------------------------|-----------------------|
| Output econômico DEA | Valor Adicionado (VA) | Faturamento real (`Fat`) | Substituir VA por Fat em metodologia/resultados/conclusão, mantendo VA apenas como discussão histórica |
| Output emprego DEA | RAIS (crosswalk CNAE) | Emprego SUFRAMA (mesmo universo de Fat/I/K) | Remover qualquer frase normativa que trate RAIS como fonte principal |
| Ferramenta DEA | `pyDEA` em alguns trechos legados | Solver LP (`scipy.optimize`/HiGHS) conforme scripts atuais | Atualizar seção de software para refletir código executado |
| Hipótese central | Automação vs VA/Emprego | Automação vs Fat/Emprego, com hipótese revisada após resultados | Harmonizar introdução, objetivo e discussão com veredicto final |
| Malmquist | EC/TC sem escala explícita | M, EC, TC + leitura PEC/SC no fechamento | Inserir decomposição completa e explicação curta de escala |
| Ambiental | Ausente no TCC1 | Proxy qualitativa na discussão/anexo (fora do DEA base) | Criar subseção no Cap. 6 e anexo metodológico |
| Escopo temporal | 2018-2023 (ok) | 2018-2023 (mantido) | Verificar consistência em todos os capítulos |

Checklist de varredura antes de fechar o texto final:

1. Buscar e revisar termos: `RAIS`, `valor adicionado`, `VA`, `pyDEA`, `input-oriented`, `Lei de Informática` (quando implicar método).
2. Confirmar que todas as equações de metodologia usam Inputs=(ICMS, CAPEX) e Outputs=(Faturamento, Emprego SUFRAMA).
3. Confirmar que hipótese, resultados e conclusão usam a mesma formulação final.

---

## 15. APRESENTAÇÃO AO ORIENTADOR — O PERCURSO COMPLETO

> **Objetivo desta seção:** Contar a história completa do trabalho de ponta a ponta — desde a pergunta de pesquisa até os resultados finais — de forma que o orientador entenda cada decisão, cada número e cada implicação. Não é um resumo: é o roteiro narrativo completo, auto-contido, para a reunião de orientação.

---

### 15.1 A Pergunta de Pesquisa

O Polo Industrial de Manaus (PIM) é sustentado por um dos maiores regimes de incentivo fiscal do mundo. A Zona Franca de Manaus (ZFM) concede isenções e restituições de ICMS, IPI, II, IRPJ, PIS e COFINS para empresas que se instalam na região. O modelo foi criado em 1967 e prorrogado até 2073.

A pergunta central deste TCC é: **os 23 subsetores industriais que compõem o PIM são igualmente eficientes em converter esses incentivos fiscais em resultados econômicos (faturamento e empregos)?** E se não são — quais características estruturais explicam as diferenças?

Essa pergunta é relevante porque o debate sobre a ZFM frequentemente trata o polo como um bloco homogêneo ("a ZFM é eficiente ou não?"), quando na realidade há 23 subsetores com perfis produtivos radicalmente diferentes — desde Brinquedos (1 subsetor, alta dependência fiscal) até Duas Rodas (capital-intensivo, escala massiva).

A hipótese original era que subsetores mais automatizados (maior capital por trabalhador) seriam mais eficientes em faturamento, mas menos eficientes em geração de empregos. Os dados, como veremos, contam uma história diferente e mais interessante.

---

### 15.2 Proveniência dos Dados — De Onde Vem Cada Número

Todos os dados primários vêm de fontes públicas oficiais. Nenhum dado foi estimado, imputado ou aproximado por modelo — cada variável é observada diretamente na sua fonte.

#### Fonte principal: SUFRAMA — Caderno de Indicadores do PIM (2018-2023)

O Caderno de Indicadores da SUFRAMA é publicado anualmente em PDF e contém tabelas com dados por subsetor do PIM. Foram extraídas 6 tabelas distintas via parser Python customizado (`02_suframa_extract.py`):

| Tabela SUFRAMA | Variável extraída | Nome no painel | Papel no modelo |
|----------------|-------------------|----------------|-----------------|
| Tab 5 — Faturamento | Faturamento bruto (R$ correntes) | `faturamento_real2023` (deflacionado) | **Output DEA 1** |
| Tab 18 — Emprego | Média mensal (efetiva + temporária + terceirizada) | `emprego_SUFRAMA` | **Output DEA 2** |
| Tab 10 — ICMS Restituído | ICMS restituído por subsetor (R$ correntes) | `icms_restituido_real2023` (deflacionado) | **Input DEA 1** |
| Tab 11 — CAPEX | Investimento em máquinas e equipamentos (USD correntes) | `capex_real2023` (USD→BRL via PTAX, deflacionado) | **Input DEA 2** |
| Tab 24 — Salários | Salários + Encargos + Benefícios Sociais (R$ 1.000) | `salario_medio` (= massa / emprego = W/L) | **K-means var 2 + Simar-Wilson regressor** |
| Tab 14 — Insumos | Insumos adquiridos (R$ correntes, apenas BRL) | `insumos_real2023` | Descritiva (não entra no DEA por cobertura parcial: 11/23 subsetores) |

**Por que SUFRAMA e não RAIS/IBGE?** A RAIS (Relação Anual de Informações Sociais) foi inicialmente usada como fonte de emprego, mas exigia um crosswalk CNAE→Subsetor PIM que introduzia ruído taxonômico. A SUFRAMA reporta emprego diretamente por subsetor, no mesmo universo estatístico das demais variáveis (faturamento, ICMS, CAPEX). A decisão de unificar em SUFRAMA eliminou a fricção de compatibilização e garantiu consistência interna do painel.

#### Fontes complementares: IBGE e BCB (via API)

| Fonte | Variável | API / Endpoint | Uso |
|-------|----------|----------------|-----|
| IBGE SIDRA | IPCA Número-Índice (T.1737) | `servicodados.ibge.gov.br/api/v3/agregados/1737/...` | Deflacionar todas as variáveis monetárias para R$ de 2023 |
| IBGE SIDRA | PIB Municipal Manaus (T.5938) | `servicodados.ibge.gov.br/api/v3/agregados/5938/...` | Contexto descritivo |
| BCB SGS | PTAX (câmbio médio, série 3698) | `api.bcb.gov.br/dados/serie/bcdata.sgs.3698/...` | Converter CAPEX de USD para BRL |

**Processo de deflação:** Todas as variáveis monetárias (faturamento, ICMS, CAPEX em BRL, massa salarial) foram deflacionadas pelo IPCA para valores reais de dezembro/2023. O deflator é calculado como razão entre o IPCA de dezembro do ano-base e o IPCA de dezembro de 2023.

#### Fonte secundária: Receita Federal do Brasil

| Fonte | Conteúdo | Uso |
|-------|----------|-----|
| RFB — Demonstrativo de Benefícios Tributários (DGT) | Renúncia federal por subsetor ZFM (IPI, II, IRPJ, PIS/COFINS) | Contexto descritivo — rateio federal. **Não usado no DEA** porque o rateio por subsetor é proporcional ao faturamento, gerando circularidade: $I_{fed}(s)/Fat(s) = cte$ $\forall s$ |

#### Construção do Painel Final

O painel resulta do merge das 6 tabelas SUFRAMA, deflacionadas e enriquecidas com variáveis-razão calculadas:

| Variável calculada | Fórmula | Interpretação |
|--------------------|---------|---------------|
| `automacao` ($K/L$) | CAPEX real / Emprego | Intensidade de capital por trabalhador (proxy de automação) |
| `salario_medio` ($W/L$) | Massa salarial real / Emprego | Salário médio (proxy de capital humano / qualificação) |
| `incentivo_faturamento` ($I/Fat$) | ICMS restituído real / Faturamento real | Dependência fiscal (fração do faturamento coberta por incentivo ICMS) |

**Painel final:** 137 observações (23 subsetores × 6 anos, menos 1 — Couros e Similares 2018 excluído por zero estrutural: subsetor inativo naquele ano, todos os valores = 0). 30 colunas.

---

### 15.3 O Pipeline Analítico — Uma Técnica Para Cada Pergunta

O pipeline combina 4 técnicas em sequência lógica. Cada técnica responde a uma pergunta específica, e o output de uma alimenta a próxima:

```
┌──────────────────────────────────────────────────────────────────────────┐
│              PIPELINE ANALÍTICO — FLUXO E DEPENDÊNCIAS                  │
│                                                                          │
│   DADOS BRUTOS              PAINEL                EXPLORATÓRIA           │
│   ┌──────────┐           ┌──────────┐          ┌──────────────┐         │
│   │ SUFRAMA  │───merge──▶│ 23×6=137 │──stats──▶│ Descritivas  │         │
│   │ IBGE/BCB │  deflac   │ obs, 30  │          │ Correlações  │         │
│   │ RFB      │  +razões  │ colunas  │          │ Concentração │         │
│   └──────────┘           └────┬─────┘          └──────────────┘         │
│                               │                                          │
│           ┌───────────────────┼──────────────────────┐                  │
│           ▼                   ▼                      ▼                  │
│    ┌──────────────┐    ┌──────────────┐       ┌──────────────┐         │
│    │  K-MEANS     │    │   DEA-BCC    │       │  MALMQUIST   │         │
│    │  3 vars-razão│    │  2 inputs    │       │  CRS (Färe)  │         │
│    │  k*=3        │    │  2 outputs   │       │  EC × TC = M │         │
│    │              │    │  θ ∈ (0,1]   │       │              │         │
│    │  SEGMENTA    │    │  MENSURA     │       │  DINÂMICA    │         │
│    └──────┬───────┘    └──────┬───────┘       └──────────────┘         │
│           │                   │                                          │
│           ▼                   ▼                                          │
│    ┌──────────────┐    ┌──────────────┐                                 │
│    │ METAFRONTEIRA│    │ SIMAR-WILSON │                                 │
│    │ TGR entre    │    │ θ ~ f(z,D,t) │                                │
│    │ clusters     │    │ B=2000 boot  │                                 │
│    │ COMPARA      │    │ EXPLICA      │                                 │
│    └──────────────┘    └──────────────┘                                 │
└──────────────────────────────────────────────────────────────────────────┘
```

| Etapa | Técnica | Pergunta que responde | O que produz |
|-------|---------|----------------------|--------------|
| 1 | **K-means** | "Existem perfis estruturais distintos entre os subsetores?" | 3 clusters → dummies para Simar-Wilson + grupos para metafronteira |
| 2 | **DEA-BCC** | "Qual a eficiência de cada subsetor-ano em converter incentivos em resultados?" | θ_VRS por observação → variável dependente do Simar-Wilson |
| 3 | **Metafronteira** | "O gap entre clusters é estrutural ou operacional?" | TGR por cluster → quantifica distância tecnológica |
| 4 | **Malmquist** | "A eficiência melhorou ou piorou ao longo do tempo?" | M, EC, TC + PEC, SC → decompõe produtividade em catching-up, inovação e escala |
| 5 | **Simar-Wilson** | "O que *explica* as diferenças de eficiência?" | Coeficientes β → identifica determinantes (regressão truncada com bootstrap) |

---

#### 15.3.1 Etapa 1 — Segmentação K-means: Encontrando Perfis Estruturais

**Objetivo:** Identificar grupos de subsetores com perfis produtivos semelhantes, sem impor classificações a priori.

**Variáveis de segmentação (3 razões):**
- $K/L$ — automação (capital por trabalhador)
- $W/L$ — salário médio (proxy de capital humano)
- $I/Fat$ — dependência fiscal (incentivo como fração do faturamento)

**Por que variáveis-razão?** Simar & Wilson (2007) recomendam que as variáveis contextuais ($z_i$) em regressões de segundo estágio sejam razões, não níveis absolutos. Razões eliminam o efeito de escala: um subsetor com R$ 10 bilhões de faturamento e outro com R$ 500 milhões são comparados pela *intensidade* de capital e incentivo, não pelo *volume*. Isso é crítico para K-means, que é sensível à escala das variáveis.

**Padronização:** StandardScaler (z-score, média=0, desvio=1) aplicado antes do K-means para equalizar as escalas.

**Seleção do número de clusters (k*):**

Foram testados 5 métodos de validação interna para k = 2 a 8:

| Método | Referência | k* votado |
|--------|-----------|-----------|
| Elbow (WCSS) | Thorndike (1953) | k = 6 |
| Silhouette | Kaufman & Rousseeuw (1990) | k = 3 |
| Calinski-Harabasz | Caliński & Harabasz (1974) | k = 8 |
| Davies-Bouldin | Davies & Bouldin (1979) | k = 7 |
| Gap Statistic | Tibshirani, Walther & Hastie (2001) | k = 4 |

**Resultado: nenhum consenso.** Os 5 métodos votaram 5 valores diferentes. Nenhum k obteve sequer 2 votos.

**Regra de desempate:** Na ausência de consenso, o script aplica o **Silhouette tiebreaker** — o k com maior coeficiente Silhouette médio prevalece. Justificativa: Kaufman & Rousseeuw (1990) é o critério mais amplamente aceito para validação de clusters, pois mede simultaneamente coesão intra-cluster e separação inter-cluster.

**k* = 3, Silhouette = 0.501.** Segundo a escala de Kaufman & Rousseeuw: $\bar{s} > 0.50$ indica "reasonable structure" — os clusters refletem uma estrutura real nos dados, não artefato.

**Robustez via bootstrap:** 100 reamostragens com cálculo do Adjusted Rand Index (ARI). ARI(k=3) = 0.621 (moderado) — ~62% da estrutura é recuperável sob reamostragem. Para n=23 (amostra pequena para K-means), isso é aceitável.

**Perfis encontrados:**

| Cluster | Subsetores | K/L médio | W/L médio | I/Fat médio | Interpretação |
|---------|-----------|-----------|-----------|-------------|---------------|
| **C0** (n=1) | Brinquedos | R$ 49 mil | R$ 5.112 | **63,1%** | Outlier fiscal — mais da metade do faturamento vem de ICMS restituído |
| **C1** (n=16) | Bebidas, Borracha, Couros, Diversos, Editorial, **Eletroeletrônico**, Madeireiro, Mecânico, Metalúrgico, Mobiliário, Naval, Papel, Alimentícios, Relojoeiro, Têxtil, Vestuário | R$ 225 mil | R$ 4.259 | 5,7% | Diversificado — maioria do PIM, automação e dependência fiscal moderadas |
| **C2** (n=6) | Duas Rodas, Isqueiros, Mineral N. Met., Químico, Termoplástico, Ótico | R$ 867 mil | R$ 8.188 | 7,1% | Capital-intensivo — alta automação, altos salários |

**Achado relevante:** O **Eletroeletrônico** — maior subsetor do PIM em faturamento absoluto — classifica-se em C1 (diversificado), não em C2 (capital-intensivo). Motivo: seu K/L (≈ R$ 363 mil) é moderado na escala do PIM, abaixo da média de C2 (R$ 867 mil). O Eletroeletrônico é grande em *volume*, mas não é o mais capital-intensivo *por trabalhador*. Duas Rodas, Químico e Termoplástico investem proporcionalmente mais em capital por empregado.

**Figuras geradas:** `fig_validation_panel.png` (painel com 5 métricas de validação), `fig_clusters_2d_v2.png` (scatter PCA 2D), `fig_clusters_radar_v2.png` (radar dos perfis).

---

#### 15.3.2 Etapa 2 — DEA-BCC: Mensurando Eficiência

**Objetivo:** Calcular a eficiência relativa de cada subsetor-ano na conversão de incentivos fiscais em resultados econômicos.

**Modelo:** DEA BCC (Banker, Charnes & Cooper 1984) — VRS output-oriented. Permite retornos variáveis de escala, adequado quando os subsetores operam em escalas muito diferentes (CV do faturamento > 200%).

**Especificação:**

| | Variáveis | Interpretação |
|--|-----------|---------------|
| **Inputs** | ICMS restituído real ($I$) + CAPEX real ($K$) | O que o subsetor "consome" — incentivo fiscal + investimento produtivo |
| **Outputs** | Faturamento real ($Fat$) + Emprego SUFRAMA ($E$) | O que o subsetor "produz" — resultado econômico + geração de postos |

**Rule of thumb:** $n = 23 \geq 3 \times (2+2) = 12$ ✔️ (Cooper, Seiford & Tone 2007)

**Solver:** `scipy.optimize.linprog` (HiGHS). Cada LP resolvido individualmente por DMU-ano.

**Resultados globais:**

| Estatística | Valor |
|-------------|-------|
| Média θ_VRS | **0.821** |
| Mediana θ_VRS | **0.995** |
| DMUs na fronteira (θ ≥ 0.999) | **68 / 137 (50%)** |
| DMUs eficientes por ano | 9 a 13 (média ≈ 11 por cross-section) |

**Nota sobre 50% de eficientes:** Proporção alta, mas esperada em modelos BCC com 2 inputs + 2 outputs e n ≈ 23 por cross-section. O BCC cria muitas facetas na fronteira convexa, permitindo que DMUs com mix único de inputs/outputs sejam auto-eficientes. O modelo CRS (mais restritivo) produz média = 0.34 — discriminando muito mais. A eficiência de escala ($SE = \theta_{CRS}/\theta_{VRS}$) complementa a análise.

**Top performers (sempre na fronteira VRS):** Eletroeletrônico, Brinquedos, Diversos, Madeireiro, Têxtil, Duas Rodas — todos com θ = 1.000 em todos os anos.

**Bottom performers:** Mineral Não Metálico (θ = 0.341), Ótico (0.383), Couros (0.454), Vestuário (0.513), Químico (0.547) — persistentemente ineficientes.

**Metafronteira e Technology Gap Ratio (TGR):**

A metafronteira compara a fronteira de cada cluster com a fronteira global. O TGR mede quanto da ineficiência é "estrutural" (do cluster) vs. "operacional" (da DMU dentro do cluster).

| Cluster | TGR médio | Interpretação |
|---------|-----------|---------------|
| C0 (Brinquedos, n=1) | **1.000** | Singleto — fronteira de grupo = metafronteira (artefato) |
| C1 (Diversificado, n=16) | **0.990** | 1% de gap — domina a metafronteira |
| C2 (Capital-intensivo, n=6) | **0.719** | **28% de gap** — o mais distante da metafronteira |

**O que isso significa:** C1 (que inclui Eletroeletrônico, Diversos, Têxtil, Madeireiro — todos sempre eficientes) domina a fronteira global. C2, apesar de ter a maior automação (K/L), tem as DMUs menos eficientes (Mineral, Ótico, Químico). Alta automação sozinha não garante eficiência.

**Figuras geradas:** `fig_dea_scores.png`, `fig_dea_by_cluster.png`, `fig_frontier_scatter.png`, `fig_eff_vs_contextual.png`, `fig_tgr_evolution.png`.

---

#### 15.3.3 Etapa 3 — Índice de Malmquist: Dinâmica Temporal da Produtividade

**Objetivo:** Avaliar se a produtividade total dos fatores (PTF) dos subsetores melhorou ou piorou entre 2018 e 2023, e decompor essa variação em dois componentes: catching-up operacional (EC) e deslocamento da fronteira tecnológica (TC).

**Modelo:** Malmquist CRS (Färe et al. 1994). Usa CRS porque o VRS Malmquist gera infeasibility nos LPs cross-period (propriedade de cone do CRS garante feasibility).

**Resultados (média geométrica, transições válidas):**

| Componente | Valor | Interpretação |
|------------|-------|---------------|
| **M (Malmquist)** | **0.831** | **Declínio de 17% na PTF média** |
| **EC (Efficiency Change)** | **0.829** | DMUs se afastaram da fronteira (perda de catching-up) |
| **TC (Technical Change)** | **1.003** | Fronteira permaneceu estável (sem regressão tecnológica) |
| Transições válidas | 91 / 114 (80%) | 23 transições descartadas por infeasibility CRS |

**O que isso revela:** A queda de produtividade é **inteiramente** explicada por perda de eficiência técnica (EC < 1), *não* por regressão da fronteira tecnológica (TC ≈ 1). A "tecnologia disponível" não piorou — os subsetores é que estão subutilizando a capacidade existente. É uma perda de catching-up operacional, não de inovação.

**Subsetores com catching-up positivo:** Papel e Papelão (M = 1.28 — o melhor), Vestuário (M = 1.07) — estes melhoraram durante o período.

**Subsetores com forte declínio:** Dois subsetores com M < 0.50 — perderam mais de 50% de PTF relativa.

**3 DMUs excluídas:** Diversos, Madeireiro e Têxtil são sempre eficientes em todos os anos → transições undefined no Malmquist (limitação conhecida de Färe et al. 1994).

**Figuras geradas:** `fig_malmquist_decomp.png`, `fig_malmquist_ec_tc.png`, `fig_malmquist_evolution.png`.

---

#### 15.3.4 Etapa 4 — Simar-Wilson: O Que Explica as Diferenças de Eficiência

**Objetivo:** Identificar os determinantes da eficiência VRS. Por que alguns subsetores convertem incentivos em resultados melhor que outros?

**Problema técnico:** Os escores DEA (θ) são enviesados por construção — estimados relativamente às demais DMUs, com erro serial. OLS sobre θ produz inferência inconsistente. A solução é a regressão truncada com bootstrap (Simar & Wilson 2007, Algorithm #1), que:
1. Reconhece que θ ∈ (0, 1] é censurado (truncamento em 1)
2. Usa bootstrap (B = 2000 replicações) para construir intervalos de confiança válidos
3. Produz erros-padrão corrigidos para a autocorrelação do DEA

**Modelo estimado:**

$$\theta_{VRS} = f\left(\ln(I/Fat),\; \ln(K/L),\; \ln(W/L),\; D_{C0},\; D_{C2},\; t\right) + \varepsilon$$

Onde: $\ln(I/Fat)$ = log da dependência fiscal, $\ln(K/L)$ = log da automação, $\ln(W/L)$ = log do salário médio, $D_{C0}$ e $D_{C2}$ = dummies de cluster (C1 = referência), $t$ = tendência temporal linear.

**Resultados:**

| Variável | β | IC 95% Bootstrap | Significativo? |
|----------|---|-------------------|----------------|
| Constante | −2.184 | [−4.329, +0.505] | Não |
| **ln(I/Fat)** | **−0.139** | [−0.150, −0.049] | **Sim** ★ |
| **ln(K/L)** | **−0.508** | [−0.607, −0.296] | **Sim** ★ |
| **ln(W/L)** | **+1.105** | [+0.677, +1.389] | **Sim** ★ |
| Cluster 0 (Brinquedos) | −0.039 | [−0.572, +0.603] | Não |
| **Cluster 2 (Capital-intensivo)** | **−0.411** | [−0.695, −0.143] | **Sim** ★ |
| Tendência temporal | −0.006 | [−0.039, +0.036] | Não |

**4 variáveis significativas, 3 não significativas.** OLS confirma sinais e significância (R² = 0.541). Modelo estendido com COVID dummy (n.s.) e eficiência de escala (β = −0.483, p = 0.0002, R² = 0.628).

**Figuras geradas:** `fig_simar_wilson_coefs.png` (coeficientes com ICs bootstrap), `fig_eff_vs_contextual.png`.

---

### 15.4 Resultado Central: A Narrativa que Emerge dos Dados

Todos os resultados apontam na mesma direção. Cruzando as 4 técnicas, emerge uma narrativa coerente com 4 mensagens-chave:

**Mensagem 1 — Capital humano é o determinante mais forte da eficiência.**

O coeficiente de $\ln(W/L)$ é +1.105 — o maior em magnitude, significativo a 99% em ambos os métodos (SW e OLS). Subsetores que pagam salários mais altos (proxy de qualificação da mão-de-obra) são sistematicamente mais eficientes. Não é apenas correlação: o OLS com todos os controles (cluster, tendência, escala, COVID) confirma o efeito.

Isso é consistente com a teoria do efficiency wage (Shapiro & Stiglitz 1984): salários acima do mercado induzem maior esforço e atraem trabalhadores mais qualificados. Também é consistente com capital humano como fator produtivo (Becker 1964): qualificação amplifica a conversão de inputs em outputs.

**Mensagem 2 — Dependência fiscal tem efeito negativo sobre eficiência.**

$\ln(I/Fat)$ tem β = −0.139, significativo. Maior fração do faturamento coberta por incentivo ICMS → menor eficiência. Interpretação: subsetores que dependem proporcionalmente mais de incentivo fiscal enfrentam menor pressão por produtividade — possível **moral hazard** institucional. O incentivo generoso reduz o custo de ser ineficiente.

Este achado é especialmente relevante porque na especificação anterior (incentivo como nível absoluto $I$, não como razão $I/Fat$), o efeito do incentivo era **não significativo**. O uso de razões revelou o efeito que o nível absoluto escondia.

**Mensagem 3 — Automação isolada não garante eficiência.**

$\ln(K/L)$ tem β = −0.508, significativo. Mais capital por trabalhador, ceteris paribus, associa-se a **menor** eficiência VRS. Não é que investir em capital seja ruim — é que investir em capital **sem** a qualificação correspondente gera retornos decrescentes. Os subsetores de C2 (K/L = R$ 867 mil) têm a maior automação, mas TGR = 0.719 (28% de gap). Os eficientes são os de C1, que combinam automação moderada (R$ 225 mil) com salários adequados.

O sinal negativo de K/L, combinado com o sinal positivo de W/L, sugere que a eficiência é função do **equilíbrio** entre capital físico e capital humano, não da maximização de apenas um deles.

**Mensagem 4 — A produtividade está caindo por subutilização, não por atraso tecnológico.**

Malmquist M = 0.831 (queda de 17%), EC = 0.829, TC = 1.003. A fronteira tecnológica se manteve estável — mas os subsetores estão se afastando dela. É uma perda operacional, não estrutural. A tendência temporal no Simar-Wilson é não significativa, corroborando: não há trend de piora/melhora sistêmica.

---

### 15.5 Confronto com a Hipótese Original → Hipótese Revisada

| Hipótese Original | Resultado Empírico | Veredicto |
|-------------------|--------------------|-----------|
| Maior automação (K/L) → maior eficiência em faturamento | β(K/L) = −0.508, significativo, **negativo** | **REJEITADA** |
| Maior automação → menor eficiência em emprego (trade-off) | DEA inclui emprego como output → modelo captura ambos simultaneamente | **Parcialmente testada** — o trade-off existe mas é mediado por W/L |

A hipótese deve ser **revisada**, não abandonada. Os dados sugerem uma formulação mais precisa:

> **Hipótese Revisada:** A eficiência dos subsetores do PIM na conversão de incentivos fiscais é função do equilíbrio entre capital físico (K/L) e capital humano (W/L). Subsetores que combinam investimento produtivo com qualificação da mão-de-obra apresentam maior eficiência, enquanto o excesso de capital relativo sem qualificação correspondente gera retornos decrescentes. A intensidade de dependência fiscal (I/Fat) associa-se negativamente à eficiência, sugerindo que incentivos generosos podem reduzir pressão por produtividade (moral hazard institucional).

---

### 15.6 Coerência Interna — Os Resultados se Confirmam Mutuamente

| Evidência A | Evidência B | Coerência |
|-------------|-------------|-----------|
| SW: K/L negativo (β = −0.51) | DEA: C2 (alto K/L) tem θ_VRS médio menor, TGR = 0.72 | ✅ |
| SW: W/L positivo (β = +1.11) | Top performers (Eletroeletrônico, Diversos, Têxtil) geralmente têm W/L acima da mediana | ✅ |
| SW: Cluster 2 negativo (β = −0.41) | TGR C2 = 0.72 (o mais distante da metafronteira) | ✅ |
| Malmquist: TC ≈ 1 | SW: tendência temporal não significativa | ✅ |
| Malmquist: EC = 0.83 | Perda operacional sem mudança estrutural | ✅ |
| SW: I/Fat negativo | Brinquedos (I/Fat = 63%) é outlier fiscal e singleto | ⚠️ Tensão (n=1, potência zero) |

5 de 6 cruzamentos são internamente coerentes. O único ponto de tensão (Brinquedos) é explicável pelo fato de ser singleto.

---

### 15.7 Limitações Conhecidas e Decisões Pendentes

#### Limitações do modelo

1. **Dimensionalidade DEA:** 2I+2O com n=23 → regra de ouro atende, mas 50% de eficientes sugere baixa discriminação VRS. Alternativa: super-efficiency ou redução para 1 output.

2. **CAPEX como fluxo, não estoque:** K deveria idealmente ser estoque de capital (depreciado). CAPEX anual é proxy ruidosa — ano sem investimento ≠ ausência de capital produtivo.

3. **ICMS ≈ 25% do custo fiscal total:** Incentivos federais (IPI, II, IRPJ, PIS/COFINS) representam ~75% do benefício. I/Fat subestima a exposição fiscal real. É a única proxy observável por subsetor.

4. **Painel curto (6 anos):** 2018-2023 inclui choque COVID. Tendência pode estar contaminada.

5. **Endogeneidade potencial de W/L:** Subsetores eficientes pagam mais *porque* são eficientes? Causalidade reversa possível. Simar-Wilson mitiga (bootstrap), mas não resolve. IV difícil com n=23.

6. **Cluster singleto (Brinquedos):** C0 com 1 membro tem potência estatística zero. TGR = 1 é artefato.

#### Decisões para o orientador

| Questão | Recomendação |
|---------|--------------|
| 50% de DMUs eficientes — aceitável? | Aceitar e documentar como limitação BCC. CRS discrimina (média 0.34), SE complementa. |
| Eletroeletrônico em C1 — muda a tese? | Sim, reformular hipótese (§15.5). Variáveis-razão são mais corretas. |
| Endogeneidade de W/L | Documentar como limitação. IV impraticável com n e T. |
| 3 DMUs sem Malmquist | Excluir e documentar (limitação Färe 1994). |
| Simar-Wilson Algorithm #1 vs #2 | Manter #1 + bootstrap IC. #2 seria mais complexo sem ganho substancial para TCC. |

---

### 15.8 Implicações para Política Pública

Os resultados deste trabalho, se confirmados e aceitos pelo orientador, sugerem 4 direções para a política de incentivos da ZFM:

1. **Incentivo condicional a produtividade:** I/Fat negativo e significativo → incentivos deveriam ser vinculados a contrapartidas de produtividade (metas de faturamento/emprego), não concedidos automaticamente.

2. **Investimento em capital humano como alavanca:** W/L é o preditor mais forte da eficiência (β = +1.105). Programas de qualificação profissional no PIM podem ter retorno superior a desonerações fiscais adicionais.

3. **Diagnóstico diferenciado por cluster:** C2 (capital-intensivo) com TGR = 0.72 precisa de atenção específica. Mineral Não Metálico (θ = 0.34), Ótico (0.38) e Químico (0.55) são persistentemente ineficientes — diagnóstico individual necessário.

4. **Monitoramento contínuo:** Declínio de 17% na PTF (M = 0.831) é sinal de alerta. A Fronteira não regrediu (TC ≈ 1) — os subsetores estão simplesmente operando abaixo do potencial. Subutilização de capacidade instalada.

---

### 15.9 Contribuição para a Literatura

| Aspecto | Contribuição |
|---------|-------------|
| **Metodologia** | Primeiro estudo a combinar DEA + K-means + Malmquist + metafronteira + Simar-Wilson para subsetores do PIM nesta granularidade |
| **Dados** | Painel SUFRAMA 2018-2023 com salários extraídos, deflacionado, câmbio PTAX via API — replicável |
| **Achado empírico** | I/Fat negativo e significativo — uso de razões (não níveis) revelou efeito que a especificação anterior escondia |
| **Achado de política** | Capital humano > incentivo fiscal como determinante de eficiência — alinha com críticas da CPI da ZFM (2025) e relatórios do TCU |

---

### 15.10 Narrativa para o TCC (parágrafo-síntese)

> Este trabalho avalia a eficiência relativa dos 23 subsetores industriais do Polo Industrial de Manaus na conversão de incentivos fiscais em faturamento e empregos, utilizando DEA-BCC output-oriented no período 2018-2023. A clusterização K-means (k* = 3, Silhouette = 0.501) revela três perfis estruturais: um outlier de dependência fiscal desproporcional (Brinquedos, I/Fat = 63%), um cluster diversificado de 16 subsetores (incluindo Eletroeletrônico) e um cluster capital-intensivo de 6 subsetores. A regressão Simar-Wilson com bootstrap (B = 2000) identificou quatro determinantes significativos da eficiência: a dependência fiscal (I/Fat) tem efeito negativo (β = −0.14), sugerindo moral hazard institucional; a automação (K/L) também negativa (β = −0.51), consistente com retornos decrescentes de capital isolado; o salário médio (W/L) é positivo e o preditor mais forte (β = +1.11), indicando que capital humano é mais determinante que capital físico; e o pertencimento ao cluster capital-intensivo reduz eficiência (β = −0.41). O Índice de Malmquist registra declínio de 17% na PTF média (M = 0.831) inteiramente explicado por perda de catching-up operacional (EC = 0.829), sem regressão da fronteira tecnológica (TC = 1.003). Os resultados sugerem que a política de incentivos da ZFM seria mais efetiva se vinculada a contrapartidas de qualificação profissional e produtividade, em vez de concessão automática baseada na localização.

---

## 16. PROTOCOLO FINAL DE ROBUSTEZ METODOLÓGICA

### 16.1 Princípio de decisão (mínimo-máximo)

Não rodar todas as combinações possíveis de DEA/Malmquist. Rodar apenas o conjunto mínimo que responde às perguntas críticas da banca com rastreabilidade técnica.

Critério: incluir nova especificação apenas se ela responder uma pergunta concreta de avaliação e se não deslocar a pergunta original de pesquisa.

### 16.2 Pacote mínimo obrigatório (versão final)

| Bloco | Especificação | Papel |
|------|---------------|-------|
| DEA estático principal | BCC/VRS (output-oriented) | Eficiência técnica relativa principal |
| DEA comparativo | CCR/CRS | Eficiência de escala (complemento) |
| Malmquist principal | CRS (Färe et al.) | Dinâmica de produtividade (M, EC, TC) |
| Decomposição adicional | PEC (VRS) e SC = EC/PEC | Separar efeito puro vs escala ao longo do tempo |
| 2º estágio | Simar-Wilson bootstrap | Determinantes da eficiência |

### 16.3 Texto obrigatório para evitar crítica de incongruência

Inserir no capítulo de metodologia e repetir resumidamente em resultados:

1. DEA estático usa VRS por heterogeneidade de escala entre subsetores do PIM.
2. Malmquist operacional usa CRS para manter comparabilidade intertemporal e evitar infeasibility cross-period.
3. A informação de escala não foi ignorada: é recuperada pela decomposição PEC/SC e pela análise de `scale_eff` no DEA estático.

### 16.4 Quadro de alternativas metodológicas (para banca)

| Alternativa | Por que considerada | Por que não é principal no TCC |
|-------------|---------------------|---------------------------------|
| SFA (fronteira estocástica) | Paramétrica, separa ineficiência e ruído | Exige forma funcional e hipóteses distributivas mais fortes; foco aqui é comparação relativa não paramétrica com amostra curta |
| Malmquist VRS completo como principal | Permite leitura pura de eficiência | Maior instabilidade/infeasibility intertemporal na amostra atual; mantido como complementar (PEC/SC) |
| Expansão para múltiplos modelos de cluster | Robustez de segmentação | Custo/benefício desfavorável para prazo do TCC; validação interna atual já documentada com 5 critérios |

### 16.5 Tabela de robustez enxuta (resultado para defesa)

| Bloco | Especificação | Resultado-chave | Leitura de robustez |
|-------|---------------|-----------------|---------------------|
| DEA principal | BCC/VRS, output-oriented | Média θ_VRS = 0.821; 68/137 na fronteira | Resultado central de eficiência relativa |
| DEA comparativo | CCR/CRS | Média θ_CRS ≈ 0.34 (mais restritivo) | Confirma que alta eficiência no VRS não elimina problema de escala |
| Malmquist (principal) | CRS | M=0.831, EC=0.829, TC=1.003 | Queda de PTF vem de eficiência, não de regressão tecnológica |
| Decomposição EC | PEC/SC | PEC=0.982, SC=0.844 | Perda de escala é o principal componente da queda de EC |
| 2º estágio | Simar-Wilson + OLS comparativo | Sinais consistentes para I/Fat, K/L, W/L, C2 | Estabilidade de sinal fortalece inferência substantiva |

**Mensagem de banca (1 frase):** O núcleo empírico se mantém sob especificações comparativas essenciais; diferenças entre modelos alteram magnitude, não o sentido dos principais achados.

---

## 17. GUIA DE TRANSCRIÇÃO PARA O TCC ESCRITO (CAPÍTULOS 1-7)

> Esta seção é um mapa de redação: o que cada capítulo deve conter, em que ordem e quais pontos não podem faltar para manter congruência total com o pipeline de dados.

### 17.1 Capítulo 1 — Introdução (versão final)

Deve conter obrigatoriamente:

1. Problema: heterogeneidade da eficiência de incentivos na ZFM.
2. Lacuna: literatura usa DEA ou cluster isoladamente; combinação sequencial com dinâmica temporal é rara.
3. Objetivo geral e objetivos específicos (já definidos na Seção 1.3 do mestre).
4. Contribuição prática: orientação de política pública baseada em eficiência observada por subsetor.

Não esquecer:

1. Delimitação temporal (2018-2023).
2. Delimitação de unidade (23 subsetores).
3. Delimitação de inferência (evidência associativa, não causal forte).

### 17.2 Capítulo 2 — Referencial Teórico

Organização recomendada:

1. Incentivos fiscais e desenvolvimento regional (ZFM).
2. Eficiência produtiva e DEA (fundamentos, VRS/CRS).
3. Produtividade dinâmica e Malmquist (EC/TC/PEC/SC).
4. Segmentação setorial com clusterização.
5. Segundo estágio e inferência em DEA (Simar-Wilson).
6. Bloco ambiental (trade-off desenvolvimento vs externalidades).

Ponto de atenção:

1. Citar explicitamente por que o desenho escolhido é apropriado para amostra pequena e dados administrativos.

### 17.3 Capítulo 3 — Dados e Contexto

Obrigatório:

1. Proveniência variável a variável (já pronta em §15.2).
2. Regras de limpeza/transformação (deflação, câmbio, razões, exclusão de zero estrutural).
3. Justificativa SUFRAMA vs RAIS.
4. Mapa final do painel (137 obs, 30 colunas).

### 17.4 Capítulo 4 — Metodologia

Obrigatório:

1. Pipeline completo (K-means → DEA → Metafronteira → Malmquist → Simar-Wilson).
2. Justificativa formal VRS/CRS por etapa.
3. Especificações matemáticas mínimas de cada modelo.
4. Nota de limitações metodológicas ex-ante.
5. Quadro de alternativas metodológicas descartadas.

---

## 18. CAPÍTULO 5 — RESULTADOS (ROTEIRO PRONTO)

Estrutura final recomendada:

1. **5.1 Painel e descritivas**
2. **5.2 Validação K-means**
3. **5.3 DEA estático (VRS/CRS/scale_eff)**
4. **5.4 Malmquist e decomposição completa (M, EC, TC, PEC, SC)**
5. **5.5 Metafronteira (TGR)**
6. **5.6 Simar-Wilson e robustez**
7. **5.7 Síntese dos achados empíricos**

Checklist de conteúdo obrigatório:

1. Reportar resultados principais com número e interpretação econômica.
2. Separar claramente resultado estatístico, interpretação e implicação.
3. Destacar o que confirma e o que rejeita a hipótese original.
4. Inserir quadro "Achado → Evidência → Implicação".

Frases que não podem faltar (em essência):

1. "A queda de produtividade é majoritariamente explicada por eficiência (catching-up), não por regressão tecnológica."
2. "Automação isolada não garante eficiência; o efeito depende da combinação com capital humano."
3. "Dependência fiscal relativa associa-se negativamente à eficiência observada."

---

## 19. CAPÍTULO 6 (DISCUSSÃO) E 7 (CONCLUSÃO)

### 19.1 Capítulo 6 — Discussão

Sequência recomendada:

1. Confronto com literatura nacional/internacional.
2. Interpretação dos mecanismos (I/Fat, K/L, W/L, cluster).
3. Escala vs técnica (leitura PEC/SC + scale_eff).
4. Implicações de policy para SUFRAMA/Estado.
5. Limitações e riscos de interpretação.

Não esquecer:

1. Não extrapolar causalidade além do desenho.
2. Tratar Brinquedos (singleto) como caso especial sem generalização.
3. Documentar sensibilidade de resultados para amostra curta.

### 19.2 Capítulo 7 — Conclusão

Obrigatório:

1. Responder diretamente a pergunta de pesquisa em 1 parágrafo.
2. Listar 3-5 contribuições do estudo.
3. Listar limites sem fragilizar o núcleo dos achados.
4. Agenda futura em duas trilhas:
   - trilha acadêmica (extensões metodológicas)
   - trilha de política pública (monitoramento anual por subsetor)

---

## 20. SEÇÃO AMBIENTAL — METODOLOGIA DEFINITIVA

### 20.1 Decisão metodológica final

Sim, a estratégia está definida para o TCC:

1. Criar **proxy ambiental qualitativa/categórica por subsetor** (baixo/médio/alto) com base em literatura e critério transparente.
2. Usar essa proxy **na discussão e em tabelas de cruzamento** (eficiência e TGR por classe ambiental).
3. **Não inserir a proxy no DEA principal** nesta versão final do TCC.

### 20.2 O que esta decisão resolve

1. Atende a recomendação do orientador sobre o dilema desenvolvimento vs ambiente.
2. Mantém comparabilidade e estabilidade do motor empírico já validado.
3. Evita inflar dimensionalidade do DEA com variável construída e potencialmente ruidosa.

### 20.3 Protocolo mínimo da proxy ambiental

Cada subsetor deve ter:

1. Classe ambiental (baixo/médio/alto).
2. Critério textual de classificação.
3. Referência bibliográfica/documental (ao menos uma fonte verificável).
4. Nota de limite (proxy qualitativa, não medição direta de emissões).

Arquivos operacionais para execução do anexo:

- `outputs/tables/tab_proxy_ambiental_template.csv` (template base)
- `outputs/tables/tab_proxy_ambiental_v1.csv` (v1 preenchida: 23/23 subsetores classificados)
- `outputs/tables/base_consolidada_classificacao_ambiental_subsetor.csv` (nome academico oficial: BCCAS)
- `outputs/tables/tabela_anexo_classificacao_ambiental.md` (tabela final pronta para anexo)
- `outputs/tables/cruzamento_ambiental_eficiencia_subsetor.csv` (cruzamento subsetor: classe ambiental x eficiencia x TGR)
- `outputs/tables/cruzamento_ambiental_eficiencia_classe.csv` (resumo por classe ambiental para discussao)
- `outputs/tables/texto_discussao_ambiental_final.md` (paragrafos prontos para Cap. 6)
- `outputs/tables/texto_metodo_anexo_proxy_final.md` (bloco metodologico pronto para anexo)
- `outputs/tables/nomenclatura_academica_artefatos_ambientais.md` (padrao de nomenclatura do TCC)
- `outputs/tables/tab_proxy_ambiental_reclassificacoes.csv` (trilha de auditoria interna)
- `deep-research-report-clean.md` (relatorio de pesquisa limpo, sem marcadores tecnicos)

### 20.4 Como reportar no texto

1. No corpo principal: 1 subseção em Discussão com tabela resumo e interpretação.
2. No anexo: tabela completa subsetor-a-subsetor + critérios + referências.
3. Na conclusão: usar a proxy como reforço interpretativo, não como base de inferência causal forte.

### 20.5 Dúvidas acadêmicas remanescentes (controladas)

As dúvidas restantes não impedem a execução:

1. Granularidade ambiental ideal seria por firma/planta; indisponível na base pública atual.
2. Classificação por subsetor pode mascarar heterogeneidade interna.
3. Para artigo futuro, avaliar extensão com dados energéticos/emissões e modelos com undesirable outputs.

Conclusão prática: **metodologia ambiental do TCC está fechada para execução**, com limitações explicitadas.

---

## 21. RASCUNHO PRONTO — CAPÍTULO 5 (RESULTADOS)

> Uso desta seção: transcrever e adaptar para o documento final do TCC (Capítulo 5), mantendo numeração de tabelas/figuras e estilo acadêmico da banca.

### 21.1 Estrutura do painel e estatísticas descritivas

O painel final contém 137 observações para 23 subsetores no período 2018-2023, com base monetária em preços constantes de 2023. A exclusão de Couros e Similares em 2018 decorre de zero estrutural de operação (faturamento, emprego e CAPEX iguais a zero), não de dado ausente. A distribuição das variáveis revela elevada heterogeneidade produtiva no PIM, com forte concentração de faturamento e incentivos em poucos subsetores.

As estatísticas descritivas mostram assimetria elevada em Faturamento, Emprego, CAPEX e ICMS, coerente com a coexistência de subsetores de grande escala e subsetores de nicho. O indicador I/Fat apresenta cauda longa, com Brinquedos como outlier de dependência fiscal. Em termos de implicação analítica, a heterogeneidade observada justifica a estratégia de segmentação prévia por K-means antes da estimação de fronteiras de eficiência.

### 21.2 Validação da segmentação K-means

Foram testados cinco critérios internos para seleção de k (Elbow, Silhouette, Calinski-Harabasz, Davies-Bouldin e Gap Statistic). Não houve consenso entre os métodos, com votos divergentes para diferentes valores de k. Na ausência de maioria, aplicou-se a regra de desempate pelo maior Silhouette médio, resultando em k*=3 e Silhouette=0.501.

O valor de Silhouette indica estrutura de agrupamento razoável para a amostra disponível, e os testes de estabilidade por bootstrap (ARI) confirmam robustez moderada da partição. A segmentação final resultou em três perfis: C0 (outlier fiscal, singleto), C1 (diversificado) e C2 (capital-intensivo). Um resultado substantivo relevante foi a classificação do Eletroeletrônico em C1, indicando que seu porte absoluto não se traduz em maior intensidade de capital por trabalhador.

### 21.3 Eficiência estática via DEA (VRS/CRS)

O modelo principal DEA (BCC, VRS, orientado a outputs) foi estimado com Inputs=(ICMS, CAPEX) e Outputs=(Faturamento, Emprego SUFRAMA). A média de eficiência VRS foi 0.821, com mediana elevada e 68 observações na fronteira (50%). Esse padrão é compatível com modelos VRS em amostras pequenas e com múltiplos outputs, exigindo leitura complementar por eficiência de escala.

A estimação comparativa em CRS mostrou maior restrição (média de eficiência substancialmente inferior), reforçando que parcela relevante da ineficiência observada está associada a escala e não apenas a gestão técnica. A decomposição por cluster evidenciou desvantagem estrutural do C2, consistente com os resultados de metafronteira.

### 21.4 Dinâmica de produtividade (Malmquist)

No período analisado, o índice de Malmquist indicou queda de produtividade total dos fatores (M=0.831). A decomposição mostrou EC=0.829 e TC=1.003, sinalizando que a perda de desempenho está associada ao afastamento relativo da fronteira, e não a retrocesso tecnológico agregado.

Com a decomposição adicional solicitada pelo orientador, obteve-se PEC=0.982 e SC=0.844. Isso indica que o principal componente da perda em EC foi escala, não eficiência pura. A leitura por cluster confirma o padrão: C2 exibe deterioração mais forte em escala dinâmica (SC mais baixo), apesar de não apresentar perda equivalente em eficiência pura.

### 21.5 Metafronteira e gap tecnológico (TGR)

Os resultados de TGR indicam diferença clara entre grupos tecnológicos. O cluster C1 apresenta TGR próximo da metafronteira, enquanto C2 mantém gap expressivo e persistente. Essa evidência reforça que comparações agregadas do PIM ocultam heterogeneidade tecnológica relevante para avaliação de política pública.

Do ponto de vista interpretativo, o TGR permite separar dois diagnósticos: ineficiência dentro do cluster (problema gerencial/técnico) e distância entre fronteiras de cluster (problema tecnológico/estrutural). Essa distinção é central para recomendações de política segmentadas.

### 21.6 Determinantes da eficiência (Simar-Wilson)

A regressão truncada com bootstrap indicou quatro resultados principais: (i) I/Fat com efeito negativo e significativo sobre eficiência, (ii) K/L também negativo e significativo, (iii) W/L positivo e com maior magnitude, e (iv) dummy de C2 negativa e significativa. Tendência temporal e C0 não foram significativos.

Em robustez, a comparação com OLS manteve os sinais das variáveis centrais, com diferenças principalmente de magnitude. O conjunto de resultados sustenta a interpretação de que capital humano (W/L) é o fator mais fortemente associado à eficiência, enquanto dependência fiscal relativa e automação isolada associam-se a desempenho inferior.

### 21.7 Síntese integrada dos achados

Tomados em conjunto, os resultados convergem para quatro mensagens centrais: (1) há heterogeneidade estrutural relevante entre subsetores; (2) a produtividade agregada caiu no período por perda de eficiência, com componente de escala predominante; (3) capital humano se associa positivamente à eficiência; e (4) maior dependência fiscal relativa se associa negativamente à eficiência.

Essas evidências justificam uma leitura de política pública baseada em condicionalidade e segmentação: incentivos devem ser calibrados por perfil produtivo e acompanhados por metas explícitas de desempenho, evitando desenho uniforme para subsetores tecnologicamente distintos.

---

## 22. RASCUNHO PRONTO — CAPÍTULO 6 (DISCUSSÃO) E CAPÍTULO 7 (CONCLUSÃO)

### 22.1 Capítulo 6 — Discussão (texto-base)

Os resultados deste estudo sugerem que a eficiência de conversão dos incentivos fiscais no PIM é fortemente condicionada por heterogeneidade estrutural entre subsetores. A segmentação por K-means mostrou que diferenças de intensidade de capital, perfil salarial e dependência fiscal não são marginais: elas definem grupos com fronteiras tecnológicas distintas e trajetórias de produtividade diferentes.

No primeiro eixo de discussão, a evidência de I/Fat negativo e significativo indica que maior dependência fiscal relativa se associa a menor eficiência observada. Esse resultado é coerente com interpretações de incentivo mal calibrado, em que a proteção fiscal reduz pressão competitiva por ganhos de produtividade. Do ponto de vista de desenho de política, isso reforça a necessidade de condicionalidades explícitas e monitoráveis.

No segundo eixo, o sinal negativo de K/L, combinado ao sinal positivo e robusto de W/L, aponta que automação isolada não garante eficiência. O padrão empírico sugere complementaridade entre capital físico e capital humano: aumentos de intensidade de capital sem qualificação correspondente tendem a gerar desequilíbrios e perda de eficiência relativa.

No terceiro eixo, a análise dinâmica mostrou queda de PTF no período, com TC estável e deterioração de EC. A decomposição adicional PEC/SC esclarece que o principal vetor da perda foi escala. Essa conclusão é particularmente relevante para o debate de política industrial, pois desloca o foco de “falta de tecnologia” para “arranjo produtivo e escala operacional”.

No quarto eixo, a leitura de metafronteira confirma que parte da desvantagem é tecnológica entre grupos, e não apenas gerencial dentro dos grupos. Assim, recomendações uniformes para todos os subsetores tendem a ser ineficientes. A política deve distinguir problemas de gestão, escala e lacuna tecnológica.

### 22.2 Seção ambiental da Discussão (texto-base)

A dimensão ambiental foi incorporada de forma parcimoniosa e metodologicamente prudente, por meio de proxy qualitativa de risco ambiental por subsetor, ancorada em literatura e documentação setorial. A decisão de manter essa variável fora do DEA principal preserva a consistência do motor empírico e evita inflar o modelo com medida construída de alta incerteza observacional.

Com essa abordagem, a contribuição ambiental é interpretativa e de policy, não de inferência causal forte. O cruzamento entre eficiência econômica e classe ambiental permite discutir a alocação de incentivos sob ótica de dupla materialidade: retorno econômico e risco de externalidade negativa. Em termos práticos, a implicação é que instrumentos fiscais podem ser progressivamente condicionados não apenas a produção e emprego, mas também a compromissos ambientais verificáveis.

Na consolidacao da Base Consolidada de Classificacao Ambiental por Subsetor (BCCAS), a distribuicao final ficou em Alto=10, Medio=12 e Baixo=1 subsetor. No resumo de cruzamento por classe (`cruzamento_ambiental_eficiencia_classe.csv`), a media de eficiencia VRS foi 0.788 para Alto, 0.831 para Medio e 0.961 para Baixo; para TGR, as medias foram 0.889 (Alto), 0.940 (Medio) e 0.985 (Baixo). A leitura substantiva e que nao ha determinismo simples entre risco ambiental potencial e eficiencia economica, reforcando a interpretacao de dupla materialidade e a necessidade de condicionalidades calibradas por perfil setorial.

O resultado da classe Baixo deve ser tratado com cautela analitica, pois contem apenas um subsetor na configuracao consolidada. Portanto, o foco interpretativo principal deve recair na comparacao Alto vs Medio e nos casos com reclassificacao conservadora (8 subsetores), documentados em arquivo de auditoria.

Limitações permanecem explícitas: ausência de dados diretos de emissões por subsetor, heterogeneidade interna dentro de cada grupo industrial e potencial erro de classificação em proxies categóricas. Mesmo assim, a estratégia é defensável para o escopo de TCC e compatível com agenda de aprofundamento em artigo posterior.

### 22.3 Limitações e validade externa (texto-base)

Entre as principais limitações, destacam-se: painel curto (2018-2023), zero estrutural de um subsetor no início da série, uso de CAPEX anual como proxy de capital e não de estoque de capital, e indisponibilidade de incentivos federais desagregados por subsetor para incorporar integralmente o custo fiscal total no modelo principal.

Em termos de validade externa, os resultados são diretamente aplicáveis ao PIM no recorte temporal estudado. Generalizações para outros polos industriais exigem cautela e replicação com estrutura de dados equivalente.

### 22.4 Capítulo 7 — Conclusão (texto-base)

Este estudo avaliou a eficiência relativa dos subsetores do PIM na conversão de incentivos fiscais em faturamento e emprego no período 2018-2023, combinando segmentação produtiva, fronteiras de eficiência estática, dinâmica de produtividade e inferência de determinantes.

A evidência empírica convergiu para três conclusões centrais: (i) a heterogeneidade produtiva é determinante para entender eficiência na ZFM; (ii) a queda de produtividade no período decorre principalmente de perda de eficiência com componente de escala predominante; e (iii) capital humano se associa positivamente à eficiência, enquanto dependência fiscal relativa e automação isolada se associam negativamente.

Do ponto de vista de política pública, os resultados sustentam a recomendação de migrar de uma lógica uniforme de incentivo para uma lógica condicional e segmentada, com metas de desempenho e monitoramento contínuo por perfil produtivo. A incorporação da dimensão ambiental por proxy qualitativa amplia a utilidade do diagnóstico para decisões de médio prazo.

Como agenda futura, recomenda-se: (1) ampliar a série temporal; (2) incorporar medidas setoriais de energia/emissões para refinar a dimensão ambiental; (3) testar extensões metodológicas com fronteiras ambientais (undesirable outputs) em versão de artigo.

---

## 23. PROTOCOLO DE PREENCHIMENTO — ANEXO DA PROXY AMBIENTAL

### 23.1 Objetivo

Garantir que a classificação ambiental por subsetor seja auditável, replicável e defensável em banca.

### 23.2 Arquivo-base

Usar o arquivo `outputs/tables/base_consolidada_classificacao_ambiental_subsetor.csv` como base principal do TCC e manter os arquivos tecnicos para rastreabilidade.

Campos obrigatórios por linha:

1. `classe_ambiental`: Baixo, Médio, Alto.
2. `score_ambiental`: 1, 2, 3 (respectivamente).
3. `criterio_classificacao`: texto curto, objetivo, sem ambiguidade.
4. `referencia_base`: fonte verificável (artigo, relatório técnico ou documento institucional).

### 23.3 Regra de classificação (versão TCC)

Usar abordagem qualitativa por evidência textual, com foco em vetor predominante de externalidade:

1. Intensidade energética e/ou térmica.
2. Potencial de emissões e resíduos perigosos.
3. Potencial de e-waste, solventes e efluentes.
4. Pressão sobre recursos naturais (quando aplicável).

### 23.4 Regras de qualidade

1. Não classificar sem referência.
2. Não usar linguagem vaga (ex.: "parece mais poluente").
3. Em caso de dúvida entre duas classes, adotar a mais conservadora e registrar justificativa em `observacao`.
4. Se houver evidência conflitante, registrar duas fontes e explicar o critério de desempate.

### 23.5 Entrega mínima para fechar o anexo

1. 23/23 subsetores classificados.
2. 23/23 com referência preenchida.
3. Tabela final exportada para o anexo textual.
4. Parágrafo metodológico curto no Cap. 6 explicando que a proxy é interpretativa e não entra no DEA base.

### 23.6 Status atual (execução)

1. Classificacao concluida para 23/23 subsetores na base consolidada BCCAS.
2. Distribuição atual (regra conservadora): Médio = 12, Alto = 10, Baixo = 1.
3. Reclassificacoes registradas: 8 subsetores (arquivo de auditoria dedicado).
4. Cruzamento com eficiência/TGR concluído (por subsetor e por classe).
5. Próxima validação: revisão bibliográfica fina por subsetor (prioridade em classes Alto e setores heterogêneos).

## 24. STATUS EXECUTIVO DO PLANO GERAL (FECHAMENTO)

### 24.1 Estágio atual do projeto

1. **Motor empírico principal:** concluído e validado (pipeline 01→11 executado, sem bloqueio metodológico aberto).
2. **Bloco ambiental do TCC:** concluído em base consolidada (BCCAS), com anexo e cruzamentos prontos.
3. **Rascunhos de escrita final (Cap. 5, 6 e 7):** prontos em versão base, pendentes de edição final no texto da monografia.

### 24.2 Percentual de conclusão (estimativa operacional)

1. **Concluído:** ~88%
2. **Pendente crítico para banca:** ~12%

### 24.3 Pendências para encerramento do TCC

1. Consolidar redação final dos Capítulos 5, 6 e 7 no documento oficial.
2. Revisar e enxugar Capítulos 1-4 para coerência total com o modelo final.
3. Fechar Resumo e Abstract na versão final.
4. Revisão ABNT/UFPB completa (citações, referências, listas e formatação).
5. Revisão final com orientador (foco em narrativa, limites e recomendações de policy).

### 24.4 Regra de comunicação no texto final

No texto acadêmico, usar sempre o nome **Base Consolidada de Classificação Ambiental por Subsetor (BCCAS)** e evitar linguagem de versionamento interno (`v1`, `v2`) fora de anexos técnicos de auditoria.

---

## 25. MATRIZ DE RASTREABILIDADE DA ESCRITA (AFIRMACAO -> EVIDENCIA -> ARQUIVO)

### 25.1 Regra de uso

Cada afirmacao do texto final (Cap. 5, 6 e 7) deve apontar para ao menos uma evidencia empirica rastreavel em arquivo. Se nao houver evidencia direta, a afirmacao nao entra no corpo principal.

### 25.2 Matriz minima obrigatoria

| Afirmacao que pode entrar no texto | Evidencia numerica minima | Tabela/Figura de suporte | Arquivo-fonte rastreavel | Limite inferencial explicito |
|---|---|---|---|---|
| O painel final possui 137 observacoes e 23 subsetores (2018-2023) | contagem de linhas e subsetores unicos | Tabela de painel/descritivas | `data/processed/painel_subsetor_ano.csv` | Descreve cobertura da amostra; nao implica representatividade para fora do PIM |
| A estrutura produtiva e heterogenea entre subsetores | dispersao em Fat, E, K, I/Fat + concentracao | Tabelas descritivas + figura de concentracao | `outputs/tables/tab_descritivas.csv`; `outputs/figures/fig_concentracao_pim.png` | Heterogeneidade observada no painel; nao mede causalidade |
| O modelo K-means final adota k*=3 | validacao interna e desempate por Silhouette | Tabelas de validacao + painel grafico | `outputs/tables/tab_kmeans_validation.csv`; `outputs/tables/tab_gap_statistic.csv`; `outputs/tables/tab_bootstrap_stability.csv`; `outputs/figures/fig_validation_panel.png` | Regra de selecao metodologica; nao e verdade universal de clusterizacao |
| C2 e o cluster mais capital-intensivo | K/L medio por cluster | Tabela de perfil de clusters | `outputs/tables/tab_perfil_clusters_v2.csv` | Comparacao relativa dentro da amostra |
| Eficiência VRS media e 0.821 | media dos escores VRS no painel | Tabela resumo DEA | `outputs/tables/tab_dea_summary.csv`; `data/processed/dea_scores.csv` | Eficiência relativa ao conjunto de DMUs, nao absoluta |
| C2 apresenta maior gap tecnologico (TGR menor) | TGR medio por cluster | Tabela de metafronteira + figura de evolucao TGR | `outputs/tables/tab_metafrontier_tgr.csv`; `outputs/figures/fig_tgr_evolution.png` | Gap relativo entre fronteiras estimadas |
| A PTF caiu no periodo (M=0.831) | media geometrica do Malmquist | Tabela Malmquist + figura de decomposicao | `outputs/tables/tab_malmquist_summary.csv`; `outputs/figures/fig_malmquist_decomp.png` | Leitura restrita a transicoes validas (91/114) |
| A queda de PTF vem de EC, com TC estavel | EC<1 e TC~1 | Tabela Malmquist + figura EC vs TC | `outputs/tables/tab_malmquist_summary.csv`; `outputs/figures/fig_malmquist_ec_tc.png` | Nao implica ausencia de mudanca tecnologica micro por firma |
| A perda em EC e majoritariamente escala (SC<1, PEC proximo de 1) | valores de PEC e SC reportados | Tabela Malmquist (decomposicao) | `outputs/tables/tab_malmquist_summary.csv` | Depende da decomposicao adotada no texto |
| I/Fat associa-se negativamente a eficiencia | coeficiente SW negativo e IC95% sem zero | Tabela SW + figura de coeficientes | `outputs/tables/tab_simar_wilson.csv`; `outputs/figures/fig_simar_wilson_coefs.png` | Associacao condicional; nao inferencia causal forte |
| K/L associa-se negativamente e W/L positivamente | sinais e significancia dos coeficientes | Tabela SW + tabela de robustez OLS | `outputs/tables/tab_simar_wilson.csv`; `outputs/tables/tab_tobit_comparison.csv` | Interpretacao economica condicional ao modelo especificado |
| O cluster C2 apresenta penalidade de eficiencia | dummy C2 negativa e significativa | Tabela SW | `outputs/tables/tab_simar_wilson.csv` | Comparacao relativa ao cluster de referencia (C1) |
| A leitura ambiental e interpretativa, fora do DEA base | regra metodologica + cruzamentos por classe | Tabela de anexo + cruzamento por classe | `outputs/tables/tabela_anexo_classificacao_ambiental.md`; `outputs/tables/cruzamento_ambiental_eficiencia_classe.csv` | Nao usar como prova causal ambiental no modelo principal |

### 25.3 Matriz de escrita por capitulo (uso operacional)

| Capitulo | O que afirmar | Evidencia obrigatoria antes de escrever |
|---|---|---|
| 5.1 | Composicao do painel, escala e heterogeneidade | `tab_descritivas.csv`, `tab_media_ano.csv`, `fig_concentracao_pim.png` |
| 5.2 | Escolha de k e perfil de clusters | `tab_kmeans_validation.csv`, `tab_bootstrap_stability.csv`, `tab_perfil_clusters_v2.csv` |
| 5.3 | Niveis de eficiencia e fronteira | `tab_dea_summary.csv`, `dea_scores.csv`, `fig_dea_scores.png` |
| 5.4 | Dinamica da produtividade (M, EC, TC, PEC, SC) | `tab_malmquist_summary.csv`, `fig_malmquist_decomp.png`, `fig_malmquist_ec_tc.png` |
| 5.5 | Gap entre fronteiras (TGR) | `tab_metafrontier_tgr.csv`, `fig_tgr_evolution.png` |
| 5.6 | Determinantes da eficiencia | `tab_simar_wilson.csv`, `tab_tobit_comparison.csv`, `fig_simar_wilson_coefs.png` |
| 6 | Mecanismos, trade-offs e limites | saídas de 5.1-5.6 + `texto_discussao_ambiental_final.md` |
| 7 | Resposta a pergunta e recomendacoes | sintese de 5 e 6, sem numero novo sem fonte |

---

## 26. CHECKLIST DE NAO-OMISSAO (PRONTO PARA REDACAO FINAL)

### 26.1 Regra de aceite por secao

Uma secao so e considerada fechada quando todos os itens abaixo forem marcados como concluido:

1. Cada numero citado aparece em uma tabela/figura/arquivo rastreavel.
2. Cada interpretacao economica vem apos o resultado estatistico, nao antes.
3. Cada implicacao de policy explicita pelo menos uma limitacao de inferencia.
4. Nao existe contradicao interna entre Cap. 5, 6 e 7.

### 26.2 Checklist por capitulo

| Capitulo | Item de controle | Status alvo |
|---|---|---|
| 1 | Objetivos especificos (Secao 1.3) explicitados e alinhados ao pipeline final | Obrigatorio antes da versao final |
| 1-4 | Nenhuma mencao metodologica legada incoerente (ex.: VA como output principal, RAIS como output principal) | Obrigatorio antes da banca |
| 5 | Todas as 7 subsecoes com tabela/figura numerada e interpretacao separada | Obrigatorio |
| 6 | Discussao com confronto de literatura + limites + implicacoes segmentadas | Obrigatorio |
| 6 | Secao ambiental com BCCAS, sem extrapolacao causal | Obrigatorio |
| 7 | Resposta direta da pergunta de pesquisa em 1 paragrafo | Obrigatorio |
| 7 | Contribuicoes, limites e agenda futura em itens separados | Obrigatorio |
| Pos-texto | Referencias e anexos consistentes com citacoes no corpo | Obrigatorio |

### 26.3 Itens proibidos no texto final

1. Declarar causalidade forte a partir de Simar-Wilson/DEA.
2. Generalizar resultados do PIM para outros polos sem ressalva.
3. Usar nomenclatura de versionamento tecnico no corpo principal (`v1`, `v2`, `conservadora`).
4. Introduzir numero nao presente nos arquivos de output.

---

## 27. PROTOCOLO DE GOVERNANCA DE AFIRMACOES (ANTI-LACUNA)

### 27.1 Fluxo antes de escrever qualquer paragrafo analitico

1. Selecionar a afirmacao.
2. Localizar o arquivo de evidencia na Secao 25.
3. Validar que o numero aparece exatamente na tabela/figura correspondente.
4. Redigir em tres blocos: resultado -> interpretacao -> limite.
5. So entao integrar no capitulo.

### 27.2 Template obrigatorio de paragrafo empirico

Usar a seguinte estrutura minima:

1. **Resultado:** apresentar o numero e a fonte (tabela/figura).
2. **Interpretacao:** explicar o significado economico no contexto do PIM.
3. **Limite:** registrar o que o resultado nao permite concluir.

### 27.3 Regra de consistencia transversal

Antes da versao final, executar varredura textual para garantir:

1. Mesmos valores para os mesmos indicadores em todos os capitulos.
2. Mesma nomenclatura de clusters (C0, C1, C2) e da base ambiental (BCCAS).
3. Mesma formulacao da pergunta de pesquisa e da resposta final.

---

*Documento atualizado em: 14/03/2026 (Modelo Final — rastreabilidade integral da escrita e protocolo anti-lacuna)*
*Pipeline: 01→02→03→04→06→07→08→09→10→11. Painel: 137 obs, 23 sub. Outputs: 17 figuras, 14 tabelas analiticas + 8 artefatos ambientais consolidados (base principal + anexo + cruzamentos + textos finais + trilha de auditoria).*
*Especificação final: RAIS removida. SUFRAMA emprego. Salários Tab 24. K-means 3 vars-razão. SW 3 regressores + cluster + trend. DEA VRS+CRS. Malmquist CRS + decomposição EC/TC/PEC/SC. Couros 2018 = zero estrutural.*
