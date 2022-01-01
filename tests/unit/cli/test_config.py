"""Unit tests of module scripts.cli.config."""

import sys
from unittest.mock import patch

import pytest
from scripts.cli.config import initialize_parser

PARAMETER = [True, False]
SYS_MOCK = [
    {'mock': ['file_name'], True: ['--help'], False: []},
    {'mock': ['file_name', '-v'], True: ['-v'], False: ['-v']}
]


@pytest.mark.parametrize('sys_mock', SYS_MOCK)
def test_initialize_parser_without_parameter(sys_mock):
    """Test initialize_parser without options."""
    with patch.object(sys, 'argv', sys_mock['mock']):
        args = initialize_parser()
        assert args == sys_mock[True]


@pytest.mark.parametrize('sys_mock', SYS_MOCK)
@pytest.mark.parametrize('parameter', PARAMETER)
def test_initialize_parser_with_parameter(parameter, sys_mock):
    """Test initialize_parser with option help."""
    with patch.object(sys, 'argv', sys_mock['mock']):
        args = initialize_parser(parameter)
        assert args == sys_mock[parameter]
