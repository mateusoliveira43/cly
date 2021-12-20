import argparse
import sys

import config
import utils
from command1 import command1

__version__ = '1.0.0'  # major.minor.patch
NAME = 'Script name'
DESCRIPTION = 'Script description.'

parser = config.configured_parser(NAME, __version__, DESCRIPTION)

parser.add_argument(
    '-o', '--optional',
    action='store_const', const='optional',
    help='Description of the optional flag.'
)

# TODO think how to transform this part in a function
subparser = parser.add_subparsers(
    dest='command',
    metavar='[COMMAND]',
    title='Commands',
    prog=sys.argv[0]
)
commands = dict(
    command1=dict(
        help='Description of the command1.',
        command=command1
    ),
)
# automatically alphabetically sort commands
commands = dict(sorted(commands.items()))

for name, actions in commands.items():
    command = config.configured_command(subparser, name, actions)

    group = command.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-t', '--text',
        metavar='str', type=str,
        help='Example of argument that receives a string.'
    )
    group.add_argument(
        '-n', '--number',
        metavar='int', type=int,
        help='Example of argument that receives a integer.'
    )

    command.add_argument(
        dest='arguments',
        nargs=argparse.REMAINDER,
        help='Arbitrary arguments for a command.'
    )


def main():
    """Run script on user call."""
    args = parser.parse_args(config.initialize_parser())
    if args.optional:
        utils.print_flashy('Optional flag called.')
        for color in utils.COLORS.keys():
            utils.print_flashy(
                utils.color_text('Optional flag called.', color)
            )
        utils.print_flashy(f'Optional {utils.underline_text("flag")} called.')
        for color in utils.COLORS.keys():
            utils.print_flashy(utils.color_text(
                f'Optional {utils.underline_text("flag")} called.', color)
            )
            utils.print_flashy(utils.color_text(
                f'Optional {utils.underline_text("flag", color)} called.',
                color
            ))
        utils.print_flashy(
            f"{utils.color_text('Optional', 'green')} "
            f"{utils.color_text('flag', 'yellow')} "
            f"{utils.color_text('called.', 'red')}"
        )
    if args.command:
        commands.get(args.command).get('command')(**dict(args._get_kwargs()))
