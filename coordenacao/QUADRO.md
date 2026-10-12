# Quadro

Estados: `por fazer` · `em curso` · `bloqueada` · `em revisão` · `integrada`.
O coordenador cria e atribui; cada dev actualiza o estado e a nota das suas tarefas.

| Id | Fatia | Dono | Estado | Depende de | Ramo | Critério de aceitação | Nota (última) |
|---|---|---|---|---|---|---|---|
| T-001 | 1 | dev-be | por fazer | — | `contrato/fatia-1` | Contrato da fatia 1 proposto (schema + 1 exemplo de sucesso e 1 de erro por endpoint) | |
| T-002 | 1 | dev-fe | por fazer | T-001 | — | Revisão do contrato da fatia 1 do ponto de vista do ecrã | |
| T-003 | 1 | coordenador | por fazer | T-002 | — | Contrato v1 firmado (`VERSOES.json`) e aviso aos dois | |
| T-004 | 1 | dev-be | por fazer | T-003 | `be/fatia-1` | Exemplos v1 passam como testes do servidor; quality gate verde | |
| T-005 | 1 | dev-fe | por fazer | T-003 | `fe/fatia-1` | Ecrã da fatia 1 com mocks dos exemplos v1; quality gate verde | |
| T-006 | 1 | coordenador | por fazer | T-004, T-005 | — | E2E da fatia 1 contra o BE real; integrado no principal | |
