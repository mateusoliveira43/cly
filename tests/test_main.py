import argparse
from unittest.mock import patch

import pytest
from scripts.__main__ import commands, initialize_parser, main

TEXT_OPTION_TEST_DATA = ['1', 'batman', 'nightwing']
NUMBER_OPTION_TEST_DATA = ['1', '37', '-4']
INVALID_NUMBER_OPTION_TEST_DATA = ['1.9', 'joker', '-0.7', '1,7']
ARGUMENTS_OPTION_TEST_DATA = [['1.9'], ['-0.7'], ['batman', 'joker', 'robin']]
INVALID_ARGUMENTS_OPTION_TEST_DATA = [['-k'], ['-v'], ['-batman', 'joker']]
INVALID_COMMANDS = ['riddler', 'joker']


def test_initialize_parser_without_options():
    """Test initialize_parser without options."""
    args = initialize_parser([])
    assert args == argparse.Namespace(command=None, optional=None)


def test_initialize_parser_with_option_help(capsys):
    """Test initialize_parser with option help."""
    for option in ['-h', '--help']:
        with pytest.raises(SystemExit) as sys_exit:
            initialize_parser([option])
        output, error = capsys.readouterr()
        assert not error
        assert 'Usage:\n  [python|python3]' in output
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 0


def test_initialize_parser_with_option_version(capsys):
    """Test initialize_parser with option version."""
    for option in ['-v', '--version']:
        with pytest.raises(SystemExit) as sys_exit:
            initialize_parser([option])
        output, error = capsys.readouterr()
        assert not error
        assert output == 'Script name version 1.0.0\n'
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 0


def test_initialize_parser_with_option_optional():
    """Test initialize_parser with option optional."""
    for option in ['-o', '--optional']:
        args = initialize_parser([option])
        assert args.optional == 'optional'


def test_initialize_parser_with_invalid_options(capsys):
    """Test initialize_parser with invalid options."""
    for option in ['-k', '--invalid']:
        with pytest.raises(SystemExit) as sys_exit:
            initialize_parser([option])
        output, error = capsys.readouterr()
        assert 'error: unrecognized arguments' in error
        assert not output
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 2


def test_initialize_parser_invalid_commands(capsys):
    """Test initialize_parser invalid commands."""
    for command in INVALID_COMMANDS:
        with pytest.raises(SystemExit) as sys_exit:
            initialize_parser([command])
        output, error = capsys.readouterr()
        assert 'invalid choice' in error
        assert not output
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 2


def test_initialize_parser_commands_without_options(capsys):
    """Test initialize_parser commands without options."""
    for command in commands:
        with pytest.raises(SystemExit) as sys_exit:
            initialize_parser([command])
        output, error = capsys.readouterr()
        assert not output
        assert 'one of the arguments' in error
        assert 'is required' in error
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 2


def test_initialize_parser_commands_with_option_help(capsys):
    """Test initialize_parser commands with option help."""
    for command in commands:
        for option in ['-h', '--help']:
            with pytest.raises(SystemExit) as sys_exit:
                initialize_parser([command, option])
            output, error = capsys.readouterr()
            assert not error
            assert 'Usage:\n  [python|python3]' in output
            assert sys_exit.type == SystemExit
            assert sys_exit.value.code == 0


def test_initialize_parser_commands_with_option_text():
    """Test initialize_parser commands with option text."""
    for command in commands:
        for text_input in TEXT_OPTION_TEST_DATA:
            args = initialize_parser([command, '-t', text_input])
            assert args.command == command
            assert args.text == text_input


def test_initialize_parser_commands_with_option_number():
    """Test initialize_parser commands with option number."""
    for command in commands:
        for number_input in NUMBER_OPTION_TEST_DATA:
            args = initialize_parser([command, '-n', number_input])
            assert args.command == command
            assert args.number == int(number_input)


def test_initialize_parser_commands_with_option_arguments():
    """Test initialize_parser commands with option arguments."""
    for command in commands:
        for arguments in ARGUMENTS_OPTION_TEST_DATA:
            args = initialize_parser([command, '-t', 'text_input', *arguments])
            assert args.command == command
            assert args.arguments == arguments


def test_initialize_parser_commands_with_invalid_option_number(capsys):
    """Test initialize_parser commands with invalid option number."""
    for command in commands:
        for number_input in INVALID_NUMBER_OPTION_TEST_DATA:
            with pytest.raises(SystemExit) as sys_exit:
                initialize_parser([command, '-n', number_input])
            output, error = capsys.readouterr()
            assert not output
            assert 'invalid int value' in error
            assert sys_exit.type == SystemExit
            assert sys_exit.value.code == 2


def test_initialize_parser_commands_with_invalid_option_arguments(capsys):
    """Test initialize_parser commands with invalid option arguments."""
    for command in commands:
        for args in INVALID_ARGUMENTS_OPTION_TEST_DATA:
            with pytest.raises(SystemExit) as sys_exit:
                initialize_parser(
                    [command, '-t', 'text_input', *args]
                )
            output, error = capsys.readouterr()
            assert not output
            assert 'unrecognized arguments' in error
            assert sys_exit.type == SystemExit
            assert sys_exit.value.code == 2


@patch('scripts.__main__.sys')
def test_main_without_options(sys_mock, capsys):
    """Test main without options."""
    sys_mock.argv = ['file_name']
    with pytest.raises(SystemExit) as sys_exit:
        main()
    output, error = capsys.readouterr()
    assert not error
    assert 'Usage:\n  [python|python3]' in output
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


