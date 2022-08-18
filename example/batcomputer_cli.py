"""Create configured argparse's CLI example."""

from cly import config

from . import __version__
from .commands.identify import identify
from .commands.list_aliases import list_aliases

CLI_CONFIG = {
    "name": "Batcomputer",
    "description": "Run Batcomputer analysis on selected areas.",
    "epilog": "Wayne Enterprises \N{office building}",
    "version": __version__,
}

CLI = config.ConfiguredParser(CLI_CONFIG)
CLI.parser.add_argument(
    "-o",
    "--oracle",
    action="store_true",
    help="Use Oracle's help to get more data.",
)

identify_command = CLI.create_command(identify, alias="id")
identify_command.add_argument(dest="aliases", metavar="aliases", nargs="+")

CLI.create_command(list_aliases, alias="ls")
