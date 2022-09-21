from typing import List

import pytest

from cly.testing import run_cli

from ..batcomputer_cli.__main__ import CLI
from ..batcomputer_cli.database import CHARACTERS

USAGE_PREFIX = "Usage:\n  [python|python3] "
USAGE_FLAGS = ["[-h]", "[-v]", "[-o]", "command", "..."]

OPTIONS = {
    "help": [["-h"], ["--help"]],
    "version": [["-v"], ["--version"]],
    "oracle": [["-o"], ["--oracle"]],
}
COMMAND_OPTIONS = [[""], *OPTIONS["oracle"]]
COMMAND_HELPS = {
    "id": ["Identify", "the", "person", "behind", "each", "alias"],
    "ls": ["List", "all", "aliases", "in", "Batcomputer"],
}

INVALID_USAGE = {
    "FLAGS": ["-w", "--wrong", "--invalid"],
    "COMMANDS": ["riddler", "penguin"],
    "COMMAND_FLAGS": ["-k", "-v", "-batman"],
}
ERROR_MESSAGES = {
    "NO_COMMAND": "arguments are required: command",
    "UNRECOGNIZED_ARGUMENTS": "unrecognized arguments",
    "INVALID_CHOICE": "argument command: invalid choice",
}


def test_example_cli_without_options() -> None:
    exit_code, stdout, stderr = run_cli(CLI, [])
    assert not stderr
    assert USAGE_PREFIX in stdout
    assert all(option in stdout for option in USAGE_FLAGS)
    assert all(word in stdout for word in COMMAND_HELPS["id"])
    assert all(word in stdout for word in COMMAND_HELPS["ls"])
    assert exit_code == 0


@pytest.mark.parametrize("option", OPTIONS["help"])
def test_example_cli_with_option_help(option: List[str]) -> None:
    exit_code, stdout, stderr = run_cli(CLI, option)
    assert not stderr
    assert USAGE_PREFIX in stdout
    assert all(option in stdout for option in USAGE_FLAGS)
    assert all(word in stdout for word in COMMAND_HELPS["id"])
    assert all(word in stdout for word in COMMAND_HELPS["ls"])
    assert exit_code == 0


@pytest.mark.parametrize("option", OPTIONS["version"])
def test_example_cli_with_option_version(option: List[str]) -> None:
    exit_code, stdout, stderr = run_cli(CLI, option)
    assert not stderr
    assert "version" in stdout
    assert exit_code == 0


@pytest.mark.parametrize("option", OPTIONS["oracle"])
def test_example_cli_with_option_oracle_without_command(
    option: List[str],
) -> None:
    exit_code, stdout, stderr = run_cli(CLI, option)
    assert not stdout
    assert ERROR_MESSAGES["NO_COMMAND"] in stderr
    assert exit_code == 2


@pytest.mark.parametrize("option", INVALID_USAGE["FLAGS"])
def test_example_cli_without_command(option: str) -> None:
    exit_code, stdout, stderr = run_cli(CLI, [option])
    assert not stdout
    assert ERROR_MESSAGES["NO_COMMAND"] in stderr
    assert exit_code == 2


@pytest.mark.parametrize("option", INVALID_USAGE["FLAGS"])
def test_example_cli_with_invalid_options_with_command_ls(option: str) -> None:
    exit_code, stdout, stderr = run_cli(CLI, [option, "ls"])
    assert not stdout
    assert ERROR_MESSAGES["UNRECOGNIZED_ARGUMENTS"] in stderr
    assert exit_code == 2


@pytest.mark.parametrize("option", INVALID_USAGE["FLAGS"])
def test_example_cli_with_invalid_options_with_command_id(option: str) -> None:
    exit_code, stdout, stderr = run_cli(CLI, [option, "id", "batman"])
    assert not stdout
    assert ERROR_MESSAGES["UNRECOGNIZED_ARGUMENTS"] in stderr
    assert exit_code == 2


@pytest.mark.parametrize("command", INVALID_USAGE["COMMANDS"])
def test_example_cli_invalid_commands(command: str) -> None:
    exit_code, stdout, stderr = run_cli(CLI, [command])
    assert not stdout
    assert ERROR_MESSAGES["INVALID_CHOICE"] in stderr
    assert exit_code == 2


@pytest.mark.parametrize("option", OPTIONS["help"])
def test_example_cli_command_id_with_option_help(option: List[str]) -> None:
    exit_code, stdout, stderr = run_cli(CLI, ["id"] + option)
    assert not stderr
    assert USAGE_PREFIX in stdout
    assert all(word in stdout for word in COMMAND_HELPS["id"])
    assert all(
        word in stdout
        for word in [
            "One",
            "or",
            "more",
            "alias",
            "to",
            "be",
            "identified",
            "separated",
            "by",
            "spaces",
        ]
    )
    assert exit_code == 0


@pytest.mark.parametrize("option", OPTIONS["help"])
def test_example_cli_command_ls_with_option_help(option: List[str]) -> None:
    exit_code, stdout, stderr = run_cli(CLI, ["ls"] + option)
    assert not stderr
    assert USAGE_PREFIX in stdout
    assert all(word in stdout for word in COMMAND_HELPS["ls"])
    assert exit_code == 0


@pytest.mark.parametrize("args", INVALID_USAGE["COMMAND_FLAGS"])
def test_example_cli_command_id_with_invalid_arguments(args: str) -> None:
    exit_code, stdout, stderr = run_cli(CLI, ["id", args, "joker"])
    assert not stdout
    assert ERROR_MESSAGES["UNRECOGNIZED_ARGUMENTS"] in stderr
    assert exit_code == 2


@pytest.mark.parametrize("args", INVALID_USAGE["COMMAND_FLAGS"])
def test_example_cli_command_ls_with_invalid_arguments(args: str) -> None:
    exit_code, stdout, stderr = run_cli(CLI, ["ls", args])
    assert not stdout
    assert ERROR_MESSAGES["UNRECOGNIZED_ARGUMENTS"] in stderr
    assert exit_code == 2


@pytest.mark.parametrize("option", COMMAND_OPTIONS)
def test_example_cli_command_id(option: List[str]) -> None:
    sys_mock = list(filter(None, [*option, "id", "joker", "penguin"]))
    exit_code, stdout, stderr = run_cli(CLI, sys_mock)
    assert "A.K.A." in stdout
    assert "not identified" in stderr
    assert exit_code == 0


@pytest.mark.parametrize("option", COMMAND_OPTIONS)
def test_example_cli_command_ls(option: List[str]) -> None:
    sys_mock = list(filter(None, [*option, "ls"]))
    exit_code, stdout, stderr = run_cli(CLI, sys_mock)
    assert not stderr
    assert all(character.title() in stdout for character in CHARACTERS)
    assert exit_code == 0
