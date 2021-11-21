import sys
from unittest.mock import patch

import pytest
from scripts.__main__ import commands, main
import tests

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
            main()
    output, error = capsys.readouterr()
    assert not error
    assert tests.USAGE in output
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


def test_main_with_option_help(capsys):
    """Test main with option help."""
    for option in tests.HELP_FLAGS:
        sys_mock = ['file_name', option]
        with patch.object(sys, 'argv', sys_mock):
            with pytest.raises(SystemExit) as sys_exit:
                main()
        output, error = capsys.readouterr()
        assert not error
        assert tests.USAGE in output
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 0


def test_main_with_option_version(capsys):
    """Test main with option version."""
    for option in tests.VERSION_FLAGS:
        sys_mock = ['file_name', option]
        with patch.object(sys, 'argv', sys_mock):
            with pytest.raises(SystemExit) as sys_exit:
                main()
        output, error = capsys.readouterr()
        assert not error
        assert output == 'Script name version 1.0.0\n'
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 0


def test_main_with_option_optional(capsys):
    """Test main with option optional."""
    for option in tests.OPTIONAL_FLAGS:
        sys_mock = ['file_name', option]
        with patch.object(sys, 'argv', sys_mock):
            main()
        output, error = capsys.readouterr()
        assert not error
        assert tests.USAGE not in output
        assert 'Optional flag called.' in output


def test_main_with_invalid_options(capsys):
    """Test main with invalid options."""
    for option in tests.INVALID_FLAGS:
        sys_mock = ['file_name', option]
        with patch.object(sys, 'argv', sys_mock):
            with pytest.raises(SystemExit) as sys_exit:
                main()
        output, error = capsys.readouterr()
        assert tests.UNRECOGNIZED_ARGUMENTS in error
        assert not output
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 2


def test_main_invalid_commands(capsys):
    """Test main invalid commands."""
    for command in INVALID_COMMANDS:
        sys_mock = ['file_name', command]
        with patch.object(sys, 'argv', sys_mock):
            with pytest.raises(SystemExit) as sys_exit:
                main()
        output, error = capsys.readouterr()
        assert tests.INVALID_CHOICE in error
        assert not output
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 2


def test_main_commands_without_options(capsys):
    """Test main commands without options."""
    for command in commands:
        sys_mock = ['file_name', command]
        with patch.object(sys, 'argv', sys_mock):
            with pytest.raises(SystemExit) as sys_exit:
                main()
        output, error = capsys.readouterr()
        assert not output
        assert 'one of the arguments' in error
        assert 'is required' in error
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 2


def test_main_commands_with_option_help(capsys):
    """Test main commands with option help."""
    for command in commands:
        for option in tests.HELP_FLAGS:
            sys_mock = ['file_name', command, option]
            with patch.object(sys, 'argv', sys_mock):
                with pytest.raises(SystemExit) as sys_exit:
                    main()
            output, error = capsys.readouterr()
            assert not error
            assert tests.USAGE in output
            assert sys_exit.type == SystemExit
            assert sys_exit.value.code == 0


@patch('scripts.__main__.commands')
def test_main_commands_with_option_text(commands_mock, capsys):
    """Test main commands with option text."""
    for command in commands:
        for text_input in TEXT_OPTION_TEST_DATA:
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


@patch('scripts.__main__.commands')
def test_main_commands_with_option_number(commands_mock, capsys):
    """Test main commands with option number."""
    for command in commands:
        for number_input in NUMBER_OPTION_TEST_DATA:
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


@patch('scripts.__main__.commands')
def test_main_commands_with_option_arguments(commands_mock, capsys):
    """Test main commands with option arguments."""
    for command in commands:
        for args in ARGUMENTS_OPTION_TEST_DATA:
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


def test_main_commands_with_invalid_option_number(capsys):
    """Test main commands with invalid option number."""
    for command in commands:
        for number_input in INVALID_NUMBER_OPTION_TEST_DATA:
            sys_mock = ['file_name', command, '-n', number_input]
            with patch.object(sys, 'argv', sys_mock):
                with pytest.raises(SystemExit) as sys_exit:
                    main()
            output, error = capsys.readouterr()
            assert not output
            assert tests.INVALID_INT_VALUE in error
            assert sys_exit.type == SystemExit
            assert sys_exit.value.code == 2


def test_main_commands_with_invalid_option_arguments(capsys):
    """Test main commands with invalid option arguments."""
    for command in commands:
        for args in INVALID_ARGUMENTS_OPTION_TEST_DATA:
            sys_mock = ['file_name', command, '-t', 'text_input', *args]
            with patch.object(sys, 'argv', sys_mock):
                with pytest.raises(SystemExit) as sys_exit:
                    main()
            output, error = capsys.readouterr()
            assert not output
            assert tests.UNRECOGNIZED_ARGUMENTS in error
            assert sys_exit.type == SystemExit
            assert sys_exit.value.code == 2
