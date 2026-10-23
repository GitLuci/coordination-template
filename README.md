# Coordination template

A way of working with **one coordinator and two or more developers** (for example, one frontend and one backend), each in their own terminal or agent session. It doesn't depend on any project, language or AI vendor.

The idea in three sentences:

1. **Contract before code.** FE and BE only start implementing after they sign the API contract (what the FE sends, what the BE receives and returns, what the FE receives, the errors and examples). Both sides test against the same examples, so integration holds no surprises.
2. **The coordinator decides, the devs implement.** The coordinator answers questions in the owner's place, manages the test queue and integrates. Only what is really the owner's goes up to them: architecture, product scope, costs and irreversible or outward-facing actions.
3. **Everything that matters is written down.** Board, questions, decisions and contract live in files everyone reads; nobody depends on the memory of a conversation.

## Where to start

| File | What it is for |
|---|---|
| [`TEMPLATE.md`](TEMPLATE.md) | The complete method: roles, communication, task cycle, tests, escalation |
| [`AGENTS.md`](AGENTS.md) | Entry point for any agent that opens the project (copy it into each repo) |
| [`roles/`](roles/) | What each role does and doesn't do: coordinator, dev BE, dev FE |
| [`contract/`](contract/) | The contract-first process, the contract template and version checking |
| [`coordination/`](coordination/) | Templates for the board, questions, decisions, test queue and message inboxes |
| [`gates/QUALITY-GATE.md`](gates/QUALITY-GATE.md) | What must pass before a task is integrated |
| [`prompts/`](prompts/) | Startup prompts to paste into each role's terminal |

## How to apply it to a project

**A single repository (monorepo):** copy `AGENTS.md`, `coordination/`, `contract/` and `gates/` into the project root.

**Separate repositories (FE and BE):** coordination lives somewhere all three read and write:

- a shared local folder (e.g. `../coordination-<project>/`) or a dedicated coordination repository, with `coordination/` and `contract/`;
- each repository (FE and BE) has its own `AGENTS.md` pointing at that folder and a copy of the signed contract in `contract/`, checked with `scripts/contract.py verify --against <shared folder>`.

Then fill in the prompts in [`prompts/`](prompts/) with the project's details and paste them into each terminal.

## Communication between agents

- **Claude Code sessions on the same machine** can use direct messages between sessions for urgent notices. Even so, whatever is decided is written in the files.
- **Terminals, sessions or agents from other vendors** (or any mix) communicate **only through files**, in git or a shared local folder: the board, the inboxes, the questions and the decisions.
