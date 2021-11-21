import argparse
import sys
from typing import Callable, TypedDict

USAGE_PREFIX = 'Usage:\n  [python|python3] '
EPILOG = 'Script epilog.'
POSITIONALS_TITLE = 'Required options'
OPTIONALS_TITLE = 'Options'
HELP_MESSAGE = "Show script's help message."
VERSION_MESSAGE = "Show script's version."


class Command(TypedDict):
    """Actions of a command."""
    help: str
    command: Callable


def get_version(name: str, version: str) -> str:
    """
    Get the version of a script.

    Parameters
    ----------
    name : str
        Name of the script.
    version : str
        Version of the script, in format major.minor.patch.

    Returns
    -------
    str
        Script's version.

    """
    return f'{name} version {version}'


def get_command_help_messsage(command: str) -> str:
    """
    Get the help message for a command.

    Parameters
    ----------
    command : str
        Name of the command.

    Returns
    -------
    str
        Command's help message.

    """
    return f'Show {command} command help message.'


class CustomFormatter(argparse.HelpFormatter):
    """
    Custom formatter for argparse's argument parser.

    Methods
    -------
    _format_usage(self, usage, actions, groups, prefix)
        Formats prefix of usage section.

    _format_action(self, action)
        Removes subparser's metavar when listing its parsers.

    _format_action_invocation(self, action)
        Adds metavar only once to arguments.

    """
    def __init__(self, *args, **kwargs):
        """Call super class init's."""
        super().__init__(*args, **kwargs)

    def _format_usage(self, usage, actions, groups, prefix):
        return super()._format_usage(
            usage, actions, groups, USAGE_PREFIX
        )

    def _format_action(self, action):
        parts = super()._format_action(action)
        if action.nargs == argparse.PARSER:
            line_break = '\n'
            parts = line_break.join(parts.split(line_break)[1:])
        return parts

    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        metavar = self._format_args(
            action, self._get_default_metavar_for_optional(action)
        )
        comma = ', '
        return f'{comma.join(action.option_strings)} {metavar}'


def configured_parser(
    name: str, version: str, description: str
) -> argparse.ArgumentParser:
    """
    Create configured parser to create script.

    Parameters
    ----------
    name : str
        Name of the script.
    version : str
        Version of the script, in format major.minor.patch.
    description : str
        Description of the script.

    Returns
    -------
    ArgumentParser
        Configured argparse's parser.

    """
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description=description,
        epilog=EPILOG,
        allow_abbrev=False,
        formatter_class=CustomFormatter,
    )
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=get_version(name, version),
        help=VERSION_MESSAGE
    )
    parser._positionals.title = POSITIONALS_TITLE
    parser._optionals.title = OPTIONALS_TITLE
    parser._actions[0].help = HELP_MESSAGE
    return parser


def configured_command(
    subparser: argparse._SubParsersAction, name: str, actions: Command
) -> argparse.ArgumentParser:
    """
    Create configured command to script.

    Parameters
    ----------
    subparser : _SubParsersAction
        Supparser to add command.
    name : str
        Name of the command.
    actions : Command
        Actions of the command.

    Returns
    -------
    ArgumentParser
        Configured argparse's parser command.

    """
    command = subparser.add_parser(name, help=actions.get('help'))
    command.formatter_class = CustomFormatter
    command._positionals.title = POSITIONALS_TITLE
    command._optionals.title = OPTIONALS_TITLE
    command._actions[0].help = get_command_help_messsage(name)
    command.description = actions.get('help')
    command.epilog = EPILOG
    return command


def initialize_parser(parser: argparse.ArgumentParser) -> argparse.Namespace:
    """
    Initialize the CLI parser.

    Parameters
    ----------
    parser : ArgumentParser
        parser to get user arguments.

    Returns
    -------
    Namespace
        Arguments used and unused.

    """
    return parser.parse_args(sys.argv[1:] or ['--help'])
