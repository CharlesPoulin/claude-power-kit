# A small power-user routine

## Pick the right amount of planning

Small fix: give the task directly. Bigger feature: enter Claude's Plan Mode
with Shift+Tab and describe the outcome and how you will recognize success.
Review the plan, then switch to execution. `opusplan` uses Opus only in actual
Plan Mode; a prose plan from `/power-build` does not switch models by itself.
You can start explicitly with:

```bash
claude --model opusplan --permission-mode plan
```

If Opus is unavailable, use a supported model such as `claude --model sonnet`.
The kit uses aliases instead of pinning model release names. See
[model configuration](https://code.claude.com/docs/en/model-config) and
[interactive mode](https://code.claude.com/docs/en/interactive-mode).

## Build, inspect, then ship

```text
/power-build Implement [outcome]. Reuse [existing module]. Verify [observable behavior].
/power-review Review working changes against that requirement.
```

Read the diff and check results. Ask Claude to fix any validated findings, then
commit or open a PR when ready. Publishing remains a separate user-authorized
action unless you included it in the original request.

UI work: give `/emil-design-eng` an actual task and ask for a browser check of
the changed interaction. Test cleanup: start with `/test-audit` in report-only
mode, then request cleanup of the evidence-backed candidates.

## Keep sessions focused

Use `/context` to inspect context usage. Before switching tasks, run
`/power-handoff`. Start a fresh session and ask:

```text
Read HANDOFF.md and the relevant project instructions. Verify the current
working state, then continue with the next action.
```

Use `claude --continue` to continue the latest conversation in that directory,
or `claude --resume` to choose an earlier one. Keep handoffs short and exclude
secrets. See [interactive commands](https://code.claude.com/docs/en/interactive-mode).

## Parallel work only when it helps

One implementation session per working tree. For a separate task, create a
separate branch and worktree from a Git repository with an initial commit:

```bash
git worktree add ../my-project-feature -b feature/my-task
```

Tracked kit files follow the checkout. If the kit is untracked in the original
project, run its installer for the new worktree too. Start Claude there and
give it a bounded task. Merge through your normal project workflow. Do not
run two editing sessions against the same files.

The kit does not start background agents. `/power-review` requests one scoped
read-only reviewer. Explicitly request parallel discovery if a large test audit
would benefit from it. See [Claude subagents](https://code.claude.com/docs/en/sub-agents)
and [Git worktrees](https://git-scm.com/docs/git-worktree).

## Maintain useful instructions

If the project lacks its own guidance, ask Claude to inspect the repository
and add verified build/test commands to the existing `CLAUDE.md`. Then use
`/improve-claude-md` to trim it. Keep the kit's marked block intact if you want
idempotent reinstall; put project-specific rules outside it.

Use tests to protect credible regressions, not to inflate counts. Keep the
smallest meaningful check plus your repository's required gates. `rtk` is
optional; the kit uses ordinary tools when it is absent.
