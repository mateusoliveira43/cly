import re
import pytest

from ....batcomputer_cli.commands.identify import identify
from ....batcomputer_cli.database import CHARACTERS

NON_IDENTIFIED_CHARACTERS = ["riddler", "nightwing", "penguin"]

UPPER_CASE_CHARACTERS = [character.upper() for character in CHARACTERS]
TITLE_CASE_CHARACTERS = [character.title() for character in CHARACTERS]

@pytest.mark.parametrize(
    "alias", list(CHARACTERS) + UPPER_CASE_CHARACTERS + TITLE_CASE_CHARACTERS
)
def test_identify_with_one_identified_alias_and_its_oracle(
    alias: str, capsys: pytest.CaptureFixture[str]
) -> None:
    bring_oracle = True
    identify([alias], bring_oracle)
    output, error = capsys.readouterr()
    print("output", output)
    assert not error
    assert "A.K.A" in output
    assert "The Dark Knight (2008)" in output


@pytest.mark.parametrize(
    "alias", list(CHARACTERS) + UPPER_CASE_CHARACTERS + TITLE_CASE_CHARACTERS
)
def test_identify_with_one_identified_alias(
    alias: str, capsys: pytest.CaptureFixture[str]
) -> None:
    identify([alias])
    output, error = capsys.readouterr()
    assert not error
    assert "A.K.A" in output


@pytest.mark.parametrize("alias", NON_IDENTIFIED_CHARACTERS)
def test_identify_with_one_non_identified_alias(
    alias: str, capsys: pytest.CaptureFixture[str]
) -> None:
    identify([alias])
    output, error = capsys.readouterr()
    assert not output
    assert "not identified" in error


# TODO test with more then one input
