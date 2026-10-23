# Quality gate

A task only goes to review with the **local** gate green; it is only integrated with the **integration** gate green. Each project's concrete commands live in the repository's `AGENTS.md`.

## Local (the dev, before delivering)

| Check | BE | FE |
|---|---|---|
| Unit tests, whole suite | ✔ | ✔ |
| Contract examples (signed version) | as server tests | as test mocks/fixtures |
| Validation of responses against the schema | ✔ | — |
| Lint and formatting | ✔ | ✔ |
| Types (type-check) | ✔ if the language has them | ✔ |
| Build | ✔ | ✔ with no new warnings |
| Coverage of new lines | ≥ project target | ≥ project target |
| `python scripts/contract.py verify` | ✔ | ✔ |
| Contract generates without errors in the project's type generator | ✔ before proposing | — |
| Generated code up to date (regenerating from the signed contract leaves no differences) | ✔ if it generates | ✔ |

## Integration (through the test queue)

| Check | Who runs | Passes if |
|---|---|---|
| BE integration (real database and services or containers) | dev-be | all green |
| FE ↔ real BE integration | dev-fe | all green |
| E2E of the slice's flows (browser) | dev-fe or coordinator | all green, at phone and screen widths |
| Static analysis / quality (e.g. SonarQube) | coordinator | no new high-severity issues; the tool's quality gate green |
| Dependency security | coordinator | no new high/critical vulnerabilities |

## After the merge (coordinator)

Full suite on the main branch. If it fails, the merge is reverted before anything else and the task goes back to the dev with the output.

## Rule

Real results, with the command and the output. A step not done is said not to have been done.
