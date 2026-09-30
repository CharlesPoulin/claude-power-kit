# Sources and adaptations

Upstream files are vendored so installation is offline and reproducible.
`sources.json` records exact repositories, paths, revisions, and modifications.
`checksums.json` records the installed payload. This kit is independently
curated; inclusion does not imply endorsement by any creator.

| Source | Pinned revision | Bundled material | License copy |
| --- | --- | --- | --- |
| [Poteto's pstack in cursor/plugins](https://github.com/cursor/plugins/tree/2eb7ed4613cfc8f098dfe464a23680ea44d84c5e/pstack) | `2eb7ed4613cfc8f098dfe464a23680ea44d84c5e` | principle-laziness-protocol, tdd, unslop | [pstack license](licenses/cursor-plugins.txt) |
| [Dex Horthy / HumanLayer skills](https://github.com/humanlayer/skills/tree/ca7c8088db69e315a8b2deea43820270457f8f3c) | `ca7c8088db69e315a8b2deea43820270457f8f3c` | improve-claude-md | [HumanLayer license](licenses/humanlayer-skills.txt) |
| [Emil Kowalski's skills](https://github.com/emilkowalski/skills/tree/d16ebe60d09a5ba2afcb7054ede9d0a10c9f6128) | `d16ebe60d09a5ba2afcb7054ede9d0a10c9f6128` | emil-design-eng | [Emil license](licenses/emilkowalski-skills.txt) |
| [OpenClaw test-audit](https://github.com/openclaw/openclaw/tree/ca17064696396cb0dcec6fe034b04fdce347c720/.agents/skills/test-audit) | `ca17064696396cb0dcec6fe034b04fdce347c720` | test-audit and CAMPAIGN.md, adapted | [OpenClaw license](licenses/openclaw-openclaw.txt) |

Each installed upstream skill also carries its license in its own directory.
The first five upstream skills are unchanged; their licenses were added
alongside them. No claims of upstream authorship apply to the kit's installer,
settings template, reviewer, or `power-*` workflows.

## OpenClaw changes

The test-audit value bar, junk-pattern checklist, retention criteria, and
candidate evidence requirements are retained. Adaptations:

- Replace OpenClaw-specific paths, Vitest wrappers, changed-file gates, and
  mandatory `openclaw-testing`, `crabbox`, `autoreview`, and PR-maintainer
  dependencies with the target project's actual commands and policies.
- Make audit-only requests explicitly read-only; cleanup requests may proceed
  after recording evidence. Sequential work is the default; delegation requires
  a user request.
- Make review and publishing follow the user's scope. State self-review limits
  when an independent reviewer is not requested or unavailable.
- Rewrite campaign examples and sequencing for arbitrary projects. Preserve
  baseline failures as potential bugs and meaningful test contracts during
  consolidation. Inspect merge conflicts instead of automatically retaining
  deletions.
- Clarify that coverage metrics or surviving mutations alone do not justify
  removing tests; restore temporary mutation edits without disturbing other work.

## Updating vendored sources

Review the upstream revision and license before replacing files. Record the
new full commit and any adaptations in `sources.json` and this document, then:

```bash
python3 scripts/check.py --update
python3 -m unittest discover -s tests -v
```

Review the source and checksum diffs together. Checksums detect accidental
payload changes; they are not a signature or a substitute for reviewing trust.
