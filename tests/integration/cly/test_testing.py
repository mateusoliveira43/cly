from pathlib import Path

from cly import config
from cly.testing import run_cli
from cly.utils import run_command, run_multiple_commands


def example_command() -> None:
    run_command("ls", Path(__file__).parent)
    print("did you get me?")
    run_multiple_commands(
        [
            ("git --version", None),
            ("batman --version", None),
            ("python --version", None),
        ]
    )


CLI_CONFIG = {
    "name": "Test",
    "description": "Test testing environment.",
    "epilog": "Epilog",
    "version": "1.0.0",
}

CLI = config.ConfiguredParser(CLI_CONFIG)
CLI.create_command(example_command, alias="example")


def test_run_cli() -> None:
    returncode, stdout, stderr = run_cli(CLI, ["example"])
    assert "test_testing.py" in stdout
    assert "did you get me?" in stdout
    assert "git version" in stdout
    assert all(word in stderr for word in ["batman:", "not found"])
    assert "Python" in stdout
    assert "ERROR:" in stderr
    assert returncode == 1
