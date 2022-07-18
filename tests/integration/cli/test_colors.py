"""Integration tests of module scripts.cli.colors."""

import math
from typing import List, Tuple
from unittest.mock import Mock, patch

import pytest

from cli.colors import (
    COLORS,
    DEFAULT,
    UNDERLINE,
    color_text,
    print_flashy,
    underline_text,
)

WORD_DATA: List[Tuple[str, int, int, int]] = [
    # input, mocked return, left, right
    ("1", 20, 8, 9),
    ("12", 20, 8, 8),
    ("123", 20, 7, 8),
    ("1234", 20, 7, 7),
]
TWO_WORD_DATA: List[Tuple[str, int, int, int]] = [
    ("1234 5678", 20, 4, 5),
]
PRINT_FLASHY_DATA = WORD_DATA + TWO_WORD_DATA

# TODO automatizar!
# PRINT_FLASHY_COLOR_DATA = [
#     {
#         'message': color_text(
#             f'{underline_text("LEGO", "green")} is awesome!', 'green'
#         ),
#         'mock': 20, 'left': 1, 'right': 1
#     },
#     {
#         'message': f'Optional {underline_text("flag")} called.',
#         'mock': 80, 'left': 28, 'right': 29
#     },
#     {
#         'message': color_text(
#             f'Optional {underline_text("flag")} called.', 'green'
#         ),
#         'mock': 80, 'left': 28, 'right': 29
#     },
#     {
#         'message': color_text(
#             f'Optional {underline_text("flag")} called.', 'red'
#         ),
#         'mock': 80, 'left': 28, 'right': 29
#     },
#     {
#         'message': color_text(
#             f'Optional {underline_text("flag")} called.', 'yellow'
#         ),
#         'mock': 80, 'left': 28, 'right': 29
#     },
#     {
#         'message': color_text(
#             f'Optional {underline_text("flag", "green")} called.', 'green'
#         ),
#         'mock': 80, 'left': 28, 'right': 29
#     },
# ]


@pytest.mark.parametrize(
    "scenario_input,scenario_mock,scenario_left,scenario_right",
    PRINT_FLASHY_DATA,
)
@patch("shutil.get_terminal_size")
def test_print_flashy(
    mock_shutil: Mock,
    scenario_input: str,
    scenario_mock: int,
    scenario_left: int,
    scenario_right: int,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test print_flashy."""
    mock_shutil.return_value = (scenario_mock, 1)
    expected = (
        f"{'>'*scenario_left} {scenario_input} " f"{'<'*scenario_right}\n"
    )
    print_flashy(scenario_input)
    output, error = capsys.readouterr()
    assert not error
    assert output == expected


@pytest.mark.parametrize("color", COLORS)
@pytest.mark.parametrize(
    "scenario_input,scenario_mock,scenario_left,scenario_right",
    PRINT_FLASHY_DATA,
)
@patch("shutil.get_terminal_size")
def test_print_flashy_with_color(
    mock_shutil: Mock,
    scenario_input: str,
    scenario_mock: int,
    scenario_left: int,
    scenario_right: int,
    color: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test print_flashy with colors."""
    mock_shutil.return_value = (scenario_mock, 1)
    expected = (
        f"{'>'*scenario_left} {color_text(scenario_input, color)} "
        f"{'<'*scenario_right}\n"
    )
    print_flashy(color_text(scenario_input, color))
    output, error = capsys.readouterr()
    assert not error
    assert output == expected


@pytest.mark.parametrize(
    "scenario_input,scenario_mock,scenario_left,scenario_right",
    PRINT_FLASHY_DATA,
)
@patch("shutil.get_terminal_size")
def test_print_flashy_with_underline(
    mock_shutil: Mock,
    scenario_input: str,
    scenario_mock: int,
    scenario_left: int,
    scenario_right: int,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Test print_flashy with underline."""
    mock_shutil.return_value = (scenario_mock, 1)
    expected = (
        f"{'>'*scenario_left} {UNDERLINE}{scenario_input}{DEFAULT} "
        f"{'<'*scenario_right}\n"
    )
    print_flashy(underline_text(scenario_input))
    output, error = capsys.readouterr()
    assert not error
    assert output == expected


@patch("shutil.get_terminal_size")
def test_print_flashy_with_all_colors(
    mock_shutil: Mock, capsys: pytest.CaptureFixture[str]
) -> None:
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
