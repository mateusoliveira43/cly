"""argparse's parser custom configuration."""

import argparse
import sys

USAGE_PREFIX = "Usage:\n  [python|python3] "
EPILOG = "Script epilog."
POSITIONALS_TITLE = "Required options"
OPTIONALS_TITLE = "Options"
HELP_MESSAGE = "Show script's help message."
VERSION_MESSAGE = "Show script's version."
PYTHON_MINIMUM_VERSION = (3, 7)


def check_python_minimum_version():
    """Check if user Python's version is valid to running the template."""
    user_version = (sys.version_info.major, sys.version_info.minor)
    if user_version < PYTHON_MINIMUM_VERSION:
        # TODO create colors file, to avoid cyclic dependencies
        print(
            "Python version does not meet minimum requirement",
            PYTHON_MINIMUM_VERSION,
        )
        sys.exit(1)


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
    return f"{name} version {version}"


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
    return f"Show {command} command help message."


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
        return super()._format_usage(usage, actions, groups, USAGE_PREFIX)

    def _format_action(self, action):
        parts = super()._format_action(action)
        if action.nargs == argparse.PARSER:
            line_break = "\n"
            parts = line_break.join(parts.split(line_break)[1:])
        return parts

    def _format_action_invocation(self, action):
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        metavar = self._format_args(
            action, self._get_default_metavar_for_optional(action)
        )
        comma = ", "
        return f"{comma.join(action.option_strings)} {metavar}"


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
    check_python_minimum_version()
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description=description,
        epilog=EPILOG,
        allow_abbrev=False,
        formatter_class=CustomFormatter,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=get_version(name, version),
        help=VERSION_MESSAGE,
    )
    parser._positionals.title = POSITIONALS_TITLE
    parser._optionals.title = OPTIONALS_TITLE
    parser._actions[0].help = HELP_MESSAGE
    return parser


def configured_subparser(
    parser: argparse.ArgumentParser,
) -> argparse._SubParsersAction:
    """
    Create configured subparser to add commands.

    Parameters
    ----------
    parser : ArgumentParser
        Argparse's parser.

    Returns
    -------
    _SubParsersAction
        Configured argparse's subparser.

    """
    return parser.add_subparsers(
        dest="command", metavar="[COMMAND]", title="Commands", prog=sys.argv[0]
    )


def configured_command(
    subparser: argparse._SubParsersAction, name: str, help_message: str
) -> argparse.ArgumentParser:
    """
    Create configured command to script.

    Parameters
    ----------
    subparser : _SubParsersAction
        Subparser to add command.
    name : str
        Name of the command.
    help_message : str
        Help message of the command.

    Returns
    -------
    ArgumentParser
        Configured argparse's parser command.

    """
    command = subparser.add_parser(name, help=help_message)
    command.formatter_class = CustomFormatter
    command._positionals.title = POSITIONALS_TITLE
    command._optionals.title = OPTIONALS_TITLE
    command._actions[0].help = get_command_help_messsage(name)
    command.description = help_message
    command.epilog = EPILOG
    return command


def initialize_parser(add_help: bool = True) -> list:
    """
    Initialize the CLI parser.

    Parameters
    ----------
    add_help : bool, optional
        Add help option if no arguments are passed, by default True.

    Returns
    -------
    list
        List of arguments to be parsed by argparse.

    """
    if add_help:
        return sys.argv[1:] or ["--help"]
    return sys.argv[1:]
