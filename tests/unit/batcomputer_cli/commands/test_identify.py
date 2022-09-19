import pytest

from ....batcomputer_cli.commands.identify import identify
from ....batcomputer_cli.database import CHARACTERS

NON_IDENTIFIED_CHARACTERS = ["riddler", "nightwing", "penguin"]


@pytest.mark.parametrize("alias", CHARACTERS)
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
    assert not error
    assert "not identified" in output


# TODO test with more then one input
# TODO test with oracle option
