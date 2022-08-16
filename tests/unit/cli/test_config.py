from contextlib import nullcontext
from typing import Tuple
from unittest.mock import Mock, patch

import pytest

from cli.colors import color_text
from cli.config import (
    MAJOR_VERSION,
    MINOR_VERSION,
    check_python_minimum_version,
)

PARAMETER = [True, False]
SYS_MOCK = [
    {"mock": ["file_name"], True: ["--help"], False: []},
    {"mock": ["file_name", "-v"], True: ["-v"], False: ["-v"]},
]
VALID_VERSIONS = [(3, 7), (3, 8), (3, 9), (3, 10)]
INVALID_VERSIONS = [(2, 7), (3, 5), (3, 6)]


@pytest.mark.parametrize("version", VALID_VERSIONS)
@patch("sys.version_info")
def test_check_python_minimum_version_with_valid_version(
    mock_version_info: Mock,
    version: Tuple[int, int],
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_version_info.major = version[0]
    mock_version_info.minor = version[1]
    with nullcontext() as sys_exit:
        check_python_minimum_version()
    sys_output, sys_error = capsys.readouterr()
    assert not sys_error
    assert not sys_output
    assert sys_exit is None


@pytest.mark.parametrize("version", INVALID_VERSIONS)
@patch("sys.version_info")
def test_check_python_minimum_version_with_invalid_version(
    mock_version_info: Mock,
    version: Tuple[int, int],
    capsys: pytest.CaptureFixture[str],
) -> None:
    mock_version_info.major = version[0]
    mock_version_info.minor = version[1]
    with pytest.raises(SystemExit) as sys_exit:
        check_python_minimum_version()
    sys_output, sys_error = capsys.readouterr()
    assert not sys_error
    assert sys_output == (
        color_text(
            f"ERROR: Python version {version[0]}.{version[1]} does not meet "
            f"minimum requirement of {MAJOR_VERSION}.{MINOR_VERSION}.",
            "red",
        )
        + "\n"
    )
    assert sys_exit.type == SystemExit
    assert sys_exit.value.code == 1
