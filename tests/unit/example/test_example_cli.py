"""Unit tests of module scripts.example.example_cli."""

import sys
from unittest.mock import patch

import pytest

from scripts.example.example_cli import COMMANDS, main
from tests import ABSOLUTE_PATH

EXAMPLE_FILE = (ABSOLUTE_PATH / 'run_example.py').as_posix()
HELP_FLAGS = ['-h', '--help']
ARGUMENTS = {
    'optional': ['-o', '--optional'],
}
INVALID_FLAGS = ['-k', '--invalid']

USAGE = f'Usage:\n  [python|python3] {EXAMPLE_FILE} '
OPTIONS = '[-h] [-v] [-o] [COMMAND] ...'
OPTIONS_COMMAND = ' [-h] (-t str | -n int) ...'

UNRECOGNIZED_ARGUMENTS = 'error: unrecognized arguments'
INVALID_CHOICE = 'invalid choice'
INVALID_INT_VALUE = 'invalid int value'

INVALID_COMMANDS = ['riddler', 'joker']
TEXT_OPTION_TEST_DATA = ['1', 'batman', 'nightwing']
NUMBER_OPTION_TEST_DATA = ['1', '37', '-4']
ARGUMENTS_OPTION_TEST_DATA = [['1.9'], ['-0.7'], ['batman', 'joker', 'robin']]
INVALID_NUMBER_OPTION_TEST_DATA = ['1.9', 'joker', '-0.7', '1,7']
INVALID_ARGUMENTS_OPTION_TEST_DATA = [['-k'], ['-v'], ['-batman', 'joker']]


@pytest.mark.parametrize('text_input', TEXT_OPTION_TEST_DATA)
@pytest.mark.parametrize('command', COMMANDS)
@patch('scripts.example.example_cli.COMMANDS')
def test_main_commands_with_option_text(
    commands_mock, command, text_input, capsys
):
    """Test main commands with option text."""
    sys_mock = ['file_name', command, '-t', text_input]
    with patch.object(sys, 'argv', sys_mock):
        main()
    output, error = capsys.readouterr()
    assert not output
    assert not error
    commands_mock.get(command).assert_called_once_with(
        optional=False,
        command=command,
        text=text_input,
        number=None,
        arguments=[],
    )
    commands_mock.reset_mock()


@pytest.mark.parametrize('number_input', NUMBER_OPTION_TEST_DATA)
@pytest.mark.parametrize('command', COMMANDS)
@patch('scripts.example.example_cli.COMMANDS')
def test_main_commands_with_option_number(
    commands_mock, command, number_input, capsys
):
    """Test main commands with option number."""
    sys_mock = ['file_name', command, '-n', number_input]
    with patch.object(sys, 'argv', sys_mock):
        main()
    output, error = capsys.readouterr()
    assert not output
    assert not error
    commands_mock.get(command).assert_called_once_with(
        optional=False,
        command=command,
        text=None,
        number=int(number_input),
        arguments=[],
    )
    commands_mock.reset_mock()


@pytest.mark.parametrize('args', ARGUMENTS_OPTION_TEST_DATA)
@pytest.mark.parametrize('command', COMMANDS)
@patch('scripts.example.example_cli.COMMANDS')
def test_main_commands_with_option_arguments(
    commands_mock, command, args, capsys
):
    """Test main commands with option arguments."""
    sys_mock = ['file_name', command, '-t', 'text_input', *args]
    with patch.object(sys, 'argv', sys_mock):
        main()
    output, error = capsys.readouterr()
    assert not output
    assert not error
    commands_mock.get(command).assert_called_once_with(
        optional=False,
        command=command,
        text='text_input',
        number=None,
        arguments=args,
    )
    commands_mock.reset_mock()
