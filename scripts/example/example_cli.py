"""Create configured argparse's CLI example."""

import argparse

from cli import config, utils
from example.command1 import command1

__version__ = "1.0.0"  # major.minor.patch
NAME = "Script name"
DESCRIPTION = "Script description."

COMMANDS = {
    command1.__name__: command1,
}

parser = config.configured_parser(NAME, __version__, DESCRIPTION)

parser.add_argument(
    "-o",
    "--optional",
    action="store_true",
    help="Description of the optional flag.",
)

subparser = config.configured_subparser(parser)

command = config.configured_command(
    subparser, command1.__name__, "Description of the command1."
)
group = command.add_mutually_exclusive_group(required=True)
group.add_argument(
    "-t",
    "--text",
    metavar="str",
    type=str,
    help="Example of argument that receives a string.",
)
group.add_argument(
    "-n",
    "--number",
    metavar="int",
    type=int,
    help="Example of argument that receives a integer.",
)
command.add_argument(
    dest="arguments",
    nargs=argparse.REMAINDER,
    help="Arbitrary arguments for a command.",
)


def main():
    """Run script on user call."""
    args = parser.parse_args(config.initialize_parser())
    if args.optional:
        utils.print_flashy("Optional flag called.")
    if args.command:
        COMMANDS.get(args.command)(**dict(args._get_kwargs()))
