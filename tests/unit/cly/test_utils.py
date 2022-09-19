import subprocess
from typing import Dict, List, Optional, Tuple, Union
from unittest.mock import Mock, patch

import pytest

from cly.colors import color_text
from cly.utils import (
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
RETURNCODE_DATA: List[Tuple[Union[str, List[str]], int]] = [
    # input, returncode
    (["joker", "--help"], 0),
    ("batman --version", 127),
]
INPUT_FOR_OUTPUT_DATA: List[Tuple[Union[str, List[str]], str]] = [
    # input, mocked return
    (
        ["joker", "--help"],
        "Why\nso\nserious\n?",
    ),
    (
        "batman --version",
        "",
    ),
    (
        "dent --version",
        (
            "You either die a hero\nor you live long enough to see yourself "
            "become the villain"
        ),
    ),
]
OUTPUT_DATA: List[Tuple[Union[str, List[str]], str, Optional[List[str]]]] = [
    # input, mocked return, output
    (
        *INPUT_FOR_OUTPUT_DATA[0],
        ["Why", "so", "serious", "?"],
    ),
    (
        *INPUT_FOR_OUTPUT_DATA[1],
        None,
    ),
    (
        *INPUT_FOR_OUTPUT_DATA[2],
        [
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
    ),
]
OUTPUT_DATA_LINES: List[
    Tuple[
        Union[str, List[str]],
        str,
        Optional[List[str]],
    ]
] = [
    # input, mocked return, output
    (
        *INPUT_FOR_OUTPUT_DATA[0],
        ["Why", "so", "serious", "?"],
    ),
    (
        *INPUT_FOR_OUTPUT_DATA[1],
        None,
    ),
    (
        *INPUT_FOR_OUTPUT_DATA[2],
        [
            "You either die a hero",
            "or you live long enough to see yourself become the villain",
        ],
    ),
]
# RUN_COMMAND_SUCCESS_DATA = [
#     {
#         "input": ["joker", "--help"],
#         "output": "Why\nso\nserious\n?\n",
#     },
#     {"input": "batman --version", "output": "Batman 1.2.3\n"},
# ]
RUN_COMMAND_ERROR_DATA: List[Tuple[Union[str, List[str]], int]] = [
    # input, returncode
    (["riddler", "--help"], 127),
    ("batman --version", 1),
]


@pytest.mark.parametrize("scenario", PARSE_ARGUMENTS_DATA)
def test_parse_arguments(scenario: Dict[str, Union[str, List[str]]]) -> None:
    output = parse_arguments(scenario["input"])
    assert output == scenario["output"]


@pytest.mark.parametrize("scenario", GET_OUTPUT_DATA)
@patch("subprocess.run")
def test_get_output(
    mock_subprocess: Mock, scenario: Dict[str, Union[str, List[str]]]
) -> None:
    get_output(scenario["input"])
    mock_subprocess.assert_called_once_with(
        scenario["parsed"],
        shell=True,
        check=False,
        capture_output=True,
        encoding="utf-8",
        cwd=None,
    )


@pytest.mark.parametrize("scenario_input,scenario_mock", RETURNCODE_DATA)
@patch("subprocess.run")
def test_get_returncode(
    mock_subprocess: Mock,
    scenario_input: Union[str, List[str]],
    scenario_mock: int,
) -> None:
    mock_subprocess.return_value.returncode = scenario_mock
    output = get_returncode(scenario_input)
    assert output == scenario_mock


@pytest.mark.parametrize(
    "scenario_input,scenario_mock,scenario_output", OUTPUT_DATA
)
@patch("subprocess.run")
def test_get_standard_output(
    mock_subprocess: Mock,
    scenario_input: Union[str, List[str]],
    scenario_mock: str,
    scenario_output: Optional[List[str]],
) -> None:
    mock_subprocess.return_value.stdout = scenario_mock
    output = get_standard_output(scenario_input)
    assert output == scenario_output


@pytest.mark.parametrize(
    "scenario_input,scenario_mock,scenario_output", OUTPUT_DATA_LINES
)
@patch("subprocess.run")
def test_get_standard_output_with_lines(
    mock_subprocess: Mock,
    scenario_input: Union[str, List[str]],
    scenario_mock: str,
    scenario_output: Optional[List[str]],
) -> None:
    mock_subprocess.return_value.stdout = scenario_mock
    output = get_standard_output(scenario_input, lines=True)
    assert output == scenario_output


# @pytest.mark.parametrize("scenario", RUN_COMMAND_SUCCESS_DATA)
# @patch("subprocess.run")
# def test_run_command_success(
#     mock_subprocess: Mock, scenario: Dict[str, Union[str, List[str]]]
# ) -> None:
#     """Test run_command successfully."""
#     mock_subprocess.return_value = scenario["output"]
#     output = run_command(scenario["input"])
#     assert output == scenario["output"]


@pytest.mark.parametrize(
    "scenario_input,scenario_returncode", RUN_COMMAND_ERROR_DATA
)
def test_run_command_error(
    scenario_input: Union[str, List[str]],
    scenario_returncode: int,
    capsys: pytest.CaptureFixture[str],
) -> None:
    side_effect = subprocess.CalledProcessError(
        returncode=scenario_returncode,
        cmd=scenario_input,
    )
    formatted = color_text(
        f"ERROR: Command '{scenario_input}' returned "
        f"non-zero exit status {scenario_returncode}.",
        "red",
    )
    formatted += "\n"
    with patch.object(subprocess, "run", side_effect=side_effect):
        with pytest.raises(SystemExit) as sys_exit:
            run_command(scenario_input)
    sys_output, sys_error = capsys.readouterr()
    assert not sys_error
    assert sys_output == formatted
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == scenario_returncode
