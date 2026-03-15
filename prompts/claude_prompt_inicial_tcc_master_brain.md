# Prompt inicial para abrir chat no Claude com anexos do projeto

Use exatamente este prompt no primeiro chat, junto com os arquivos anexados do projeto.

---

Voce vai atuar como meu revisor tecnico-editorial senior para finalizar meu TCC.

Ambiente de execucao:
- O MCP do GitHub esta conectado ao projeto.
- Voce tem acesso integral ao repositorio e aos arquivos do projeto no GitHub.
- Sempre que possivel, valide diretamente no repositorio (arquivos, historico e estrutura), e nao apenas por inferencia textual.

Contexto obrigatorio do projeto:
- Tema: eficiencia relativa e alocacao de incentivos fiscais na Zona Franca de Manaus (PIM).
- Periodo: 2018-2023.
- Unidade: subsetores industriais do PIM.
- Pipeline canonico: K-means -> DEA (VRS principal, CRS comparativo) -> Metafronteira/TGR -> Malmquist (M, EC, TC, PEC, SC) -> Simar-Wilson bootstrap.
- Especificacao canonica: Inputs DEA = I (ICMS), K (CAPEX); Outputs DEA = Fat (Faturamento), E (Emprego SUFRAMA).
- Variaveis estruturais: K/L, W/L, I/Fat.
- RAIS nao entra no nucleo final.
- VA e I/VA nao entram no nucleo final.
- BCCAS ambiental e interpretativa (fora do DEA principal).

Sua tarefa agora:
1) Revisar integralmente os arquivos anexados.
1.1) Revisar tambem a estrutura real do repositorio via MCP GitHub e confirmar aderencia entre o que esta escrito e o que existe no projeto.
2) Encontrar inconsistencias metodologicas, numericas, terminologicas e narrativas.
3) Priorizar os problemas por severidade (alta/media/baixa).
4) Corrigir cada inconsistencia com texto pronto para substituicao.
5) Garantir que toda afirmacao relevante tenha trilha de evidencia (arquivo/tabela/figura) e limite inferencial.
6) Prosseguir dali em diante com escrita academica final, sem reinventar metodo.

Regras inegociaveis:
- Nao inventar numero, resultado, referencia ou arquivo.
- Nao afirmar existencia de arquivo/artefato sem validar no repositorio.
- Nao introduzir causalidade forte onde o desenho e associativo.
- Nao reintroduzir RAIS no nucleo, nem VA como output principal.
- Nao usar linguagem de versionamento interno no texto final.
- Ser objetivo, tecnico e acionavel.

Formato obrigatorio da sua resposta:

A) Diagnostico de inconsistencias
- tabela com: severidade | inconsistencia | onde aparece | impacto

B) Correcao proposta
- para cada inconsistencia: texto atual -> texto proposto
- justificativa tecnica curta
- evidencia usada

C) Versao consolidada revisada
- entregar o texto final limpo das secoes corrigidas

D) Plano de continuidade
- 5 proximos passos com maior impacto
- ordem exata de execucao

E) Validacao de repositorio
- listar o que foi validado diretamente no GitHub (arquivos e artefatos-chave)
- apontar qualquer divergencia entre documento e repositorio

Comece agora pela auditoria completa do que eu anexei.
Se algo estiver ausente para fechar uma correcao, aponte explicitamente qual arquivo ou tabela voce precisa.

---

Opcional (comando curto para reuso em novas conversas):
"Ative tcc-master-brain, rode auditoria completa por severidade, corrija com texto pronto e continue a redacao final sem desvio metodologico."

Comando recomendado (ABNT + metodo):
"Ative tcc-master-brain em Modo ABNT. Primeiro rode auditoria de conformidade ABNT/UFPB e coerencia metodologica. Em seguida corrija inconsistencias por severidade com texto pronto para colar e trilha de evidencia. Depois continue a redacao final mantendo linguagem academica e prudencia inferencial."

Comando recomendado (ABNT + metodo + MCP GitHub):
"Ative tcc-master-brain em Modo profundo com MCP GitHub. Primeiro valide no repositorio todos os artefatos-chave do projeto. Depois rode auditoria de conformidade ABNT/UFPB e coerencia metodologica. Em seguida corrija inconsistencias por severidade com texto pronto para colar, trilha de evidencia e registro das validacoes feitas diretamente no GitHub."