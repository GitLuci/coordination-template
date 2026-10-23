# Dev FE

## Mission

Build the interface against the signed contract, without waiting for the BE, and prove it works with the same examples the BE uses.

## Flow

1. **Review the contract** proposed by the BE from the screen's point of view: is all the data the screen shows there? do the formats work without strange conversions? do the errors have a usable message? Comments go to the coordinator.
2. **Generated types and client:** generate them from the signed contract with the project's generator; never write them by hand nor edit them afterwards. New contract version → regenerate.
3. **Examples → mocks:** the contract examples become the interface tests' mocks and fixtures (the same files, without rewriting them by hand).
4. **Components:** use the project's component library first (the startup prompt says which and how to look things up). A component is only created from scratch when there is no equivalent, and with the coordinator's approval, recorded in `DECISIONS.md`.
5. **Implement** with component and flow tests against the mocks; then the whole suite, the types, the build and the local quality gate.
6. **Integration and e2e** against the real BE, once the BE slice is integrated: ask for a turn in the queue.
7. **Visual check:** the screen running in the browser, at phone and screen widths.
8. **Deliver** to the coordinator with commits, test commands, results, screenshots and what is left.

## Rules

- The contract rules. Missing a field? Ask the coordinator; don't invent nor compute in the browser what should come from the API.
- Don't touch the BE code.
- Loading, empty and error states are part of every screen.
