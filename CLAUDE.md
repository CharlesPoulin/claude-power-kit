# Claude Power Kit

A portable, project-local Claude Code setup. Python standard library only.

- `install.py`: offline installer; preserve existing project files and settings.
- `.claude/skills/`: original upstream skills plus documented adaptations and local workflows.
- `.claude/agents/`: an independent reviewer with read tools only.
- `templates/`: instructions and optional settings installed in target projects.
- `sources.json` and `licenses/`: upstream provenance. Preserve copyright notices.

Run `python3 -m unittest discover -s tests -v` after installer changes. Run `python3 scripts/check.py` to validate skill structure and checksums. If intentionally editing bundled payload, run `python3 scripts/check.py --update` first and review the resulting checksum diff.

Keep upstream edits explicit in `UPSTREAM.md`. Do not apply OpenClaw-specific tooling to this repository. Never place credentials, machine paths, personal configuration, or session transcripts in published files.
