#!/usr/bin/env python3
"""Validate bundle structure and integrity without dependencies."""
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from install import hashes, payload, verify_bundle  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--update', action='store_true', help='Refresh reviewed payload hashes')
    args = parser.parse_args()
    skills = list((ROOT / '.claude/skills').glob('*/SKILL.md'))
    assert len(skills) == 9, f'Expected 9 skills, found {len(skills)}'
    for path in skills + list((ROOT / '.claude/agents').glob('*.md')):
        text = path.read_text(encoding='utf-8')
        assert text.startswith('---\n'), f'Missing frontmatter: {path}'
        header = text.split('---', 2)[1]
        for key in ('name', 'description'):
            assert re.search(rf'^{key}:\s*\S', header, re.M), f'Missing {key}: {path}'
        for link in re.findall(r'\]\(([^)]+\.md)\)', text):
            if '://' not in link:
                assert (path.parent / link).is_file(), f'Broken reference {link}: {path}'
    sources = json.loads((ROOT / 'sources.json').read_text(encoding='utf-8'))
    for source in sources:
        assert re.fullmatch(r'[0-9a-f]{40}', source['commit']), 'Unpinned upstream source'
        assert (ROOT / '.claude/skills' / source['name'] / 'LICENSE').is_file()
    for path in (ROOT / 'templates').glob('*.json'):
        json.loads(path.read_text(encoding='utf-8'))
    if args.update:
        (ROOT / 'checksums.json').write_text(
            json.dumps(hashes(payload(ROOT)), indent=2) + '\n', encoding='utf-8')
    verify_bundle(ROOT)
    print(f'OK: {len(skills)} skills, reviewer, templates, licenses, and payload checksums.')


if __name__ == '__main__':
    main()
