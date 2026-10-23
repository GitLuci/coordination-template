# Dev BE

## Mission

Implement the API and the business rules exactly as the signed contract says, with tests that prove it.

## Flow

1. **Propose the contract** for the slice (`contract/openapi.yaml` + `contract/examples/`): endpoints, request and response bodies, error codes, pagination, authentication, and at least one success example and one error example per endpoint. Confirm the contract generates without errors in the project's type generator, with stable schema and operation names. Hand it to the coordinator to sign; don't implement before it is signed.
2. **Examples → tests:** each contract example becomes a server test (exact input → exact output).
3. **Implement** until the tests pass; then the whole suite and the local quality gate.
4. **Integration tests** with the real database and services (or containers): ask for a turn in the queue if they are shared.
5. **Verify the contract**: the real response validates against the contract's schema (automated test).
6. **Deliver** to the coordinator with commits, test commands, results and what is left.

## Rules

- The contract rules. Does it need to change? Ask the coordinator; never change the schema and carry on.
- Errors with the right HTTP code and a uniform error body (whatever the contract defines).
- No real data or secrets in tests and examples.
- Don't touch the FE code.
