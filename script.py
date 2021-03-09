#!/usr/bin/env python3
import subprocess
import argparse
import sys
from typing import List


class CustomFormatter(argparse.HelpFormatter):
    def __init__(self, *args, **kwargs):
        super(CustomFormatter, self).__init__(*args, **kwargs)

    def _format_usage(self, usage, actions, groups, prefix):
        return super(CustomFormatter, self)._format_usage(
            usage, actions, groups, prefix if prefix else 'Usage: ')

    def _format_action(self, action):
        parts = super(CustomFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = '\n'.join(parts.split('\n')[1:])
        return parts


def parse_arguments(arguments: List[str]) -> str:
    """Parses the arguments list.

    Parameters
    ----------
    arguments : List[str]
        A list of strings containing the arguments.

    Returns
    -------
    parsed_arguments : str
        String concaneted by the values of the list.
    """
    separator = ' '
    return separator.join(arguments)


def get_returncode_from_shell(arguments: List[str]) -> bool:
    """Gets the returncode on the shell command.

    Parameters
    ----------
    arguments : List[str]
        A list of strings containing the arguments.

    Returns
    -------
    shell_returncode : bool
        True if shell's returncode was 0; else, False.
    """
    command = parse_arguments(arguments)
    output = subprocess.run(
        command,
        shell=True,
        capture_output=True
    )
    return not output.returncode


def run_from_shell(arguments: List[str]):
    """Runs the shell command.

    Parameters
    ----------
    arguments : List[str]
        A list of strings containing the arguments.

    Returns
    -------
    subprocess.run
        Executes the command and exits 0; else, throws an error.
    """
    command = parse_arguments(arguments)
    return subprocess.run(
        command,
        shell=True,
        check=True
    )


parser = argparse.ArgumentParser(
    prog='python3 ./script.py',
    description='Script description.',
    epilog='Script epilog.',
    allow_abbrev=False,
    formatter_class=CustomFormatter,
)
parser._positionals.title = 'Required options'
parser._optionals.title = 'Options'
parser._actions[0].help = 'Shows scipt\'s help message.'

# Required options ############################################################
parser.add_argument(
    'int',
    type=int,
    help='Description of the required argument.'
)

# Options #####################################################################
parser.add_argument(
    '-v', '--version',
    action='version',
    version='Python script template 0.1.0',
    help='Shows script\'s version.')
parser.add_argument(
    '-m', '--mateus',
    action='store_const', const='mateus',
    help='Description of the optional flag.'
)
parser.add_argument(
    '-t', '--test',
    metavar='str',
    type=str,
    help='Description of the optional flag that recives an argument.'
)

# Commands ####################################################################
subparser = parser.add_subparsers(
    dest='commands',
    metavar='[COMMAND]',
    title='Commands',
)
command1 = subparser.add_parser('command1', help='Description of the command.')
command2 = subparser.add_parser('command2', help='Description of the command.')

args = parser.parse_args(args=sys.argv[1:] or ['--help'])

print(args)
if args.mateus:
    print(args.mateus, get_returncode_from_shell(['mateus']))
print(get_returncode_from_shell(['python3', '--version']))
run_from_shell(['python3', '--version'])
