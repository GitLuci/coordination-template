# Quality gate

Uma tarefa só vai a revisão com o gate **local** verde; só é integrada com o gate **de integração** verde. Os comandos
concretos de cada projecto ficam no `AGENTS.md` do repositório.

## Local (o dev, antes de entregar)

| Verificação | BE | FE |
|---|---|---|
| Testes unitários, suite inteira | ✔ | ✔ |
| Exemplos do contrato (versão firmada) | como testes do servidor | como mocks/fixtures dos testes |
| Validação das respostas contra o schema | ✔ | — |
| Lint e formatação | ✔ | ✔ |
| Tipos (type-check) | ✔ se a linguagem tiver | ✔ |
| Build | ✔ | ✔ sem avisos novos |
| Cobertura das linhas novas | ≥ meta do projecto | ≥ meta do projecto |
| `python scripts/contrato.py verificar` | ✔ | ✔ |
| Contrato gera sem erros no gerador de tipos do projecto | ✔ antes de propor | — |
| Código gerado em dia (regenerar do contrato firmado não deixa diferenças) | ✔ se gerar | ✔ |

## De integração (pela fila de testes)

| Verificação | Quem corre | Passa se |
|---|---|---|
| Integração BE (base de dados e serviços reais ou contentores) | dev-be | todos verdes |
| Integração FE ↔ BE real | dev-fe | todos verdes |
| E2E dos fluxos da fatia (browser) | dev-fe ou coordenador | todos verdes, em largura de telemóvel e de ecrã |
| Análise estática / qualidade (ex.: SonarQube) | coordenador | sem problemas novos de severidade alta; quality gate da ferramenta verde |
| Segurança das dependências | coordenador | sem vulnerabilidades novas altas/críticas |

## Depois do merge (coordenador)

Suite completa no ramo principal. Se falhar, reverte-se o merge antes de mais nada e a tarefa volta ao dev com o
output.

## Regra

Resultados reais, com o comando e o output. Um passo não feito diz-se que não foi feito.
