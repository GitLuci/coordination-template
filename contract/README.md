# Contract before code

The contract is the single source of truth between FE and BE: what the FE sends, what the BE receives and returns, what the FE receives, and the errors. It is signed **before** any implementation and versioned.

## Files

| File | Content |
|---|---|
| `openapi.yaml` | The schema (OpenAPI 3.x; another format works if the project already uses one, e.g. GraphQL SDL, protobuf) |
| `examples/<endpoint>/<case>.json` | Concrete cases: `{"request": {...}, "response": {"status": 201, "body": {...}}}` |
| `VERSIONS.json` | Signed versions: number → sha256 of `openapi.yaml` + `examples/` |
| `CHANGES.md` | One line per version: what changed and why |

## Flow

1. **Slice:** the coordinator defines the slice (e.g. "list and create orders").
2. **Proposal (BE):** endpoints, schemas, errors and examples, including at least one success case and one error case per endpoint.
3. **Review (FE):** can the screen show everything from this alone? Do the names and formats work?
4. **Signature (coordinator):** `python scripts/contract.py register --version N` and a line in `CHANGES.md`. Notice to both devs.
5. **Parallel implementation:**
   - BE: each example is a server test; the real response validates against the schema.
   - FE: each example is a mock/fixture; the interface tests use them as they are.
6. **Integration:** e2e with the real BE; if something diverges, the contract says who has to change.

## Types and client generated from the contract

The API types and client (in the FE and, if it makes sense, the BE) are **generated** from the signed contract with the generator the project chooses, never written by hand nor edited after being generated.

- The BE makes sure the contract generates without errors in the project's generator before proposing it (stable schema and operation names, so the generated names don't change between versions).
- With each new signed version, whoever consumes it regenerates.
- The quality gate checks that the generated code is up to date: regenerating from the signed contract must not produce differences.

The generation command lives in each repository's `AGENTS.md`.

## Changing the contract

Request to the coordinator → decision → new signed version → notice to both → both update tests and mocks. `scripts/contract.py verify` fails if the contract changed without a new version, and (with `--against`) if a repository's copy isn't equal to the version signed in the shared folder.

## Good practices

- Version in the path or header only when there are external clients; inside the project the signed number is enough.
- A uniform error body (e.g. `{"error": {"code": "...", "message": "..."}}`).
- Dates in ISO 8601 with time zone; money as integers in the smallest unit, or decimal as text; never float.
- Pagination, sorting and filters defined in the contract, not discovered during integration.
