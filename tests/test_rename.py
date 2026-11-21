#!/usr/bin/env python3
"""The 0.6 rename: what 0.5 (Context Layer) wrote or named keeps working (docs/RENAME.md).

Covers the environment fallback, the `context-layer` console entry, the `context_layer`
import shim, and the host entries, hook commands, plan marker and rule-file markers a 0.5
install left behind. Every test uses a disposable directory; nothing reads a real host.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import warnings

from _portable_helpers import isolated_home_env

REPO = Path(os.environ.get("TEST_REPO_HOME", Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(REPO))

from paracortex import __version__, cli, install, naming, rules  # noqa: E402


def legacy_mcp_entry(vault: Path, module: bool = False) -> dict:
    """The entry 0.5 wrote: the console script, or `python -m context_layer.cli`."""
    if module:
        return {"command": sys.executable,
                "args": ["-m", "context_layer.cli", "mcp", "--vault", str(vault)],
                "env": {"PYTHONUTF8": "1"}}
    return {"command": "/opt/tools/bin/context-layer", "args": ["mcp", "--vault", str(vault)]}


class Environment(unittest.TestCase):
    def test_new_name_first_then_the_0_5_spelling(self):
        self.assertEqual(naming.getenv("PARACORTEX_SESSION", environ={
            "PARACORTEX_SESSION": "new", "CONTEXT_LAYER_SESSION": "old"}), "new")
        self.assertEqual(naming.getenv("PARACORTEX_SESSION", environ={
            "CONTEXT_LAYER_SESSION": "old"}), "old")
        self.assertIsNone(naming.getenv("PARACORTEX_SESSION", environ={}))
        self.assertEqual(naming.getenv("PARACORTEX_SESSION", "d", environ={}), "d")

    def test_an_empty_new_variable_overrides_the_old_one(self):
        self.assertEqual(naming.getenv("PARACORTEX_TOOL", environ={
            "PARACORTEX_TOOL": "", "CONTEXT_LAYER_TOOL": "old"}), "")

    def test_other_variables_have_no_fallback(self):
        self.assertIsNone(naming.getenv("HOME_X", environ={"CONTEXT_LAYER_HOME_X": "x"}))

    def test_child_processes_get_both_spellings(self):
        env = naming.child_env({}, "PARACORTEX_OUT_DIR", "/tmp/out")
        self.assertEqual(env, {"PARACORTEX_OUT_DIR": "/tmp/out",
                               "CONTEXT_LAYER_OUT_DIR": "/tmp/out"})
        self.assertEqual(naming.drop_env(env, "PARACORTEX_OUT_DIR"), {})

    def test_the_memory_session_reads_the_old_variable(self):
        from paracortex import memory
        with mock.patch.dict(os.environ, {"CONTEXT_LAYER_SESSION": "s-old"}, clear=False):
            os.environ.pop("PARACORTEX_SESSION", None)
            self.assertEqual(memory._env(memory.SESSION_ENV), "s-old")


class LegacyCommand(unittest.TestCase):
    def test_legacy_main_adds_one_stderr_line_and_leaves_stdout_alone(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.legacy_main(["--version"])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue(), f"paracortex {__version__}\n")
        self.assertEqual(err.getvalue().count("\n"), 1)
        self.assertIn("now `paracortex`", err.getvalue())

    def test_python_m_context_layer_cli_runs_paracortex(self):
        env = dict(os.environ, PYTHONPATH=str(REPO))
        done = subprocess.run([sys.executable, "-m", "context_layer.cli", "--version"],
                              cwd=REPO, env=env, capture_output=True, text=True, timeout=60)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertEqual(done.stdout, f"paracortex {__version__}\n")
        self.assertIn("docs/RENAME.md", done.stderr)


class ImportShim(unittest.TestCase):
    def test_import_warns_and_aliases_the_same_modules(self):
        sys.modules.pop("context_layer", None)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            import context_layer
        self.assertTrue(any(issubclass(w.category, DeprecationWarning) for w in caught))
        self.assertEqual(context_layer.__version__, __version__)
        import context_layer.memory as old_memory
        from context_layer import tasks as old_tasks
        import paracortex.memory
        import paracortex.tasks
        self.assertIs(old_memory, paracortex.memory)
        self.assertIs(old_tasks, paracortex.tasks)
        self.assertEqual(paracortex.memory.__spec__.name, "paracortex.memory")
        with self.assertRaises(ModuleNotFoundError):
            import context_layer.no_such_module  # noqa: F401
        with self.assertRaises(AttributeError):
            context_layer.no_such_attribute


class LeftoverDistribution(unittest.TestCase):
    """pip keeps the 0.5 modules in context_layer/ when `context-layer` was not uninstalled
    before 0.6 went in; the shim must alias past them, and doctor must say so."""

    def test_stale_0_5_modules_beside_the_shim_never_load(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = os.path.realpath(temp)
            stale = Path(temp) / "context_layer"
            stale.mkdir()
            for name in ("__init__.py", "cli.py"):
                (stale / name).write_bytes((REPO / "context_layer" / name).read_bytes())
            (stale / "memory.py").write_text("STALE = True\n", encoding="utf-8")
            env = dict(os.environ, PYTHONPATH=os.pathsep.join([temp, str(REPO)]))
            code = ("import warnings; warnings.simplefilter('ignore'); "
                    "import context_layer, context_layer.memory as m, paracortex.memory as p; "
                    "import os; print(os.path.realpath(context_layer.__file__).startswith(%r), "
                    "hasattr(m, 'STALE'), m is p)"
                    % temp)
            done = subprocess.run([sys.executable, "-c", code], cwd=temp, env=env,
                                  capture_output=True, text=True, timeout=60)
            self.assertEqual(done.returncode, 0, done.stderr)
            self.assertEqual(done.stdout.split(), ["True", "False", "True"])

    def test_doctor_names_a_leftover_0_5_distribution(self):
        from paracortex import doctor
        with mock.patch.object(doctor, "legacy_distribution", return_value="0.5.0"):
            report = doctor.Report()
            doctor.check_runtime(report)
        rows = [check for check in report.checks if check["name"] == "context-layer"]
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["status"], doctor.WARN)
        self.assertIn("pip uninstall context-layer", rows[0]["detail"])
        with mock.patch.object(doctor, "legacy_distribution", return_value=None):
            report = doctor.Report()
            doctor.check_runtime(report)
        self.assertFalse([c for c in report.checks if c["name"] == "context-layer"])


class HostEntries(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.vault = self.root / "vault"
        self.vault.mkdir()
        self.project = self.root / "project"
        self.project.mkdir()
        patcher = mock.patch.dict(os.environ, isolated_home_env(os.environ, self.root / "home"),
                                  clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)

    def write_mcp(self, servers: dict) -> Path:
        path = self.project / ".mcp.json"
        path.write_text(json.dumps({"mcpServers": servers}), encoding="utf-8")
        return path

    def change(self, removing: bool):
        with contextlib.redirect_stderr(io.StringIO()) as err:
            change = install.claude_mcp_change(self.project, self.vault, removing)
        return change, err.getvalue()

    def test_install_replaces_our_0_5_entry(self):
        for module in (False, True):
            with self.subTest(module=module):
                self.write_mcp({"context-layer": legacy_mcp_entry(self.vault, module),
                                "notes": {"command": "other-server"}})
                change, err = self.change(removing=False)
                servers = json.loads(change.new)["mcpServers"]
                self.assertEqual(sorted(servers), ["notes", "paracortex"])
                self.assertIn("replaced by `paracortex`", err)
                self.assertFalse(change.own)          # another server: a backup is kept

    def test_uninstall_removes_our_0_5_entry(self):
        self.write_mcp({"context-layer": legacy_mcp_entry(self.vault)})
        change, err = self.change(removing=True)
        self.assertIsNone(change.new)
        self.assertTrue(change.own)
        self.assertIn("removed", err)

    def test_a_user_server_named_context_layer_is_left_alone(self):
        theirs = {"command": "node", "args": ["their-server.js"]}
        self.write_mcp({"context-layer": theirs})
        change, err = self.change(removing=False)
        servers = json.loads(change.new)["mcpServers"]
        self.assertEqual(servers["context-layer"], theirs)
        self.assertIn("paracortex", servers)
        self.assertEqual(err, "")
        change, _ = self.change(removing=True)
        self.assertEqual(json.loads(change.new)["mcpServers"], {"context-layer": theirs})

    def test_0_5_hook_commands_are_recognised(self):
        for command in ("PYTHONUTF8=1 /opt/tools/bin/context-layer hook claude-code --vault /v",
                        "PYTHONUTF8=1 /usr/bin/python3 -m context_layer.cli hook codex --vault /v",
                        "/opt/tools/bin/paracortex hook claude-code --vault /v"):
            with self.subTest(command=command):
                self.assertTrue(install.is_ours(command))
        self.assertTrue(install.is_ours_rules("context-layer rules hook stop --vault /v"))
        self.assertFalse(install.is_ours("other-tool hook claude-code"))

    def test_a_0_5_hook_is_replaced_not_duplicated(self):
        settings = self.project / ".claude" / "settings.json"
        settings.parent.mkdir()
        old = {"type": "command", "command": "/opt/tools/bin/context-layer hook claude-code "
               f"--vault {self.vault}", "timeout": 30}
        settings.write_text(json.dumps({"hooks": {"UserPromptSubmit": [{"hooks": [old]}]}}),
                            encoding="utf-8")
        changes = install.claude_settings_changes(self.project, self.vault, removing=False,
                                                  prompt_hook=True, rules_hooks=False,
                                                  plan_default=False)
        data = json.loads(next(c for c in changes if c.path == settings).new)
        commands = [hook["command"] for group in data["hooks"]["UserPromptSubmit"]
                    for hook in group["hooks"]]
        self.assertEqual(len(commands), 1)
        self.assertNotIn("context-layer", commands[0])

    def test_a_0_5_plan_marker_stays_in_use(self):
        folder = self.project / ".claude"
        folder.mkdir()
        self.assertEqual(install.plan_marker(self.project).name, install.PLAN_MARKER)
        (folder / install.LEGACY_PLAN_MARKER).write_text("{}", encoding="utf-8")
        self.assertEqual(install.plan_marker(self.project).name, install.LEGACY_PLAN_MARKER)
        (folder / install.PLAN_MARKER).write_text("{}", encoding="utf-8")
        self.assertEqual(install.plan_marker(self.project).name, install.PLAN_MARKER)

    def test_codex_0_5_block_is_replaced_and_removed(self):
        codex = self.root / "codex"
        codex.mkdir()
        os.environ["CODEX_HOME"] = str(codex)
        config = codex / "config.toml"
        config.write_text('model = "x"\n\n# >>> context-layer >>>\n'
                          '[mcp_servers.context_layer]\ncommand = "context-layer"\n'
                          'args = ["mcp"]\n# <<< context-layer <<<\n', encoding="utf-8")
        with contextlib.redirect_stderr(io.StringIO()):
            installed = install.codex_change(self.vault, removing=False)
            removed = install.codex_change(self.vault, removing=True)
        self.assertNotIn("context_layer", installed.new)
        self.assertIn("[mcp_servers.paracortex]", installed.new)
        self.assertEqual(installed.new.count("[mcp_servers."), 1)
        self.assertEqual(removed.new, 'model = "x"\n\n')


class RuleMarkers(unittest.TestCase):
    def test_a_0_5_rule_file_keeps_its_markers(self):
        start, end = rules.LEGACY_MARKS
        text = f"# Rules\n\n## Work records\n\n{start}\n{end}\n"
        self.assertEqual(rules._records_region(text), "\n")
        updated, _ = rules._with_entry(text, "### entry one\n", keep=10)
        self.assertIn(f"{start}\n### entry one\n{end}", updated)
        self.assertNotIn(rules.START_MARK, updated)
        self.assertEqual(rules._records_region(updated).strip(), "### entry one")

    def test_a_new_rule_file_gets_the_new_markers(self):
        updated, _ = rules._with_entry("# Rules\n", "### entry\n", keep=10)
        self.assertIn(rules.START_MARK, updated)
        self.assertNotIn(rules.LEGACY_MARKS[0], updated)


if __name__ == "__main__":
    unittest.main()
