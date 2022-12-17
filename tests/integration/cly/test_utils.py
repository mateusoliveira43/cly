from pathlib import Path
from typing import List, Tuple, Union

import pytest

from cly.utils import run_command, run_multiple_commands

RUN_COMMAND: List[Tuple[Union[str, List[str]], str]] = [
    (["ls", "-a"], "cly"),
    ("git --version", "git version"),
]
RUN_COMMAND_WITH_DIRECTORY: List[Tuple[Union[str, List[str]], str]] = [
    (["ls", "-a"], "test_utils.py"),
    ("git --version", "git version"),
]


@pytest.mark.parametrize("scenario_input,scenario_output", RUN_COMMAND)
def test_run_command(
    scenario_input: Union[str, List[str]],
    scenario_output: str,
    capfd: pytest.CaptureFixture[str],
) -> None:
    run_command(scenario_input)
    output, error = capfd.readouterr()
    assert not error
    assert scenario_output in output


@pytest.mark.parametrize(
    "scenario_input,scenario_output", RUN_COMMAND_WITH_DIRECTORY
)
def test_run_command_with_directory(
    scenario_input: Union[str, List[str]],
    scenario_output: str,
    capfd: pytest.CaptureFixture[str],
) -> None:
    run_command(scenario_input, Path(__file__).parent)
    output, error = capfd.readouterr()
    assert not error
    assert scenario_output in output


def test_run_multiple_commands(
    capfd: pytest.CaptureFixture[str],
) -> None:
    run_multiple_commands([(["ls", "-a"], None), ("git --version", None)])
    output, error = capfd.readouterr()
    assert not error
    assert "cly" in output
    assert "git version" in output


def test_run_multiple_commands_with_directory(
    capfd: pytest.CaptureFixture[str],
) -> None:
    run_multiple_commands(
        [
            (["ls", "-a"], Path(__file__).parent),
            ("git --version", Path(__file__).parent),
        ]
    )
    output, error = capfd.readouterr()
    assert not error
    assert "test_utils.py" in output
    assert "git version" in output


def test_run_multiple_commands_error(
    capfd: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(SystemExit) as sys_exit:
        run_multiple_commands(
            [
                (["ls", "-a"], None),
                ("batman --version", None),
                ("git --version", None),
            ]
        )
    output, error = capfd.readouterr()
    assert "cly" in output
    assert all(word in error for word in ["batman:", "not found"])
    assert "git version" in output
    assert "ERROR: Command 'batman --version' returned non-zero exit" in error
    assert sys_exit.value.code == 1
