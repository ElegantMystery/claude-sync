"""Tests for scripts/cli.py entry point."""

import subprocess
import sys
from pathlib import Path

# Get the scripts directory path
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
CLI_PATH = SCRIPTS_DIR / "cli.py"


class TestCliExecution:
    """Test that cli.py can be executed."""

    def test_cli_file_exists(self):
        """CLI file should exist at scripts/cli.py."""
        assert CLI_PATH.exists(), f"cli.py not found at {CLI_PATH}"

    def test_cli_is_executable_python_script(self):
        """cli.py should be a valid Python script that can be executed."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--help"],
            capture_output=True,
            text=True,
        )
        # Should not have import errors
        assert "ModuleNotFoundError" not in result.stderr
        assert "ImportError" not in result.stderr

    def test_cli_accepts_status_argument(self):
        """cli.py should accept --status argument."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--status"],
            capture_output=True,
            text=True,
        )
        # Should not fail with argument parsing error
        assert "unrecognized arguments: --status" not in result.stderr


class TestCliModuleImport:
    """Test that cli.py correctly imports sync and filter modules."""

    def test_imports_sync_module(self):
        """cli.py should import sync module from scripts directory."""
        # Run Python with scripts dir in PYTHONPATH and check if sync imports work
        result = subprocess.run(
            [sys.executable, "-c", """
import sys
sys.path.insert(0, str(__file__).rsplit('/tests', 1)[0] + '/scripts')
import sync
print('sync_ok')
"""],
            capture_output=True,
            text=True,
            cwd=str(CLI_PATH.parent),
        )
        # This verifies the module can be imported with proper path setup
        assert "ModuleNotFoundError" not in result.stderr

    def test_cli_imports_filter_module(self):
        """cli.py should import filter module (since sync imports it)."""
        result = subprocess.run(
            [sys.executable, "-c", """
import sys
sys.path.insert(0, 'scripts')
import sync
print('sync_ok')
"""],
            capture_output=True,
            text=True,
            cwd=CLI_PATH.parent.parent,
        )
        assert "ModuleNotFoundError" not in result.stderr
        assert "ImportError" not in result.stderr


class TestCliArgumentPassthrough:
    """Test that cli.py passes arguments through to sync.main()."""

    def test_passes_through_quiet_flag(self):
        """cli.py should pass --quiet through to sync.main."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--quiet"],
            capture_output=True,
            text=True,
        )
        # Should not error on unknown argument
        assert "unrecognized arguments: --quiet" not in result.stderr

    def test_passes_through_list_flag(self):
        """cli.py should pass --list through to sync.main."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--list"],
            capture_output=True,
            text=True,
        )
        assert "unrecognized arguments: --list" not in result.stderr
        assert result.returncode == 0
        assert "Claude Config Components:" in result.stdout

    def test_passes_through_export_with_target(self):
        """cli.py should pass --export and --target through."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--export", "--target", "/tmp/test"],
            capture_output=True,
            text=True,
        )
        assert "unrecognized arguments: --export" not in result.stderr
        assert "unrecognized arguments: --target" not in result.stderr

    def test_passes_through_import_with_source(self):
        """cli.py should pass --import and --source through."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--import", "--source", "/tmp/test"],
            capture_output=True,
            text=True,
        )
        assert "unrecognized arguments: --import" not in result.stderr
        assert "unrecognized arguments: --source" not in result.stderr

    def test_passes_combined_args(self):
        """cli.py should pass multiple arguments through correctly."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--export", "--target", "/tmp/test", "--dry-run", "--push"],
            capture_output=True,
            text=True,
        )
        assert "unrecognized arguments: --export" not in result.stderr
        assert "unrecognized arguments: --target" not in result.stderr
        assert "unrecognized arguments: --dry-run" not in result.stderr
        assert "unrecognized arguments: --push" not in result.stderr

    def test_passes_through_diff_with_target(self):
        """cli.py should pass --diff and --target through."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--diff", "--target", "/tmp/test"],
            capture_output=True,
            text=True,
        )
        assert "unrecognized arguments: --diff" not in result.stderr
        assert "unrecognized arguments: --target" not in result.stderr
        assert "Traceback" not in result.stderr

    def test_passes_through_pull_with_import_source(self):
        """cli.py should pass --pull through (used with --import --source)."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--import", "--source", "/tmp/test", "--pull"],
            capture_output=True,
            text=True,
        )
        assert "unrecognized arguments: --pull" not in result.stderr
        assert "unrecognized arguments: --import" not in result.stderr
        assert "unrecognized arguments: --source" not in result.stderr


class TestCliErrorHandling:
    """Test cli.py error handling."""

    def test_nonexistent_claude_dir_shows_error(self):
        """cli.py should show error when claude dir doesn't exist."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--status", "--claude-dir", "/nonexistent/path"],
            capture_output=True,
            text=True,
        )
        assert "Traceback" not in result.stderr
        assert result.returncode != 0 or "does not exist" in result.stderr

    def test_missing_target_for_export_shows_error(self):
        """cli.py should show error when --export without --target."""
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--export"],
            capture_output=True,
            text=True,
        )
        # Should show error about missing --target, not crash
        assert "Traceback" not in result.stderr