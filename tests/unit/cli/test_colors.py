"""Unit tests of module scripts.cli.colors."""

from typing import Dict, List, Tuple
from unittest.mock import Mock, patch

import pytest

from cli.colors import (
    COLORS,
    DEFAULT,
    UNDERLINE,
    color_text,
    format_options,
    get_color,
    get_print_length,
    print_flashy,
    underline_text,
)

FORMAT_OPTIONS_DATA: List[Tuple[List[str], str]] = [
    # input, output
    # ([], ""),
    (["one"], "one"),
    (["one", "two"], "one or two"),
    (["one", "two", "three"], "one, two or three"),
    (["1", "2", "3", "4", "5"], "1, 2, 3, 4 or 5"),
]
GET_COLOR_DATA_ERROR = ["batman", "joker", "riddler", "blue", "white"]
WORDS = ["Batman", "Bruce Wayne", "Joker", "Edward Nigma"]
GET_PRINT_LENGTH_DATA: List[Tuple[str, int]] = [
    # input, output
    ("1", 1),
    ("12", 2),
    ("123", 3),
    ("1234", 4),
    (color_text("LEGO", "red"), 4),
    (color_text("LEGO", "yellow"), 4),
    (color_text("LEGO", "green"), 4),
    (underline_text("LEGO"), 4),
    (f'{underline_text("LEGO")} batman', 11),
    (
        color_text(f'{underline_text("LEGO", "green")} is awesome!', "green"),
        16,
    ),
]
PRINT_FLASHY_DATA = [
    {"message_length": 1, "mock": 20, "left": 8, "right": 9},
    {"message_length": 2, "mock": 20, "left": 8, "right": 8},
    {"message_length": 3, "mock": 20, "left": 7, "right": 8},
    {"message_length": 4, "mock": 20, "left": 7, "right": 7},
    {"message_length": 5, "mock": 20, "left": 6, "right": 7},
    {"message_length": 10, "mock": 20, "left": 4, "right": 4},
    {"message_length": 20, "mock": 20, "left": 0, "right": 0},
    {"message_length": 100, "mock": 20, "left": 0, "right": 0},
    {"message_length": 100, "mock": 200, "left": 49, "right": 49},
]


@pytest.mark.parametrize("scenario_input,scenario_output", FORMAT_OPTIONS_DATA)
def test_format_options(
    scenario_input: List[str], scenario_output: str
) -> None:
    """Test format_options."""
    output = format_options(scenario_input)
    assert output == scenario_output


@pytest.mark.parametrize("color", COLORS)
def test_get_color_success(color: str) -> None:
    """Test get_color with success."""
    output = get_color(color)
    assert output == COLORS[color]


@pytest.mark.parametrize("color", GET_COLOR_DATA_ERROR)
def test_get_color_error(
    color: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test get_color with error."""
    expected = (
        f'{COLORS["red"]}ERROR: {UNDERLINE}{color}{DEFAULT}{COLORS["red"]}'
        " is not a valid color. Available colors: "
        f"{format_options(list(COLORS))}.\n"
    )
    with pytest.raises(SystemExit) as sys_exit:
        get_color(color)
    output, error = capsys.readouterr()
    assert output == expected
    assert not error
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 1


@pytest.mark.parametrize("word", WORDS)
def test_underline_text(word: str) -> None:
    """Test underline_text."""
    words = word.split()
    if len(words) > 1:
        remaining_words = " ".join(words[1:])
        output = f"{underline_text(words[0])} {remaining_words}"
        assert output == f"{UNDERLINE}{words[0]}{DEFAULT} {remaining_words}"
    output = underline_text(word)
    assert output == UNDERLINE + word + DEFAULT


@pytest.mark.parametrize("color", COLORS)
@pytest.mark.parametrize("word", WORDS)
def test_underline_text_with_color(word: str, color: str) -> None:
    """Test underline_text with color."""
    words = word.split()
    if len(words) > 1:
        remaining_words = " ".join(words[1:])
        output = f"{underline_text(words[0], color)} {remaining_words}"
        assert output == (
            f"{UNDERLINE}{words[0]}{DEFAULT}{COLORS[color]} {remaining_words}"
        )
    output = underline_text(word, color)
    assert output == UNDERLINE + word + DEFAULT + COLORS[color]


# TODO test color_text!


@pytest.mark.parametrize(
    "scenario_input,scenario_output", GET_PRINT_LENGTH_DATA
)
def test_get_print_length(scenario_input: str, scenario_output: int) -> None:
    """Test get_print_length."""
    output = get_print_length(scenario_input)
    assert output == scenario_output


@pytest.mark.parametrize("scenario", PRINT_FLASHY_DATA)
@patch("cli.colors.get_print_length")
@patch("shutil.get_terminal_size")
def test_print_flashy(
    mock_shutil: Mock,
    mock_print_length: Mock,
    scenario: Dict[str, int],
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test print_flashy."""
    mock_shutil.return_value = (scenario["mock"], 1)
    mock_print_length.return_value = scenario["message_length"]
    expected = (
        f"{'>'*scenario['left']} {'a' * scenario['message_length']} "
        f"{'<'*scenario['right']}\n"
    )
    print_flashy("a" * scenario["message_length"])
    output, error = capsys.readouterr()
    assert not error
    assert output == expected
