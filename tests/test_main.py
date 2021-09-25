import pytest
from script_name.__main__ import initialize_parser, main
from unittest.mock import patch


def test_initialize_parser_with_option_help(capsys):
    for option in ['-h', '--help']:
        with pytest.raises(SystemExit) as sys_exit:
            initialize_parser([option])
        output, error = capsys.readouterr()
        assert not error
        assert 'Usage' in output
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 0


def test_initialize_parser_with_option_version(capsys):
    for option in ['-v', '--version']:
        with pytest.raises(SystemExit) as sys_exit:
            initialize_parser([option])
        output, error = capsys.readouterr()
        assert not error
        assert 'script name version 1.0.0\n' == output
        assert sys_exit.type == SystemExit
        assert sys_exit.value.code == 0


def test_initialize_parser_with_option_mateus():
    for option in ['-m', '--mateus']:
        args = initialize_parser([option])
        assert args.mateus == 'mateus'


@patch('script_name.__main__.sys')
def test_main_with_no_option(sysMock, capsys):
    sysMock.argv = []
    with pytest.raises(SystemExit) as sys_exit:
        main()
    output, error = capsys.readouterr()
    assert not error
    assert 'Usage' in output
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


@patch('script_name.__main__.sys')
def test_main_with_option_mateus(sysMock, capsys):
    sysMock.argv = ['file_name', '-m']
    main()
    output, error = capsys.readouterr()
    assert not error
    assert 'Usage' not in output
    assert 'Namespace' in output


@patch('script_name.__main__.sys')
def test_main_with_command1_without_options(sysMock, capsys):
    sysMock.argv = ['file_name', 'command1']
    with pytest.raises(SystemExit) as sys_exit:
        main()
    output, error = capsys.readouterr()
    assert not output
    assert 'arguments' in error
    assert 'is required' in error
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 2


@patch('script_name.__main__.commands')
@patch('script_name.__main__.sys')
def test_main_with_command1_with_option_verbose_1(
    sysMock, command1Mock, capsys
):
    sysMock.argv = ['file_name', 'command1', '-v', '1']
    main()
    output, error = capsys.readouterr()
    assert not error
    command1Mock.get('command1').get('command').assert_called_once_with(
        arguments=[], command='command1', example=None, ls=None,
        mateus=None, test=None, verbose=1
    )


@patch('script_name.__main__.utils.run_command')
@patch('script_name.__main__.sys')
def test_main_with_option_ls(sysMock, utilsMock, capsys):
    sysMock.argv = ['file_name', '-ls']
    main()
    output, error = capsys.readouterr()
    assert not error
    assert 'True' in output
    utilsMock.assert_called_once_with(['ls', '-1a'])
