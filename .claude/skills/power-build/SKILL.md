---
name: power-build
description: Implement a substantial feature or bug fix from inspection through focused verification. Use when asked to build a feature end to end or explicitly run power-build.
argument-hint: "<feature or bug and acceptance criteria>"
---

# Build and verify

Task: $ARGUMENTS

Identify the requested outcome and the existing behavior. Read relevant project instructions and the implementation boundary. Ask only for missing decisions that materially change the result.

For multi-step work, state a short plan with observable acceptance criteria and a verification command. When the user asks for planning only, stop at the plan. Otherwise proceed with authorized implementation; do not turn every step into an approval gate.

Make one coherent change at a time. Reuse existing components and dependencies. Load the bundled TDD, test-audit, or design guidance only when relevant. For bugs, prefer an inexpensive check that fails before the change and passes after it.

Run the smallest meaningful checks plus required project gates. For UI changes, inspect the result in a browser when available and exercise the changed interaction. Static review does not prove visual correctness; say when visual verification is unavailable.

Before finishing, inspect the complete diff for unrelated changes and contracts lost. If the user requests an independent review, use `power-review` and resolve validated findings. Avoid repeated checks without a new change or unresolved concern.

Report changed behavior, verification results, and outstanding limits. Keep commits, pushes, PRs, and deployment within the user's requested scope.
