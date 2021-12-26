"""Unit tests of module scripts.cli.utils."""

import subprocess
from unittest.mock import patch

import pytest
from scripts.cli.utils import (
    COLORS, DEFAULT, UNDERLINE, color_text, format_options, get_color,
    get_output, get_print_length, get_returncode, get_standard_output,
    parse_arguments, print_flashy, run_command, underline_text
)

FORMAT_OPTIONS_DATA = [
    {'options': [], 'result': ''},
    {'options': ['one'], 'result': 'one'},
    {'options': ['one', 'two'], 'result': 'one or two'},
    {'options': ['one', 'two', 'three'], 'result': 'one, two or three'},
    {'options': ['1', '2', '3', '4', '5'], 'result': '1, 2, 3, 4 or 5'},
]
GET_COLOR_DATA_ERROR = ['batman', 'joker', 'riddler', 'blue', 'white']
GET_PRINT_LENGTH_DATA = [
    {'message': '1', 'result': 1},
    {'message': '12', 'result': 2},
    {'message': '123', 'result': 3},
    {'message': '1234', 'result': 4},
    {'message': color_text('LEGO', 'red'), 'result': 4},
    {'message': color_text('LEGO', 'yellow'), 'result': 4},
    {'message': color_text('LEGO', 'green'), 'result': 4},
    {'message': underline_text('LEGO'), 'result': 4},
    {'message': f'{underline_text("LEGO")} batman', 'result': 11},
    {'message': color_text(
        f'{underline_text("LEGO", "green")} is awesome!', 'green'
    ), 'result': 16},
]
PRINT_FLASHY_DATA = [
    {'message_length': 1, 'mock': 20, 'left': 8, 'right': 9},
    {'message_length': 2, 'mock': 20, 'left': 8, 'right': 8},
    {'message_length': 3, 'mock': 20, 'left': 7, 'right': 8},
    {'message_length': 4, 'mock': 20, 'left': 7, 'right': 7},
    {'message_length': 5, 'mock': 20, 'left': 6, 'right': 7},
    {'message_length': 10, 'mock': 20, 'left': 4, 'right': 4},
    {'message_length': 20, 'mock': 20, 'left': 0, 'right': 0},
    {'message_length': 100, 'mock': 20, 'left': 0, 'right': 0},
    {'message_length': 100, 'mock': 200, 'left': 49, 'right': 49},
]
PARSE_ARGUMENTS_DATA = [
    {'input': ['the', 'dark', 'knight'], 'output': 'the dark knight'},
    {'input': ['-r', 'command', '-v', '1'], 'output': '-r command -v 1'},
    {'input': 'grep -Inr "batman" .', 'output': 'grep -Inr "batman" .'},
]
GET_OUTPUT_DATA = [
    {'input': ['joker', '--help'], 'parsed': 'joker --help'},
    {'input': 'batman --version', 'parsed': 'batman --version'},
]
RETURNCODE_DATA = [
    {'input': ['joker', '--help'], 'mock': 0},
    {'input': 'batman --version', 'mock': 127},
]
OUTPUT_DATA = [
    {
        'input': ['joker', '--help'],
        'mock': 'Why\nso\nserious\n?',
        'output': ['Why', 'so', 'serious', '?'],
        'lines': ['Why', 'so', 'serious', '?'],
    },
    {
        'input': 'dent --version',
        'mock': (
            'You either die a hero\nor you live long enough to see yourself '
            'become the villain'
        ),
        'output': [
            'You', 'either', 'die', 'a', 'hero', 'or', 'you', 'live', 'long',
            'enough', 'to', 'see', 'yourself', 'become', 'the', 'villain',
        ],
        'lines': [
            'You either die a hero',
            'or you live long enough to see yourself become the villain',
        ],
    },
    {
        'input': 'batman --version',
        'mock': '',
        'output': None,
        'lines': None,
    },
]
RUN_COMMAND_SUCCESS_DATA = [
    {
        'input': ['joker', '--help'],
        'output': 'Why\nso\nserious\n?\n',
    },
    {
        'input': 'batman --version',
        'output': 'Batman 1.2.3\n'
    },
]
RUN_COMMAND_ERROR_DATA = [
    {'input': ['riddler', '--help'], 'return_code': 127},
    {'input': 'batman --version', 'return_code': 1},
]


@pytest.mark.parametrize('scenario', FORMAT_OPTIONS_DATA)
def test_format_options(scenario):
    """Test format_options."""
    output = format_options(scenario['options'])
    assert output == scenario['result']


