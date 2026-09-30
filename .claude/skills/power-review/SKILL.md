---
name: power-review
description: Review a defined code diff for actionable bugs, regressions, and lost contracts using an independent read-only reviewer when available. Use for requested code review or explicit power-review.
argument-hint: "[base ref, PR, or working changes]"
---

# Independent review

Scope: $ARGUMENTS

Establish the exact comparison. Use the supplied base/PR. Otherwise review staged and unstaged tracked changes plus relevant untracked implementation files. Do not silently compare against an arbitrary branch. Record the base and head when commits are involved.

Collect the diff, relevant project rules, and the requested behavior. Send these to the `power-reviewer` subagent with file paths it can read. Ask it to look for defects without feeding it a desired conclusion. It has no shell or editing tools; the parent supplies diff output and runs any justified check. If delegation is unavailable, perform the review directly and label it as self-review.

Validate candidate findings against code and available evidence. Report only actionable defects with file/line, trigger, consequence, and fix direction. Treat style preferences separately. For changed tests use test-audit's value and retention bars; a small or slow test is not a defect by itself.

Do not edit code unless the user asked for fixes. If fixes are authorized, apply validated repairs, rerun affected checks, and review the new diff. Finish with findings by severity, unresolved questions, and verification limits. Say explicitly if no actionable findings remain.
