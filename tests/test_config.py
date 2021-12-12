import argparse
from unittest.mock import patch

import pytest
from scripts.config import configured_parser, initialize_parser
import tests

OPTIONS = ' [-h] [-v]\n\n'
DESCRIPTION = 'test description.\n\n'
OPTIONS_DESCRIPTION = (
    "Options:\n  -h, --help     Show script's help message.\n"
    "  -v, --version  Show script's version.\n\n"
)
EPILOG = 'Script epilog.\n'

TEST_PARSER = configured_parser(
    'test script', 'major.minor.patch', 'test description.'
)


@patch('scripts.config.sys')
def test_initialize_parser_without_options(sys_mock, capsys):
    """Test initialize_parser without options."""
    sys_mock.argv = ['file_name']
    with pytest.raises(SystemExit) as sys_exit:
        args = initialize_parser(TEST_PARSER)
        assert args == argparse.Namespace()
    output, error = capsys.readouterr()
    assert not error
    assert tests.USAGE in output
    assert OPTIONS in output
    assert DESCRIPTION in output
    assert OPTIONS_DESCRIPTION in output
    assert EPILOG in output
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


@pytest.mark.parametrize('option', tests.HELP_FLAGS)
@patch('scripts.config.sys')
def test_initialize_parser_with_option_help(sys_mock, option, capsys):
    """Test initialize_parser with option help."""
    sys_mock.argv = ['file_name', option]
    with pytest.raises(SystemExit) as sys_exit:
        args = initialize_parser(TEST_PARSER)
        assert args == argparse.Namespace()
    output, error = capsys.readouterr()
    assert not error
    assert tests.USAGE in output
    assert OPTIONS in output
    assert DESCRIPTION in output
    assert OPTIONS_DESCRIPTION in output
    assert EPILOG in output
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


@pytest.mark.parametrize('option', tests.VERSION_FLAGS)
@patch('scripts.config.sys')
def test_initialize_parser_with_option_version(sys_mock, option, capsys):
    """Test initialize_parser with option version."""
    sys_mock.argv = ['file_name', option]
    with pytest.raises(SystemExit) as sys_exit:
        args = initialize_parser(TEST_PARSER)
        assert args == argparse.Namespace()
    output, error = capsys.readouterr()
    assert not error
    assert output == 'test script version major.minor.patch\n'
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 0


@pytest.mark.parametrize('option', tests.INVALID_FLAGS)
@patch('scripts.config.sys')
def test_initialize_parser_with_invalid_options(sys_mock, option, capsys):
    """Test initialize_parser with invalid options."""
    sys_mock.argv = ['file_name', option]
    with pytest.raises(SystemExit) as sys_exit:
        args = initialize_parser(TEST_PARSER)
        assert args == argparse.Namespace()
    output, error = capsys.readouterr()
    assert tests.UNRECOGNIZED_ARGUMENTS in error
    assert not output
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 2
