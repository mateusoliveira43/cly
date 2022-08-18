from typing import Optional

import pytest

from cly.docstring import (
    get_help_from_docstring,
    get_param_help_from_docstring,
)


# pylint: disable=unused-argument
def function_to_test_docstring(
    param1: str, param2: int, param3: Optional[str] = None
) -> str:
    """Just for tests."""


PARAMS = {
    "param1": "A very detailed description.",
    "param2": "A small one.",
    "param3": "A description with default value.",
}
DOCSTRINGS = {
    "NUMPY": """
    Function to test docstring styles.

    Parameters
    ----------
    param1 : str
        A very detailed description.
    param2 : int
        A small one
    param3 : Optional[str], optional
        A description with default value, by default None

    Returns
    -------
    str
        Return information.

    """,
    "GOOGLE": """
    Function to test docstring styles.

    Args:
        param1 (str): A very detailed description.
        param2 (int): A small one
        param3 (Optional[str], optional): A description with default value.
            Defaults to None.

    Returns:
        str: Return information.

    """,
    "SPHINX": """
    Function to test docstring styles.

    :param param1: A very detailed description.
    :type param1: str
    :param param2: A small one
    :type param2: int
    :param param3: A description with default value, defaults to None
    :type param3: Optional[str], optional
    :return: Return information.
    :rtype: str

    """,
}


@pytest.mark.parametrize("style", DOCSTRINGS)
def test_get_help_from_docstring(style: str) -> None:
    function_to_test_docstring.__doc__ = DOCSTRINGS[style]
    assert (
        get_help_from_docstring(function_to_test_docstring)
        == "Function to test docstring styles.\n"
    )


def test_get_help_from_docstring_with_no_docstring() -> None:
    function_to_test_docstring.__doc__ = None
    assert get_help_from_docstring(function_to_test_docstring) == ""


def test_get_help_from_docstring_with_no_style() -> None:
    function_to_test_docstring.__doc__ = (
        """Function to test docstring styles."""
    )
    assert (
        get_help_from_docstring(function_to_test_docstring)
        == "Function to test docstring styles.\n"
    )


@pytest.mark.parametrize("style", DOCSTRINGS)
@pytest.mark.parametrize("param", PARAMS)
def test_get_param_help_from_docstring(param: str, style: str) -> None:
    function_to_test_docstring.__doc__ = DOCSTRINGS[style]
    assert (
        get_param_help_from_docstring(param, function_to_test_docstring)
        == PARAMS[param]
    )


def test_get_param_help_from_docstring_with_no_docstring() -> None:
    function_to_test_docstring.__doc__ = None
    assert (
        get_param_help_from_docstring("param", function_to_test_docstring)
        == ""
    )


def test_get_param_help_from_docstring_with_no_style() -> None:
    function_to_test_docstring.__doc__ = (
        """Function to test docstring styles."""
    )
    assert (
        get_param_help_from_docstring("param", function_to_test_docstring)
        == ""
    )
