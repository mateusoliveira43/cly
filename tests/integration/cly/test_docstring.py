import sys
from typing import Optional
from unittest.mock import patch

import pytest

from cly import config


# pylint: disable=unused-argument
def function_to_test_docstring(
    param1: str, param2: int, param3: Optional[str] = None
) -> str:
    """Just for tests."""


PARAMS = {
    "param1": "A very detailed info",
    "param2": "A small one",
    "param3": "A description with default value",
}
ANOTHER_SUMARY = "Another one complete different."
ANOTHER_PARAM_DESCRIPTION = "I have no more ideas of phrases"
DOCSTRINGS = {
    "NUMPY": """
    Function to test docstring styles.

    Parameters
    ----------
    param1 : str
        A very detailed info.
    param2 : int
        A small one
    param3 : Optional[str], optional
        A description with default value, by default None

    Returns
    -------
    str
        Return information.

    """,
    "GOOGLE": """
    Function to test docstring styles.

    Args:
        param1 (str): A very detailed info.
        param2 (int): A small one
        param3 (Optional[str], optional): A description with default value.
            Defaults to None.

    Returns:
        str: Return information.

    """,
    "SPHINX": """
    Function to test docstring styles.

    :param param1: A very detailed info.
    :type param1: str
    :param param2: A small one
    :type param2: int
    :param param3: A description with default value, defaults to None
    :type param3: Optional[str], optional
    :return: Return information.
    :rtype: str

    """,
}


@pytest.mark.parametrize("style", DOCSTRINGS)
def test_get_command_help_from_docstring(
    style: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    function_to_test_docstring.__doc__ = DOCSTRINGS[style]
    cli_config = {
        "name": "Test",
        "description": "",
        "epilog": "",
        "version": "test",
    }
    cli = config.ConfiguredParser(cli_config)
    command = cli.create_command(function_to_test_docstring)
    command.add_argument(
        "-t",
        "--test",
        action="store_true",
    )
    cli.parser.print_help()
    output, error = capsys.readouterr()
    assert not error
    assert all(
        word in output
        for word in "Function to test docstring styles".split(" ")
    )


def test_get_command_help_from_docstring_with_no_style(
    capsys: pytest.CaptureFixture[str],
) -> None:
    function_to_test_docstring.__doc__ = (
        """Function to test docstring styles."""
    )
    cli_config = {
        "name": "Test",
        "description": "",
        "epilog": "",
        "version": "test",
    }
    cli = config.ConfiguredParser(cli_config)
    command = cli.create_command(function_to_test_docstring)
    command.add_argument(
        "-t",
        "--test",
        action="store_true",
    )
    cli.parser.print_help()
    output, error = capsys.readouterr()
    assert not error
    assert all(
        word in output
        for word in "Function to test docstring styles".split(" ")
    )


@pytest.mark.parametrize("style", DOCSTRINGS)
def test_command_help_priority_from_docstring(
    style: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    function_to_test_docstring.__doc__ = DOCSTRINGS[style]
    cli_config = {
        "name": "Test",
        "description": "",
        "epilog": "",
        "version": "test",
    }
    cli = config.ConfiguredParser(cli_config)
    command = cli.create_command(
        function_to_test_docstring, help_message=ANOTHER_SUMARY
    )
    command.add_argument(
        "-t",
        "--test",
        action="store_true",
    )
    cli.parser.print_help()
    output, error = capsys.readouterr()
    assert not error
    assert "Function to test docstring styles." not in output
    assert all(word in output for word in ANOTHER_SUMARY.split(" "))


def test_command_help_priority_from_docstring_with_no_style(
    capsys: pytest.CaptureFixture[str],
) -> None:
    function_to_test_docstring.__doc__ = (
        """Function to test docstring styles."""
    )
    cli_config = {
        "name": "Test",
        "description": "",
        "epilog": "",
        "version": "test",
    }
    cli = config.ConfiguredParser(cli_config)
    command = cli.create_command(
        function_to_test_docstring, help_message=ANOTHER_SUMARY
    )
    command.add_argument(
        "-t",
        "--test",
        action="store_true",
    )
    cli.parser.print_help()
    output, error = capsys.readouterr()
    assert not error
    assert "Function to test docstring styles." not in output
    assert all(word in output for word in ANOTHER_SUMARY.split(" "))


@pytest.mark.parametrize("style", DOCSTRINGS)
@pytest.mark.parametrize("param", PARAMS)
def test_get_param_help_from_docstring(
    param: str,
    style: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    function_to_test_docstring.__doc__ = DOCSTRINGS[style]
    cli_config = {
        "name": "Test",
        "description": "",
        "epilog": "",
        "version": "test",
    }
    cli = config.ConfiguredParser(cli_config)
    command = cli.create_command(function_to_test_docstring)
    command.add_argument(
        "-p",
        f"--{param}",
        action="store_true",
    )
    sys_mock = ["file_name", "function_to_test_docstring", "--help"]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            cli()
    output, error = capsys.readouterr()
    assert not error
    assert all(word in output for word in PARAMS[param].split(" "))
    assert sys_exit.value.code == 0


@pytest.mark.parametrize("style", DOCSTRINGS)
@pytest.mark.parametrize("param", PARAMS)
def test_param_help_priority(
    param: str,
    style: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    function_to_test_docstring.__doc__ = DOCSTRINGS[style]
    cli_config = {
        "name": "Test",
        "description": "",
        "epilog": "",
        "version": "test",
    }
    cli = config.ConfiguredParser(cli_config)
    command = cli.create_command(function_to_test_docstring)
    command.add_argument(
        "-p", f"--{param}", action="store_true", help=ANOTHER_PARAM_DESCRIPTION
    )
    sys_mock = ["file_name", "function_to_test_docstring", "--help"]
    with patch.object(sys, "argv", sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            cli()
    output, error = capsys.readouterr()
    assert not error
    assert PARAMS[param] not in output
    assert all(word in output for word in ANOTHER_PARAM_DESCRIPTION.split(" "))
    assert sys_exit.value.code == 0


# TODO test get param help with description breaking lines
