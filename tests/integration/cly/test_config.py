import pytest

from cly import config

CLI_CONFIG = {
    "name": "Test",
    "description": "",
    "epilog": "",
    "version": "test",
}
METAVAR = "STRING"

CLI = config.ConfiguredParser(CLI_CONFIG)
CLI.parser.add_argument(
    "-t",
    "--test",
    metavar=METAVAR,
    type=str,
)


def test_metavar_only_appears_once_in_help(
    capsys: pytest.CaptureFixture[str],
) -> None:
    CLI.parser.print_help()
    output, error = capsys.readouterr()
    assert not error
    assert output.count(METAVAR) == 2  # and once in usage
