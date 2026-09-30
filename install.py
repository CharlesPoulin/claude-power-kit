#!/usr/bin/env python3
"""Offline, additive project installer. Python 3.10+, no third-party packages."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
START = b'<!-- claude-power-kit:start -->'
END = b'<!-- claude-power-kit:end -->'


def payload(root):
    files = {}
    for folder in ('.claude/skills', '.claude/agents', 'templates'):
        for path in sorted((root / folder).rglob('*')):
            if path.is_symlink():
                raise ValueError(f'Bundle contains a symlink: {path}')
            if path.is_file():
                files[path.relative_to(root).as_posix()] = path.read_bytes()
    return files


def hashes(files):
    return {name: hashlib.sha256(data).hexdigest() for name, data in files.items()}


def verify_bundle(root):
    files = payload(root)
    expected = json.loads((root / 'checksums.json').read_text(encoding='utf-8'))
    if not files or hashes(files) != expected:
        raise ValueError('Bundle checksum mismatch. Restore the kit from its trusted Git commit.')
    return files


def check_path(project, path):
    """Reject symlinks and non-directory ancestors before any writes."""
    current = project
    parts = path.relative_to(project).parts
    for index, part in enumerate(parts):
        current = current / part
        if current.is_symlink():
            raise ValueError(f'Refusing symlink: {current}')
        if index < len(parts) - 1 and current.exists() and not current.is_dir():
            raise ValueError(f'Expected directory: {current}')


def plan_install(project, root, power_settings):
    files = verify_bundle(root)
    if not project.is_dir():
        raise ValueError('The target must be an existing project directory.')
    if project == root.resolve():
        raise ValueError('Choose your application project, not the kit repository itself.')
    writes = {}

    def add(path, data):
        check_path(project, path)
        if path.exists():
            if not path.is_file() or path.read_bytes() != data:
                raise ValueError(f'Existing file differs; reconcile it manually: {path}')
        else:
            writes[path] = data

    # Whole skill directories are owned units: never mix versions or extras.
    for source in sorted((root / '.claude/skills').iterdir()):
        if not source.is_dir():
            continue
        target = project / '.claude/skills' / source.name
        check_path(project, target)
        if target.exists():
            if not target.is_dir():
                raise ValueError(f'Expected skill directory: {target}')
            expected = {p.relative_to(source).as_posix(): p.read_bytes()
                        for p in source.rglob('*') if p.is_file()}
            actual = {}
            for p in target.rglob('*'):
                check_path(project, p)
                if p.is_file():
                    actual[p.relative_to(target).as_posix()] = p.read_bytes()
            if actual != expected:
                raise ValueError(f'Existing skill differs; reconcile it manually: {target}')
    for name, data in files.items():
        if name.startswith('.claude/'):
            add(project / name, data)

    def replace_with_backup(path, before, after):
        if before == after:
            return
        if path.exists():
            add(path.with_name(path.name + '.before-power-kit'), before)
        writes[path] = after

    instructions = project / 'CLAUDE.md'
    check_path(project, instructions)
    before = instructions.read_bytes() if instructions.exists() else b''
    block = files['templates/CLAUDE.md'].strip()
    if START in before or END in before:
        if before.count(START) != 1 or before.count(END) != 1:
            raise ValueError('CLAUDE.md has ambiguous kit markers; reconcile manually.')
        start, end = before.index(START), before.index(END) + len(END)
        if before[start:end] != block:
            raise ValueError('Existing kit instructions differ; reconcile CLAUDE.md manually.')
    else:
        separator = b'\n\n' if before and not before.endswith(b'\n\n') else b''
        replace_with_backup(instructions, before, before + separator + block + b'\n')

    if power_settings:
        settings = project / '.claude/settings.json'
        check_path(project, settings)
        before = settings.read_bytes() if settings.exists() else b''
        config = json.loads(before) if before else {}
        if not isinstance(config, dict):
            raise ValueError('Claude settings must be a JSON object.')
        original = json.dumps(config, sort_keys=True)
        defaults = json.loads(files['templates/power-settings.json'])
        config.setdefault('model', defaults['model'])
        permissions = config.setdefault('permissions', {})
        if not isinstance(permissions, dict):
            raise ValueError('Claude permissions must be a JSON object.')
        permissions.setdefault('defaultMode', defaults['permissions']['defaultMode'])
        if json.dumps(config, sort_keys=True) != original:
            after = (json.dumps(config, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
            replace_with_backup(settings, before, after)
    return writes


def install(project, *, root=ROOT, power_settings=False):
    project = Path(project).resolve()
    writes = plan_install(project, Path(root), power_settings)
    for path, data in writes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
    return len(writes)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path, help='Existing application project directory')
    parser.add_argument('--power-settings', action='store_true',
                        help='Add opusplan and acceptEdits defaults only where unset')
    args = parser.parse_args()
    try:
        count = install(args.project, power_settings=args.power_settings)
    except (OSError, ValueError) as error:
        print(f'Not installed: {error}', file=sys.stderr)
        return 1
    print(f'Ready: 9 skills + 1 reviewer in {args.project.resolve()} ({count} files written).')
    print('Power defaults added where unset; existing settings preserved.' if args.power_settings
          else 'Claude settings unchanged. Use --power-settings to add optional defaults.')
    print('Restart Claude Code in that project. Try: /power-build <your task>')
    return 0


if __name__ == '__main__':
    sys.exit(main())
