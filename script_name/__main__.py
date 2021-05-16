#!/usr/bin/env python3

import argparse
import sys

import config
import utils

parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    description=config.script_description,
    epilog=config.script_epilog,
    allow_abbrev=False,
    formatter_class=config.CustomFormatter,
)
parser.add_argument(
    '-v', '--version',
    action='version',
    version=config.version,
    help=config.version_message
)
parser._positionals.title = config.positionals_title
parser._optionals.title = config.optionals_title
parser._actions[0].help = config.help_message


# Options #####################################################################
parser.add_argument(
    '-m', '--mateus',
    action='store_const', const='mateus',
    help='Description of the optional flag.'
)


# Required options ############################################################
# parser.add_argument(
#     'int',
#     type=int,
#     help='Description of the required argument.'
# )


# Commands ####################################################################
subparser = parser.add_subparsers(
    dest='command',
    metavar='[COMMAND]',
    title='Commands',
    prog=sys.argv[0]
)
commands = dict(
    command1=dict(
        help='Description of the command1.'
    ),
    command2=dict(
        help='Description of the command2.'
    ),
)
# automatically alphabetically sort commands
commands = dict(sorted(commands.items()))

for command_name in commands:
    command = subparser.add_parser(
        command_name, help=commands.get(command_name).get('help')
    )
    command.formatter_class = config.CustomFormatter
    command._positionals.title = config.positionals_title
    command._optionals.title = config.optionals_title
    command._actions[0].help = config.get_command_help_messsage(command_name)
    command.description = commands.get(command_name).get('help')
    command.epilog = config.script_epilog

    group = command.add_mutually_exclusive_group()
    group.add_argument(
        '-e', '--example',
        metavar='str', type=str,
        help='example of argument of a command.'
    )
    group.add_argument(
        '-v', '--verbose',
        metavar='int', type=int,
        help='example of argument of a command.'
    )


# Parser Initializer ##########################################################
args = parser.parse_args(args=sys.argv[1:] or ['--help'])


def main():
    """Main function of the script."""
    if args.mateus:
        print(args)
        print('The author of this template :)')
    ls_command = ['ls', '-1a']
    print(utils.get_returncode(ls_command))
    print(utils.get_output(ls_command))
    utils.run_command(ls_command)


if __name__ == '__main__':
    main()
