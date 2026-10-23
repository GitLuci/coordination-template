# Board

Statuses: `to do` · `in progress` · `blocked` · `in review` · `integrated`.
The coordinator creates and assigns; each dev updates the status and note of their tasks.

| Id | Slice | Owner | Status | Depends on | Branch | Acceptance criterion | Note (latest) |
|---|---|---|---|---|---|---|---|
| T-001 | 1 | dev-be | to do | — | `contract/slice-1` | Slice 1 contract proposed (schema + 1 success example and 1 error example per endpoint) | |
| T-002 | 1 | dev-fe | to do | T-001 | — | Slice 1 contract reviewed from the screen's point of view | |
| T-003 | 1 | coordinator | to do | T-002 | — | Contract v1 signed (`VERSIONS.json`) and both notified | |
| T-004 | 1 | dev-be | to do | T-003 | `be/slice-1` | v1 examples pass as server tests; quality gate green | |
| T-005 | 1 | dev-fe | to do | T-003 | `fe/slice-1` | Slice 1 screen with v1 example mocks; quality gate green | |
| T-006 | 1 | coordinator | to do | T-004, T-005 | — | Slice 1 e2e against the real BE; integrated into main | |
