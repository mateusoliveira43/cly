import sys
from runpy import run_module
from unittest.mock import patch

import pytest
from scripts.cli import commands, main

HELP_FLAGS = ['-h', '--help']
VERSION_FLAGS = ['-v', '--version']
OPTIONAL_FLAGS = ['-o', '--optional']
INVALID_FLAGS = ['-k', '--invalid']

USAGE = 'Usage:\n  [python|python3] file_name '
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


def test_main_without_options(capsys):
    """Test main without options."""
    sys_mock = ['file_name']
    with patch.object(sys, 'argv', sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_module('scripts.__main__', run_name='__main__')
    output, error = capsys.readouterr()
    assert not error
    assert USAGE + OPTIONS in output
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


@pytest.mark.parametrize('option', HELP_FLAGS)
def test_main_with_option_help(option, capsys):
    """Test main with option help."""
    sys_mock = ['file_name', option]
    with patch.object(sys, 'argv', sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_module('scripts.__main__', run_name='__main__')
    output, error = capsys.readouterr()
    assert not error
    assert USAGE + OPTIONS in output
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


@pytest.mark.parametrize('option', VERSION_FLAGS)
def test_main_with_option_version(option, capsys):
    """Test main with option version."""
    sys_mock = ['file_name', option]
    with patch.object(sys, 'argv', sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_module('scripts.__main__', run_name='__main__')
    output, error = capsys.readouterr()
    assert not error
    assert output == 'Script name version 1.0.0\n'
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


@pytest.mark.parametrize('option', OPTIONAL_FLAGS)
def test_main_with_option_optional(option, capsys):
    """Test main with option optional."""
    sys_mock = ['file_name', option]
    with patch.object(sys, 'argv', sys_mock):
        run_module('scripts.__main__', run_name='__main__')
    output, error = capsys.readouterr()
    assert not error
    assert USAGE + OPTIONS not in output
    assert 'Optional flag called.' in output


@pytest.mark.parametrize('option', INVALID_FLAGS)
def test_main_with_invalid_options(option, capsys):
    """Test main with invalid options."""
    sys_mock = ['file_name', option]
    with patch.object(sys, 'argv', sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_module('scripts.__main__', run_name='__main__')
    output, error = capsys.readouterr()
    assert UNRECOGNIZED_ARGUMENTS in error
    assert not output
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 2


@pytest.mark.parametrize('command', INVALID_COMMANDS)
def test_main_invalid_commands(command, capsys):
    """Test main invalid commands."""
    sys_mock = ['file_name', command]
    with patch.object(sys, 'argv', sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_module('scripts.__main__', run_name='__main__')
    output, error = capsys.readouterr()
    assert INVALID_CHOICE in error
    assert not output
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 2


@pytest.mark.parametrize('command', commands)
def test_main_commands_without_options(command, capsys):
    """Test main commands without options."""
    sys_mock = ['file_name', command]
    with patch.object(sys, 'argv', sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_module('scripts.__main__', run_name='__main__')
    output, error = capsys.readouterr()
    assert not output
    assert 'one of the arguments' in error
    assert 'is required' in error
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 2


@pytest.mark.parametrize('option', HELP_FLAGS)
@pytest.mark.parametrize('command', commands)
def test_main_commands_with_option_help(command, option, capsys):
    """Test main commands with option help."""
    sys_mock = ['file_name', command, option]
    with patch.object(sys, 'argv', sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_module('scripts.__main__', run_name='__main__')
    output, error = capsys.readouterr()
    assert not error
    assert USAGE + command + OPTIONS_COMMAND in output
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


@pytest.mark.parametrize('text_input', TEXT_OPTION_TEST_DATA)
@pytest.mark.parametrize('command', commands)
@patch('scripts.cli.commands')
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
    commands_mock.get(command).get('command').assert_called_once_with(
        optional=None,
        command=command,
        text=text_input,
        number=None,
        arguments=[],
    )
    commands_mock.reset_mock()


@pytest.mark.parametrize('number_input', NUMBER_OPTION_TEST_DATA)
@pytest.mark.parametrize('command', commands)
@patch('scripts.cli.commands')
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
    commands_mock.get(command).get('command').assert_called_once_with(
        optional=None,
        command=command,
        text=None,
        number=int(number_input),
        arguments=[],
    )
    commands_mock.reset_mock()


@pytest.mark.parametrize('args', ARGUMENTS_OPTION_TEST_DATA)
@pytest.mark.parametrize('command', commands)
@patch('scripts.cli.commands')
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
    commands_mock.get(command).get('command').assert_called_once_with(
        optional=None,
        command=command,
        text='text_input',
        number=None,
        arguments=args,
    )
    commands_mock.reset_mock()


@pytest.mark.parametrize('number_input', INVALID_NUMBER_OPTION_TEST_DATA)
@pytest.mark.parametrize('command', commands)
def test_main_commands_with_invalid_option_number(
    command, number_input, capsys
):
    """Test main commands with invalid option number."""
    sys_mock = ['file_name', command, '-n', number_input]
    with patch.object(sys, 'argv', sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_module('scripts.__main__', run_name='__main__')
    output, error = capsys.readouterr()
    assert not output
    assert INVALID_INT_VALUE in error
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 2


@pytest.mark.parametrize('args', INVALID_ARGUMENTS_OPTION_TEST_DATA)
@pytest.mark.parametrize('command', commands)
def test_main_commands_with_invalid_option_arguments(command, args, capsys):
    """Test main commands with invalid option arguments."""
    sys_mock = ['file_name', command, '-t', 'text_input', *args]
    with patch.object(sys, 'argv', sys_mock):
        with pytest.raises(SystemExit) as sys_exit:
            run_module('scripts.__main__', run_name='__main__')
    output, error = capsys.readouterr()
    assert not output
    assert UNRECOGNIZED_ARGUMENTS in error
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 2
