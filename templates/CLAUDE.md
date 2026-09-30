<!-- claude-power-kit:start -->
## Working defaults

Inspect first, make the smallest useful change, verify it, and summarize the evidence. Follow the project's existing conventions. Act on safe, reversible work; ask when blocked, destructive, or security-sensitive. Keep replies concise.

Use `rtk` for broad/noisy commands when installed; use narrow raw commands when exact output matters. Read only relevant files, docs, and skills. Keep one active implementation thread per working tree.

<important if="you are refactoring or considering new abstractions">
Read `.claude/skills/principle-laziness-protocol/SKILL.md`. Prefer deletion and direct code. Preserve behavior and avoid unrelated cleanup.
</important>

<important if="you are writing, changing, or reviewing tests">
Use `test-audit` in authoring mode. Each test needs a credible failure and a distinct behavioral contract. A green or slow test is not automatically useless. Keep security and regression protections.
</important>

<important if="you are fixing a bug with a practical regression check or the user requests TDD">
Read `.claude/skills/tdd/SKILL.md`. Prove failure before the fix and success afterward. If that is impractical, use the closest useful check and state the limitation.
</important>

<important if="you are building or polishing interfaces or motion">
Use `emil-design-eng` with the actual task. Follow the existing visual language. Check keyboard access, reduced motion, and touch behavior. Verify APIs against installed library versions.
</important>

<important if="the user asks to improve project instructions">
Use `improve-claude-md`. Preserve verified commands and project-specific constraints.
</important>

For substantial feature work use `power-build`; for a requested review use `power-review`; for a requested checkpoint use `power-handoff`. Ordinary small edits can proceed directly. Delegate only when requested or required by an invoked workflow; give each delegate a bounded job.

<important if="you are polishing documentation, a PR description, or reusable prose">
Read `.claude/skills/unslop/SKILL.md`.
</important>

Finish with what changed, the checks actually run, and remaining limits. Commit, push, open PRs, or deploy only within the user's authorization. Use existing permission controls.
<!-- claude-power-kit:end -->
