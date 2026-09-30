import json
from pathlib import Path
import shutil
import tempfile
import unittest

from install import ROOT, install


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name) / 'project'
        self.project.mkdir()

    def snapshot(self):
        return {p.relative_to(self.project).as_posix(): p.read_bytes()
                for p in self.project.rglob('*') if p.is_file()}

    def test_fresh_install_is_offline_and_idempotent(self):
        self.assertGreater(install(self.project), 0)
        self.assertEqual(len(list((self.project / '.claude/skills').glob('*/SKILL.md'))), 9)
        self.assertTrue((self.project / '.claude/agents/power-reviewer.md').is_file())
        self.assertFalse((self.project / '.claude/settings.json').exists())
        before = self.snapshot()
        self.assertEqual(install(self.project), 0)
        self.assertEqual(self.snapshot(), before)

    def test_preserves_instruction_bytes_and_backup(self):
        original = b'# Project\r\nKeep our custom commands.\r\n'
        (self.project / 'CLAUDE.md').write_bytes(original)
        install(self.project)
        self.assertTrue((self.project / 'CLAUDE.md').read_bytes().startswith(original))
        self.assertEqual((self.project / 'CLAUDE.md.before-power-kit').read_bytes(), original)
        self.assertEqual(install(self.project), 0)

    def test_conflicting_skill_does_not_partially_install(self):
        skill = self.project / '.claude/skills/tdd/SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text('My own skill', encoding='utf-8')
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'Existing skill differs'):
            install(self.project, power_settings=True)
        self.assertEqual(self.snapshot(), before)

    def test_existing_agent_conflict_is_preflighted(self):
        agent = self.project / '.claude/agents/power-reviewer.md'
        agent.parent.mkdir(parents=True)
        agent.write_text('Custom reviewer', encoding='utf-8')
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'Existing file differs'):
            install(self.project)
        self.assertEqual(self.snapshot(), before)

    def test_power_settings_preserve_existing_preferences(self):
        settings = self.project / '.claude/settings.json'
        settings.parent.mkdir()
        original = b'{"model":"sonnet","permissions":{"deny":["Read(.env)"]},"env":{"DEMO":"yes"}}'
        settings.write_bytes(original)
        install(self.project, power_settings=True)
        config = json.loads(settings.read_bytes())
        self.assertEqual(config['model'], 'sonnet')
        self.assertEqual(config['permissions'], {'deny': ['Read(.env)'], 'defaultMode': 'acceptEdits'})
        self.assertEqual(config['env'], {'DEMO': 'yes'})
        self.assertEqual(settings.with_name('settings.json.before-power-kit').read_bytes(), original)
        self.assertEqual(install(self.project, power_settings=True), 0)

    def test_fresh_power_settings_and_existing_permission_mode(self):
        install(self.project, power_settings=True)
        settings = self.project / '.claude/settings.json'
        config = json.loads(settings.read_bytes())
        self.assertEqual(config, {'model': 'opusplan', 'permissions': {'defaultMode': 'acceptEdits'}})
        config['permissions']['defaultMode'] = 'plan'
        settings.write_text(json.dumps(config), encoding='utf-8')
        self.assertEqual(install(self.project, power_settings=True), 0)
        self.assertEqual(json.loads(settings.read_bytes())['permissions']['defaultMode'], 'plan')

    def test_invalid_settings_fail_before_any_write(self):
        settings = self.project / '.claude/settings.json'
        settings.parent.mkdir()
        for content in ('{bad', '[]', '{"permissions":false}'):
            settings.write_text(content, encoding='utf-8')
            before = self.snapshot()
            with self.assertRaises(ValueError):
                install(self.project, power_settings=True)
            self.assertEqual(self.snapshot(), before)

    def test_changed_kit_block_is_preserved(self):
        install(self.project)
        instructions = self.project / 'CLAUDE.md'
        instructions.write_bytes(instructions.read_bytes().replace(b'<!-- claude-power-kit:end -->', b'My rule\n<!-- claude-power-kit:end -->'))
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'instructions differ'):
            install(self.project)
        self.assertEqual(self.snapshot(), before)

    def test_old_backup_is_never_overwritten(self):
        (self.project / 'CLAUDE.md').write_bytes(b'Current rules')
        (self.project / 'CLAUDE.md.before-power-kit').write_bytes(b'Older backup')
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'Existing file differs'):
            install(self.project)
        self.assertEqual(self.snapshot(), before)

    def test_symlink_does_not_write_outside_project(self):
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        try:
            (self.project / '.claude').symlink_to(outside, target_is_directory=True)
        except OSError as error:
            self.skipTest(f'Symlinks unavailable on this host: {error}')
        with self.assertRaisesRegex(ValueError, 'symlink'):
            install(self.project)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.project / 'CLAUDE.md').exists())

    def test_tampered_payload_fails_before_install(self):
        bundle = Path(self.temp.name) / 'bundle'
        for name in ('.claude', 'templates'):
            shutil.copytree(ROOT / name, bundle / name)
        shutil.copy2(ROOT / 'checksums.json', bundle / 'checksums.json')
        (bundle / 'templates/CLAUDE.md').write_text('tampered', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'checksum mismatch'):
            install(self.project, root=bundle)
        self.assertEqual(list(self.project.iterdir()), [])


if __name__ == '__main__':
    unittest.main()
