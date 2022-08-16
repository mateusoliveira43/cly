import sys
from runpy import run_path
from typing import List
from unittest.mock import patch

import pytest

from example.database import CHARACTERS
from tests import ABSOLUTE_PATH

EXAMPLE_FILE = (ABSOLUTE_PATH / "batcomputer.py").as_posix()

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


def test_example_cli_without_options(
    capsys: pytest.CaptureFixture[str],
) -> None:
    sys_mock = ["file_name"]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not error
    assert USAGE_PREFIX in output
    assert all(option in output for option in USAGE_FLAGS)
    assert all(word in output for word in COMMAND_HELPS["id"])
    assert all(word in output for word in COMMAND_HELPS["ls"])
    assert sys_exit.value.code == 0


@pytest.mark.parametrize("option", OPTIONS["help"])
def test_example_cli_with_option_help(
    option: List[str], capsys: pytest.CaptureFixture[str]
) -> None:
    sys_mock = ["file_name", *option]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not error
    assert USAGE_PREFIX in output
    assert all(option in output for option in USAGE_FLAGS)
    assert all(word in output for word in COMMAND_HELPS["id"])
    assert all(word in output for word in COMMAND_HELPS["ls"])
    assert sys_exit.value.code == 0


@pytest.mark.parametrize("option", OPTIONS["version"])
def test_example_cli_with_option_version(
    option: List[str], capsys: pytest.CaptureFixture[str]
) -> None:
    sys_mock = ["file_name", *option]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not error
    assert "version" in output
    assert sys_exit.value.code == 0


@pytest.mark.parametrize("option", OPTIONS["oracle"])
def test_example_cli_with_option_oracle_without_command(
    option: List[str], capfd: pytest.CaptureFixture[str]
) -> None:
    sys_mock = ["file_name", *option]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capfd.readouterr()
    assert ERROR_MESSAGES["NO_COMMAND"] in error
    assert not output
    assert sys_exit.value.code == 2


@pytest.mark.parametrize("option", INVALID_USAGE["FLAGS"])
def test_example_cli_without_command(
    option: str, capsys: pytest.CaptureFixture[str]
) -> None:
    sys_mock = ["file_name", option]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert ERROR_MESSAGES["NO_COMMAND"] in error
    assert not output
    assert sys_exit.value.code == 2


@pytest.mark.parametrize("option", OPTIONS["oracle"])
def test_example_cli_with_option_oracle_with_command(
    option: List[str], capfd: pytest.CaptureFixture[str]
) -> None:
    sys_mock = ["file_name", *option]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capfd.readouterr()
    assert ERROR_MESSAGES["NO_COMMAND"] in error
    assert not output
    assert sys_exit.value.code == 2


@pytest.mark.parametrize("option", INVALID_USAGE["FLAGS"])
def test_example_cli_with_invalid_options_with_command_ls(
    option: str, capsys: pytest.CaptureFixture[str]
) -> None:
    sys_mock = ["file_name", option, "ls"]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert ERROR_MESSAGES["UNRECOGNIZED_ARGUMENTS"] in error
    assert not output
    assert sys_exit.value.code == 2


@pytest.mark.parametrize("option", INVALID_USAGE["FLAGS"])
def test_example_cli_with_invalid_options_with_command_id(
    option: str, capsys: pytest.CaptureFixture[str]
) -> None:
    sys_mock = ["file_name", option, "id", "batman"]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert ERROR_MESSAGES["UNRECOGNIZED_ARGUMENTS"] in error
    assert not output
    assert sys_exit.value.code == 2


@pytest.mark.parametrize("command", INVALID_USAGE["COMMANDS"])
def test_example_cli_invalid_commands(
    command: str, capsys: pytest.CaptureFixture[str]
) -> None:
    sys_mock = ["file_name", command]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert ERROR_MESSAGES["INVALID_CHOICE"] in error
    assert not output
    assert sys_exit.value.code == 2


@pytest.mark.parametrize("option", OPTIONS["help"])
def test_example_cli_command_id_with_option_help(
    option: List[str], capsys: pytest.CaptureFixture[str]
) -> None:
    sys_mock = ["file_name", "id", *option]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not error
    assert USAGE_PREFIX in output
    assert all(word in output for word in COMMAND_HELPS["id"])
    assert all(
        word in output
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
    assert sys_exit.value.code == 0


@pytest.mark.parametrize("option", OPTIONS["help"])
def test_example_cli_command_ls_with_option_help(
    option: List[str], capsys: pytest.CaptureFixture[str]
) -> None:
    sys_mock = ["file_name", "ls", *option]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not error
    assert USAGE_PREFIX in output
    for word in COMMAND_HELPS["ls"]:
        assert word in output
    assert all(word in output for word in COMMAND_HELPS["ls"])
    assert sys_exit.value.code == 0


@pytest.mark.parametrize("args", INVALID_USAGE["COMMAND_FLAGS"])
def test_example_cli_command_id_with_invalid_arguments(
    args: str, capsys: pytest.CaptureFixture[str]
) -> None:
    sys_mock = ["file_name", "id", args, "joker"]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not output
    assert ERROR_MESSAGES["UNRECOGNIZED_ARGUMENTS"] in error
    assert sys_exit.value.code == 2


@pytest.mark.parametrize("args", INVALID_USAGE["COMMAND_FLAGS"])
def test_example_cli_command_ls_with_invalid_arguments(
    args: str, capsys: pytest.CaptureFixture[str]
) -> None:
    sys_mock = ["file_name", "ls", args]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not output
    assert ERROR_MESSAGES["UNRECOGNIZED_ARGUMENTS"] in error
    assert sys_exit.value.code == 2


@pytest.mark.parametrize("option", COMMAND_OPTIONS)
def test_example_cli_command_id(
    option: List[str], capsys: pytest.CaptureFixture[str]
) -> None:
    sys_mock = list(
        filter(None, ["file_name", *option, "id", "joker", "penguin"])
    )
    with patch.object(sys, "argv", sys_mock):
        run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not error
    assert "A.K.A." in output
    assert "not identified" in output


@pytest.mark.parametrize("option", COMMAND_OPTIONS)
def test_example_cli_command_ls(
    option: List[str], capsys: pytest.CaptureFixture[str]
) -> None:
    sys_mock = list(filter(None, ["file_name", *option, "ls"]))
    with patch.object(sys, "argv", sys_mock):
        run_path(EXAMPLE_FILE, run_name="__main__")
    output, error = capsys.readouterr()
    assert not error
    assert all(character.title() in output for character in CHARACTERS)
