"""Integration tests of module scripts.cli.utils."""

import math
from unittest.mock import patch

import pytest

from scripts.cli.utils import (
    COLORS,
    DEFAULT,
    UNDERLINE,
    color_text,
    print_flashy,
    underline_text,
)

WORD_DATA = [
    {"message": "1", "mock": 20, "left": 8, "right": 9},
    {"message": "12", "mock": 20, "left": 8, "right": 8},
    {"message": "123", "mock": 20, "left": 7, "right": 8},
    {"message": "1234", "mock": 20, "left": 7, "right": 7},
]
TWO_WORD_DATA = [
    {"message": "1234 5678", "mock": 20, "left": 4, "right": 5},
]
PRINT_FLASHY_DATA = WORD_DATA + TWO_WORD_DATA

PRINT_FLASHY_COLOR_DATA = [
    # TODO automatizar
    # {
    #     'message': color_text(
    #         f'{underline_text("LEGO", "green")} is awesome!', 'green'
    #     ),
    #     'mock': 20, 'left': 1, 'right': 1
    # },
    # {
    #     'message': f'Optional {underline_text("flag")} called.',
    #     'mock': 80, 'left': 28, 'right': 29
    # },
    # {
    #     'message': color_text(
    #         f'Optional {underline_text("flag")} called.', 'green'
    #     ),
    #     'mock': 80, 'left': 28, 'right': 29
    # },
    # {
    #     'message': color_text(
    #         f'Optional {underline_text("flag")} called.', 'red'
    #     ),
    #     'mock': 80, 'left': 28, 'right': 29
    # },
    # {
    #     'message': color_text(
    #         f'Optional {underline_text("flag")} called.', 'yellow'
    #     ),
    #     'mock': 80, 'left': 28, 'right': 29
    # },
    # {
    #     'message': color_text(
    #         f'Optional {underline_text("flag", "green")} called.', 'green'
    #     ),
    #     'mock': 80, 'left': 28, 'right': 29
    # },
]


@pytest.mark.parametrize("scenario", PRINT_FLASHY_DATA)
@patch("shutil.get_terminal_size")
def test_print_flashy(mock_shutil, scenario, capsys):
    """Test print_flashy."""
    mock_shutil.return_value = (scenario["mock"], 1)
    expected = (
        f"{'>'*scenario['left']} {scenario['message']} "
        f"{'<'*scenario['right']}\n"
    )
    print_flashy(scenario["message"])
    output, error = capsys.readouterr()
    assert not error
    assert output == expected


@pytest.mark.parametrize("color", COLORS)
@pytest.mark.parametrize("scenario", PRINT_FLASHY_DATA)
@patch("shutil.get_terminal_size")
def test_print_flashy_with_color(mock_shutil, scenario, color, capsys):
    """Test print_flashy with colors."""
    mock_shutil.return_value = (scenario["mock"], 1)
    expected = (
        f"{'>'*scenario['left']} {color_text(scenario['message'], color)} "
        f"{'<'*scenario['right']}\n"
    )
    print_flashy(color_text(scenario["message"], color))
    output, error = capsys.readouterr()
    assert not error
    assert output == expected


@pytest.mark.parametrize("scenario", PRINT_FLASHY_DATA)
@patch("shutil.get_terminal_size")
def test_print_flashy_with_underline(mock_shutil, scenario, capsys):
    """Test print_flashy with underline."""
    mock_shutil.return_value = (scenario["mock"], 1)
    expected = (
        f"{'>'*scenario['left']} {UNDERLINE}{scenario['message']}{DEFAULT} "
        f"{'<'*scenario['right']}\n"
    )
    print_flashy(underline_text(scenario["message"]))
    output, error = capsys.readouterr()
    assert not error
    assert output == expected


@patch("shutil.get_terminal_size")
def test_print_flashy_with_all_colors(mock_shutil, capsys):
    """Test print_flashy with all colors."""
    mock_shutil_width = 40
    mock_shutil.return_value = (mock_shutil_width, 1)
    message = "".join([color_text("a", color) for color in COLORS])
    message_width = len(COLORS) + 2
    left = math.floor((mock_shutil_width - message_width) / 2)
    right = mock_shutil_width - left - message_width
    expected = f"{'>'*left} {message} {'<'*right}\n"
    print_flashy(message)
    output, error = capsys.readouterr()
    assert not error
    assert output == expected
