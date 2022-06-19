"""Unit tests of module scripts.example.command1."""

import pytest

from scripts.example.command1 import command1


def test_command1_without_options(capsys: pytest.CaptureFixture[str]) -> None:
    """Test command1 without options."""
    command1()
    output, error = capsys.readouterr()
    assert not error
    assert output == "Command 1 called.\n"


def test_command1_with_text(capsys: pytest.CaptureFixture[str]) -> None:
    """Test command1 with text."""
    command1(text="text")
    output, error = capsys.readouterr()
    assert not error
    assert "Text argument called with text.\n" in output


def test_command1_with_number(capsys: pytest.CaptureFixture[str]) -> None:
    """Test command1 with number."""
    command1(number=1)
    output, error = capsys.readouterr()
    assert not error
    assert "Number argument called with 1.\n" in output