@pytest.mark.parametrize('color', COLORS.keys())
def test_get_color_success(color):
    """Test get_color with success."""
    output = get_color(color)
    assert output == COLORS[color]


@pytest.mark.parametrize('color', GET_COLOR_DATA_ERROR)
def test_get_color_error(color, capsys):
    """Test get_color with error."""
    expected = (
        f'{COLORS["red"]}ERROR: {UNDERLINE}{color}{DEFAULT}{COLORS["red"]}'
        ' is not a valid color. Available colors: '
        f'{format_options(list(COLORS.keys()))}.\n'
    )
    with pytest.raises(SystemExit) as sys_exit:
        get_color(color)
    output, error = capsys.readouterr()
    assert output == expected
    assert not error
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 1

# TODO test underline_text

# TODO test color_text


@pytest.mark.parametrize('scenario', GET_PRINT_LENGTH_DATA)
def test_get_print_length(scenario):
    """Test get_print_length."""
    output = get_print_length(scenario['message'])
    assert output == scenario['result']


@pytest.mark.parametrize('scenario', PRINT_FLASHY_DATA)
@patch('scripts.cli.utils.get_print_length')
@patch('shutil.get_terminal_size')
# TODO add test for new scenarios
def test_print_flashy(mock_shutil, mock_print_length, scenario, capsys):
    """Test print_flashy."""
    mock_shutil.return_value = (scenario['mock'], 1)
    mock_print_length.return_value = scenario['message_length']
    # TODO better structure this test
    expected = (
        f"{'>'*scenario['left']} {'a' * scenario['message_length']} "
        f"{'<'*scenario['right']}\n"
    )
    print_flashy('a' * scenario['message_length'])
    output, error = capsys.readouterr()
    assert not error
    assert output == expected


@pytest.mark.parametrize('scenario', PARSE_ARGUMENTS_DATA)
def test_parse_arguments(scenario):
    """Test parse_arguments."""
    output = parse_arguments(scenario['input'])
    assert output == scenario['output']


@pytest.mark.parametrize('scenario', GET_OUTPUT_DATA)
@patch('subprocess.run')
def test_get_output(mock_subprocess, scenario):
    """Test get_output."""
    get_output(scenario['input'])
    mock_subprocess.assert_called_once_with(
        scenario['parsed'], shell=True, check=False,
        capture_output=True, encoding='utf-8'
    )


@pytest.mark.parametrize('scenario', RETURNCODE_DATA)
@patch('subprocess.run')
def test_get_returncode(mock_subprocess, scenario):
    """Test get_returncode."""
    mock_subprocess.return_value.returncode = scenario['mock']
    output = get_returncode(scenario['input'])
    assert output == scenario['mock']


@pytest.mark.parametrize('scenario', OUTPUT_DATA)
@patch('subprocess.run')
def test_get_standard_output(mock_subprocess, scenario):
    """Test get_output."""
    mock_subprocess.return_value.stdout = scenario['mock']
    output = get_standard_output(scenario['input'])
    assert output == scenario['output']


@pytest.mark.parametrize('scenario', OUTPUT_DATA)
@patch('subprocess.run')
def test_get_standard_output_with_lines(mock_subprocess, scenario):
    """Test get_output."""
    mock_subprocess.return_value.stdout = scenario['mock']
    output = get_standard_output(scenario['input'], lines=True)
    assert output == scenario['lines']


@pytest.mark.parametrize('scenario', RUN_COMMAND_SUCCESS_DATA)
@patch('subprocess.run')
def test_run_command_success(mock_subprocess, scenario):
    """Test run_command successfully."""
    mock_subprocess.return_value = scenario['output']
    output = run_command(scenario['input'])
    assert output == scenario['output']


@pytest.mark.parametrize('scenario', RUN_COMMAND_ERROR_DATA)
@patch('subprocess.run')
# TODO add test for new scenarios
def test_run_command_error(mock_subprocess, scenario, capsys):
    """Test run_command with error."""
    mock_subprocess.side_effect = subprocess.CalledProcessError(
        returncode=scenario['return_code'],
        cmd=scenario['input'],
    )
    formatted = color_text(
        f'ERROR: Command {underline_text(scenario["input"], "red")} returned '
        f'non-zero exit status {scenario["return_code"]}.',
        'red'
    )
    formatted += '\n'
    with pytest.raises(SystemExit) as sys_exit:
        run_command(scenario['input'])
    sys_output, sys_error = capsys.readouterr()
    assert not sys_error
    assert sys_output == formatted
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == scenario['return_code']
