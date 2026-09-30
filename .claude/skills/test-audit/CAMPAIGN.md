# Test-pruning campaign

Adapted from OpenClaw for any project. Use only when the user asks for a whole
subsystem audit. The retention bar and evidence rules in [SKILL.md](SKILL.md)
apply throughout. Optimize for confidence, not deletion count.

## 1. Baseline

Pin the current commit, record local modifications, inventory the subsystem's
test files, and run its existing checks. Record failures separately; they may
be product defects. Do not delete tests to make the baseline green.

## 2. Inventory by production owner

Group tests by behavior, including shared boundaries and integration harnesses.
Every in-scope file belongs to one group. Work sequentially unless the user
requests parallel agents; delegated discovery stays read-only and overlapping
edits have one owner.

## 3. Read-only ledger

Read complete tests, production owners, callers, relevant history, and CI
routing. Mark each declaration (or individual table row when needed):

- `R`: retain; name the contract and credible regression.
- `F`: fix the assertion while retaining the contract.
- `C`: consolidate; name the stronger owner that absorbs the assertion first.
- `D`: delete; name the proof that remains or explain why no contract exists.

Judge assertions, not test names. Every mark needs evidence. If the user asked
only for an audit, report this ledger without editing.

## 4. Choose keepers

Review the ledger a second time for redundant layers. Name each contract's
keeper suite, assertions to carry over, retired files, and test-only production
seams removal would unlock. Prefer real observable boundaries over mocks that
implement the asserted behavior.

## 5. Apply one coherent batch

Move distinct assertions before deleting redundant suites. Remove proven-dead
test-only seams; check production and external callers first. Update actual
CI routing and test inventories. Run each group's keepers before continuing.
Record durable project-specific lessons in the project's instruction file.

## 6. Preservation review

Compare every deleted contract with the keepers. Seek independent review when
requested; otherwise state that this was a self-review. Restore lost proof or
document source evidence for rejecting the finding. For restored or doubtful
contracts, use a small deliberate mutation to check that the keeper fails for
the intended reason, then restore exactly your temporary change. Preserve
pre-existing edits. A surviving mutation alone does not prove a test is useless.

## 7. Product defects

Treat baseline failures as potential bugs. Reproduce and report them; fix only
within the authorized scope. For each repair, demonstrate failing-before and
passing-after behavior on the same harness. Record unrelated work as follow-ups.

## 8. Reconcile and hand off

Follow the project's branch and merge policy. If newer changes touch a retired
test, inspect its new contract and preserve it in the appropriate keeper before
resolving the conflict. Never choose deletion automatically. Rerun affected
checks after reconciliation.

Report baseline/final test and support counts separately from production code,
keepers and retired layers, retained false positives, preservation gaps and
mutation evidence, exact checks and results, product defects, and remaining
risks. Commit, publish, and merge only within the user's authorization.
