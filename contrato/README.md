# Contrato antes de código

O contrato é a única fonte de verdade entre FE e BE: o que o FE envia, o que o BE recebe e devolve, o que o FE
recebe, e os erros. É firmado **antes** de qualquer implementação e versionado.

## Ficheiros

| Ficheiro | Conteúdo |
|---|---|
| `openapi.yaml` | O schema (OpenAPI 3.x; outro formato serve se o projecto já usar, ex.: GraphQL SDL, protobuf) |
| `exemplos/<endpoint>/<caso>.json` | Casos concretos: `{"pedido": {...}, "resposta": {"estado": 201, "corpo": {...}}}` |
| `VERSOES.json` | Versões firmadas: número → sha256 de `openapi.yaml` + `exemplos/` |
| `ALTERACOES.md` | Uma linha por versão: o que mudou e porquê |

## Fluxo

1. **Fatia:** o coordenador define a fatia (ex.: «listar e criar pedidos»).
2. **Proposta (BE):** endpoints, schemas, erros e exemplos, incluindo pelo menos um caso de sucesso e um de erro por
   endpoint.
3. **Revisão (FE):** o ecrã consegue mostrar tudo só com isto? Os nomes e formatos servem?
4. **Firma (coordenador):** `python scripts/contrato.py registar --versao N` e uma linha em `ALTERACOES.md`. Aviso aos
   dois devs.
5. **Implementação em paralelo:**
   - BE: cada exemplo é um teste do servidor; a resposta real valida contra o schema.
   - FE: cada exemplo é um mock/fixture; os testes da interface usam-nos tal como estão.
6. **Integração:** e2e com o BE real; se algo diverge, o contrato diz quem tem de mudar.

## Mudar o contrato

Pedido ao coordenador → decisão → nova versão firmada → aviso aos dois → os dois actualizam testes e mocks. O
`scripts/contrato.py verificar` falha se o contrato mudou sem nova versão, e (com `--contra`) se a cópia de um
repositório não for igual à versão firmada na pasta partilhada.

## Boas práticas

- Versão no caminho ou no cabeçalho só quando há clientes externos; dentro do projecto chega o número firmado.
- Um corpo de erro uniforme (ex.: `{"erro": {"codigo": "...", "mensagem": "..."}}`).
- Datas em ISO 8601 com fuso; dinheiro em inteiros na menor unidade, ou decimal em texto; nunca float.
- Paginação, ordenação e filtros definidos no contrato, não descobertos na integração.
