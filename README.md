# Claude Power Kit

A small, ready-to-use Claude Code setup: selected skills from **Poteto**, **Dex
Horthy / HumanLayer**, and **Emil Kowalski**, plus **OpenClaw's test-audit** and
three practical workflows. Nine skills, one reviewer, one offline installer.

## Start here

You need [Claude Code](https://code.claude.com/docs/en/setup), Git, and Python
3.10 or later. Choose an existing project you want Claude to work on.

**Windows / PowerShell:**

```powershell
git clone https://github.com/CharlesPoulin/claude-power-kit.git
cd claude-power-kit
py install.py "C:\path\to\your-project" --power-settings
cd "C:\path\to\your-project"
claude
```

**macOS / Linux / WSL:**

```bash
git clone https://github.com/CharlesPoulin/claude-power-kit.git
cd claude-power-kit
python3 install.py /path/to/your-project --power-settings
cd /path/to/your-project
claude
```

Replace the example project path. If Claude is already open, restart it there.
Then give it a real task:

```text
/power-build Add a settings page using the existing components. Verify saving and reloading preferences.
```

`--power-settings` adds **opusplan** (Opus in Plan Mode, Sonnet for execution)
and **acceptEdits** (automatic file-edit approval within Claude's permission
rules). Existing values in the project's settings win. Omit the flag to leave
settings untouched. Model availability depends on your account/provider;
see [model configuration](https://code.claude.com/docs/en/model-config) and
[permission modes](https://code.claude.com/docs/en/permissions).

## Included

| Source | Skill | Purpose |
| --- | --- | --- |
| Poteto, through Cursor's pstack | `principle-laziness-protocol` | Smaller changes, fewer unnecessary layers |
| Poteto, through Cursor's pstack | `tdd` | Practical failing-before / passing-after checks |
| Poteto, through Cursor's pstack | `unslop` | Remove filler from prose and documentation |
| Dex Horthy / HumanLayer | `improve-claude-md` | Keep project instructions useful and concise |
| Emil Kowalski | `emil-design-eng` | UI polish, motion, accessibility, interaction details |
| OpenClaw, adapted | `test-audit` | Find redundant tests while preserving meaningful contracts |
| This kit | `power-build` | Inspect, implement, verify, report |
| This kit | `power-review` | Review a defined diff with a separate read-only reviewer |
| This kit | `power-handoff` | Save a short checkpoint for the next session |

The `power-reviewer` agent can read files and search; it cannot edit files or
run shell commands. The main session supplies the diff and runs any needed
checks. If delegation is unavailable, the review is explicitly labeled a
self-review.

This is a curated selection, not the creators' complete stacks or an endorsed
collaboration. Pinned sources and licenses are in [UPSTREAM.md](UPSTREAM.md).

## Everyday commands

```text
/emil-design-eng Polish this settings form's spacing, focus states, and transitions.
/power-review Review my working changes for bugs and lost regression coverage.
/test-audit Audit tests in src/settings. Report candidates only; do not edit.
/test-audit Remove proven redundant tests in src/settings, preserve distinct contracts, and run affected checks.
/improve-claude-md
/power-handoff
```

The test cleanup skill comes from **OpenClaw**. It requires evidence of what
each candidate protects and what proof remains. Slowness, test size, passing
status, or a coverage percentage alone are not reasons to delete a test.

The included project rules load guidance only when relevant. Poteto's three
skills retain their upstream manual-invocation setting; project rules tell
Claude when to read their files. You can also invoke them explicitly, for
example `/principle-laziness-protocol simplify this module` or `/unslop README.md`.

See [POWER-USER.md](POWER-USER.md) for planning, separate worktrees, and clean
handoffs. No MCP server, runtime package, paid third-party service, hook, or
background updater is required by this kit. Claude usage follows your plan.

## What installation changes

- Adds project-local `.claude/skills/` entries and `.claude/agents/power-reviewer.md`.
- Appends a marked block to `CLAUDE.md`, preserving original bytes and making
  `CLAUDE.md.before-power-kit` when an existing file changes.
- With `--power-settings`, adds only missing `model` and
  `permissions.defaultMode` keys in `.claude/settings.json`, with a byte-for-byte
  backup if an existing file changes. Other settings remain intact.

The installer downloads nothing, checks bundled payload hashes, preflights
conflicts, rejects symlinks inside installation paths, and is safe to rerun on
an unchanged installation. A differing skill, agent, edited kit block, or
conflicting backup stops installation before writes; reconcile it manually.
Stop other edits while installing. Unexpected OS/disk errors can interrupt
writes; installation is not a filesystem transaction.

The installer does not edit your project's `.gitignore`. Review the added
files before committing. Backups can contain your original private instructions
or settings; keep them local. User/global and managed Claude settings can also
affect effective behavior; see [settings precedence](https://code.claude.com/docs/en/settings).

Personal skills with the same names can take precedence; resolve duplicates
if a command loads the wrong skill. See [Claude's skills documentation](https://code.claude.com/docs/en/skills).

To update, review this repo's changes, then reconcile changed installed files.
The installer deliberately does not overwrite customizations. To uninstall,
remove only this kit's skill directories, reviewer, and marked instruction
block; restore optional setting keys from your backup as appropriate. Keep
unrelated changes and personal project settings.

## Verify the kit

```bash
python3 scripts/check.py
python3 -m unittest discover -s tests -v
```

On Windows use `py` instead of `python3`. GitHub Actions checks the payload and
installer on Windows and Linux. These checks verify installation behavior and
file structure, not the quality of model-generated changes.

MIT for this kit's original code and workflows. Bundled skills retain their
upstream licenses. See [LICENSE](LICENSE), [licenses/](licenses/), and
[UPSTREAM.md](UPSTREAM.md).
