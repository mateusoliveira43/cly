from contextlib import nullcontext

from cly import config
from cly.testing import run_cli

CLI_CONFIG = {
    "name": "CLI without commands",
    "description": "Test if no exceptions are raised.",
    "epilog": "bug tm",
    "version": "1.2.3",
}

CLI = config.ConfiguredParser(CLI_CONFIG)
CLI.parser.add_argument(
    "-e",
    "--example",
    action="store_true",
    help="Example flag.",
)


def test_cli_without_commands() -> None:
    with nullcontext() as sys_exit:
        run_cli(CLI, [])
    assert sys_exit is None