@patch('scripts.__main__.sys')
def test_main_with_option_help(sys_mock, capsys):
    """Test main with option help."""
    for option in ['-h', '--help']:
        sys_mock.argv = ['file_name', option]
        with pytest.raises(SystemExit) as sys_exit:
            main()
        output, error = capsys.readouterr()
        assert not error
        assert 'Usage:\n  [python|python3]' in output
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 0


@patch('scripts.__main__.sys')
def test_main_with_option_version(sys_mock, capsys):
    """Test main with option version."""
    for option in ['-v', '--version']:
        sys_mock.argv = ['file_name', option]
        with pytest.raises(SystemExit) as sys_exit:
            main()
        output, error = capsys.readouterr()
        assert not error
        assert output == 'Script name version 1.0.0\n'
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 0


@patch('scripts.__main__.sys')
def test_main_with_option_optional(sys_mock, capsys):
    """Test main with option optional."""
    sys_mock.argv = ['file_name', '-o']
    main()
    output, error = capsys.readouterr()
    assert not error
    assert 'Usage:\n  [python|python3]' not in output
    assert 'Optional flag called.' in output


@patch('scripts.__main__.sys')
def test_main_with_invalid_options(sys_mock, capsys):
    """Test main with invalid options."""
    for option in ['-k', '--invalid']:
        sys_mock.argv = ['file_name', option]
        with pytest.raises(SystemExit) as sys_exit:
            main()
        output, error = capsys.readouterr()
        assert 'error: unrecognized arguments' in error
        assert not output
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 2


@patch('scripts.__main__.sys')
def test_main_invalid_commands(sys_mock, capsys):
    """Test main invalid commands."""
    for command in INVALID_COMMANDS:
        sys_mock.argv = ['file_name', command]
        with pytest.raises(SystemExit) as sys_exit:
            main()
        output, error = capsys.readouterr()
        assert 'invalid choice' in error
        assert not output
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 2


@patch('scripts.__main__.sys')
def test_main_commands_without_options(sys_mock, capsys):
    """Test main commands without options."""
    for command in commands:
        sys_mock.argv = ['file_name', command]
        with pytest.raises(SystemExit) as sys_exit:
            main()
        output, error = capsys.readouterr()
        assert not output
        assert 'one of the arguments' in error
        assert 'is required' in error
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 2


@patch('scripts.__main__.sys')
def test_main_commands_with_option_help(sys_mock, capsys):
    """Test main commands with option help."""
    for command in commands:
        for option in ['-h', '--help']:
            sys_mock.argv = ['file_name', command, option]
            with pytest.raises(SystemExit) as sys_exit:
                main()
            output, error = capsys.readouterr()
            assert not error
            assert 'Usage:\n  [python|python3]' in output
            assert sys_exit.type == SystemExit
            assert sys_exit.value.code == 0


@patch('scripts.__main__.commands')
@patch('scripts.__main__.sys')
def test_main_commands_with_option_text(sys_mock, commands_mock, capsys):
    """Test main commands with option text."""
    for command in commands:
        for text_input in TEXT_OPTION_TEST_DATA:
            sys_mock.argv = ['file_name', command, '-t', text_input]
            main()
            _, error = capsys.readouterr()
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
@patch('scripts.__main__.sys')
def test_main_commands_with_option_number(sys_mock, commands_mock, capsys):
    """Test main commands with option number."""
    for command in commands:
        for number_input in NUMBER_OPTION_TEST_DATA:
            sys_mock.argv = ['file_name', command, '-n', number_input]
            main()
            _, error = capsys.readouterr()
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
@patch('scripts.__main__.sys')
def test_main_commands_with_option_arguments(sys_mock, commands_mock, capsys):
    """Test main commands with option arguments."""
    for command in commands:
        for args in ARGUMENTS_OPTION_TEST_DATA:
            sys_mock.argv = ['file_name', command, '-t', 'text_input', *args]
            main()
            _, error = capsys.readouterr()
            assert not error
            commands_mock.get(command).get('command').assert_called_once_with(
                optional=None,
                command=command,
                text='text_input',
                number=None,
                arguments=args,
            )
            commands_mock.reset_mock()


@patch('scripts.__main__.sys')
def test_main_commands_with_invalid_option_number(sys_mock, capsys):
    """Test main commands with invalid option number."""
    for command in commands:
        for number_input in INVALID_NUMBER_OPTION_TEST_DATA:
            sys_mock.argv = ['file_name', command, '-n', number_input]
            with pytest.raises(SystemExit) as sys_exit:
                main()
            output, error = capsys.readouterr()
            assert not output
            assert 'invalid int value' in error
            assert sys_exit.type == SystemExit
            assert sys_exit.value.code == 2


@patch('scripts.__main__.sys')
def test_main_commands_with_invalid_option_arguments(sys_mock, capsys):
    """Test main commands with invalid option arguments."""
    for command in commands:
        for args in INVALID_ARGUMENTS_OPTION_TEST_DATA:
            sys_mock.argv = ['file_name', command, '-t', 'text_input', *args]
            with pytest.raises(SystemExit) as sys_exit:
                main()
            output, error = capsys.readouterr()
            assert not output
            assert 'unrecognized arguments' in error
            assert sys_exit.type == SystemExit
            assert sys_exit.value.code == 2
