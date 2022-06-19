"""Unit tests of module scripts.cli.utils."""

import subprocess
from typing import Dict, List, Union
from unittest.mock import Mock, patch

import pytest

from scripts.cli.colors import color_text
from scripts.cli.utils import (
    get_output,
    get_returncode,
    get_standard_output,
    parse_arguments,
    run_command,
)

PARSE_ARGUMENTS_DATA = [
    {"input": ["the", "dark", "knight"], "output": "the dark knight"},
    {"input": ["-r", "command", "-v", "1"], "output": "-r command -v 1"},
    {"input": 'grep -Inr "batman" .', "output": 'grep -Inr "batman" .'},
]
GET_OUTPUT_DATA = [
    {"input": ["joker", "--help"], "parsed": "joker --help"},
    {"input": "batman --version", "parsed": "batman --version"},
]
RETURNCODE_DATA = [
    {"input": ["joker", "--help"], "mock": 0},
    {"input": "batman --version", "mock": 127},
]
OUTPUT_DATA = [
    {
        "input": ["joker", "--help"],
        "mock": "Why\nso\nserious\n?",
        "output": ["Why", "so", "serious", "?"],
        "lines": ["Why", "so", "serious", "?"],
    },
    {
        "input": "dent --version",
        "mock": (
            "You either die a hero\nor you live long enough to see yourself "
            "become the villain"
        ),
        "output": [
            "You",
            "either",
            "die",
            "a",
            "hero",
            "or",
            "you",
            "live",
            "long",
            "enough",
            "to",
            "see",
            "yourself",
            "become",
            "the",
            "villain",
        ],
        "lines": [
            "You either die a hero",
            "or you live long enough to see yourself become the villain",
        ],
    },
    {
        "input": "batman --version",
        "mock": "",
        "output": None,
        "lines": None,
    },
]
RUN_COMMAND_SUCCESS_DATA = [
    {
        "input": ["joker", "--help"],
        "output": "Why\nso\nserious\n?\n",
    },
    {"input": "batman --version", "output": "Batman 1.2.3\n"},
]
RUN_COMMAND_ERROR_DATA = [
    {"input": ["riddler", "--help"], "return_code": 127},
    {"input": "batman --version", "return_code": 1},
]


@pytest.mark.parametrize("scenario", PARSE_ARGUMENTS_DATA)
def test_parse_arguments(scenario: Dict[str, Union[str, List[str]]]) -> None:
    """Test parse_arguments."""
    output = parse_arguments(scenario["input"])
    assert output == scenario["output"]


@pytest.mark.parametrize("scenario", GET_OUTPUT_DATA)
@patch("subprocess.run")
def test_get_output(
    mock_subprocess: Mock, scenario: Dict[str, Union[str, List[str]]]
) -> None:
    """Test get_output."""
    get_output(scenario["input"])
    mock_subprocess.assert_called_once_with(
        scenario["parsed"],
        shell=True,
        check=False,
        capture_output=True,
        encoding="utf-8",
    )


@pytest.mark.parametrize("scenario", RETURNCODE_DATA)
@patch("subprocess.run")
def test_get_returncode(
    mock_subprocess: Mock, scenario: Dict[str, Union[str, List[str], int]]
) -> None:
    """Test get_returncode."""
    mock_subprocess.return_value.returncode = scenario["mock"]
    output = get_returncode(scenario["input"])
    assert output == scenario["mock"]


@pytest.mark.parametrize("scenario", OUTPUT_DATA)
@patch("subprocess.run")
def test_get_standard_output(
    mock_subprocess: Mock, scenario: Dict[str, Union[str, List[str], None]]
) -> None:
    """Test get_output."""
    mock_subprocess.return_value.stdout = scenario["mock"]
    output = get_standard_output(scenario["input"])
    assert output == scenario["output"]


@pytest.mark.parametrize("scenario", OUTPUT_DATA)
@patch("subprocess.run")
def test_get_standard_output_with_lines(
    mock_subprocess: Mock, scenario: Dict[str, Union[str, List[str], None]]
) -> None:
    """Test get_output."""
    mock_subprocess.return_value.stdout = scenario["mock"]
    output = get_standard_output(scenario["input"], lines=True)
    assert output == scenario["lines"]


@pytest.mark.parametrize("scenario", RUN_COMMAND_SUCCESS_DATA)
@patch("subprocess.run")
def test_run_command_success(
    mock_subprocess: Mock, scenario: Dict[str, Union[str, List[str]]]
) -> None:
    """Test run_command successfully."""
    mock_subprocess.return_value = scenario["output"]
    output = run_command(scenario["input"])
    assert output == scenario["output"]


@pytest.mark.parametrize("scenario", RUN_COMMAND_ERROR_DATA)
def test_run_command_error(
    scenario: Dict[str, Union[str, List[str], int]],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test run_command with error."""
    side_effect = subprocess.CalledProcessError(
        returncode=scenario["return_code"],
        cmd=scenario["input"],
    )
    formatted = color_text(
        f"ERROR: Command '{scenario['input']}' returned "
        f"non-zero exit status {scenario['return_code']}.",
        "red",
    )
    formatted += "\n"
    with patch.object(subprocess, "run", side_effect=side_effect):
        with pytest.raises(SystemExit) as sys_exit:
            run_command(scenario["input"])
    sys_output, sys_error = capsys.readouterr()
    assert not sys_error
    assert sys_output == formatted
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == scenario["return_code"]
