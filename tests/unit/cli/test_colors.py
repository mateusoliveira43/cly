"""Unit tests of module scripts.cli.colors."""

from typing import Dict, List, Union
from unittest.mock import Mock, patch

import pytest

from scripts.cli.colors import (
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

FORMAT_OPTIONS_DATA = [
    {"options": [], "result": ""},
    {"options": ["one"], "result": "one"},
    {"options": ["one", "two"], "result": "one or two"},
    {"options": ["one", "two", "three"], "result": "one, two or three"},
    {"options": ["1", "2", "3", "4", "5"], "result": "1, 2, 3, 4 or 5"},
]
GET_COLOR_DATA_ERROR = ["batman", "joker", "riddler", "blue", "white"]
WORDS = ["Batman", "Bruce Wayne", "Joker", "Edward Nigma"]
GET_PRINT_LENGTH_DATA = [
    {"message": "1", "result": 1},
    {"message": "12", "result": 2},
    {"message": "123", "result": 3},
    {"message": "1234", "result": 4},
    {"message": color_text("LEGO", "red"), "result": 4},
    {"message": color_text("LEGO", "yellow"), "result": 4},
    {"message": color_text("LEGO", "green"), "result": 4},
    {"message": underline_text("LEGO"), "result": 4},
    {"message": f'{underline_text("LEGO")} batman', "result": 11},
    {
        "message": color_text(
            f'{underline_text("LEGO", "green")} is awesome!', "green"
        ),
        "result": 16,
    },
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


@pytest.mark.parametrize("scenario", FORMAT_OPTIONS_DATA)
def test_format_options(scenario: Dict[str, Union[str, List[str]]]) -> None:
    """Test format_options."""
    output = format_options(scenario["options"])
    assert output == scenario["result"]


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


@pytest.mark.parametrize("scenario", GET_PRINT_LENGTH_DATA)
def test_get_print_length(scenario: Dict[str, Union[str, int]]) -> None:
    """Test get_print_length."""
    output = get_print_length(scenario["message"])
    assert output == scenario["result"]


@pytest.mark.parametrize("scenario", PRINT_FLASHY_DATA)
@patch("scripts.cli.colors.get_print_length")
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
