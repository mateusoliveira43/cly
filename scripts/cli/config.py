"""argparse's parser custom configuration."""

import argparse
import sys
from types import GenericAlias
from typing import Any, Dict, Iterable, List, Optional, Union

from cli.colors import color_text

USAGE_PREFIX = "Usage:\n  [python|python3] "
POSITIONALS_TITLE = "Required options"
OPTIONALS_TITLE = "Options"
HELP_MESSAGE = "Show script's help message."
VERSION_MESSAGE = "Show script's version."
MAJOR_VERSION = 3
MINOR_VERSION = 7
PYTHON_MINIMUM_VERSION = (MAJOR_VERSION, MINOR_VERSION)


setattr(
    argparse._SubParsersAction, "__class_getitem__", classmethod(GenericAlias)
)


def check_python_minimum_version() -> None:
    """
    Check if user Python's version is valid to running the template.

    Raises
    ------
    SystemExit
        If user Python's version is invalid.

    """
    user_version = (sys.version_info.major, sys.version_info.minor)
    if user_version < PYTHON_MINIMUM_VERSION:
        print(
            color_text(
                f"ERROR: Python version {user_version[0]}.{user_version[1]} "
                f"does not meet minimum requirement of {MAJOR_VERSION}."
                f"{MINOR_VERSION}.",
                "red",
            )
        )
        raise SystemExit(1)


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


def get_command_help_message(command: str) -> str:
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


def initialize_parser(add_help: bool = True) -> List[str]:
    """
    Initialize the CLI parser.

    Parameters
    ----------
    add_help : bool, optional
        Add help option if no arguments are passed, by default True.

    Returns
    -------
    List[str]
        List of arguments to be parsed by argparse.

    """
    if add_help:
        return sys.argv[1:] or ["--help"]
    return sys.argv[1:]


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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Call super class init's."""
        super().__init__(*args, **kwargs)

    def _format_usage(
        self,
        usage: str,
        actions: Iterable[argparse.Action],
        groups: Iterable[argparse._ArgumentGroup],
        prefix: Optional[str],
    ) -> str:
        return super()._format_usage(usage, actions, groups, USAGE_PREFIX)

    def _format_action(self, action: argparse.Action) -> str:
        parts = super()._format_action(action)
        if action.nargs == argparse.PARSER:
            line_break = "\n"
            parts = line_break.join(parts.split(line_break)[1:])
        return parts

    def _format_action_invocation(self, action: argparse.Action) -> str:
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        metavar = self._format_args(
            action, self._get_default_metavar_for_optional(action)
        )
        comma = ", "
        return f"{comma.join(action.option_strings)} {metavar}"


class ConfiguredParser:
    """Configured argparse's argument parser."""

    def __init__(
        self,
        config: Dict[str, str],
        add_help: bool = True,
    ) -> None:
        """
        Initialize parser class.

        Parameters
        ----------
        config : dict
            Configurations dict for parser with keys name, description, epilog
            and version.
        add_help : bool, optional
            If parser should call the script help if no arguments are provided,
            by default True.

        """
        self.name = config["name"]
        self.description = config["description"]
        self.epilog = config["epilog"]
        self.version = config["version"]
        self.add_help = add_help
        self.parser = self.create_parser()
        self.subparser: Union[argparse._SubParsersAction, None] = None

    def create_parser(self) -> argparse.ArgumentParser:
        """
        Create configured parser to create script.

        Returns
        -------
        ArgumentParser
            Configured argparse's parser.

        """
        check_python_minimum_version()
        parser = argparse.ArgumentParser(
            prog=sys.argv[0],
            description=self.description,
            epilog=self.epilog,
            allow_abbrev=False,
            formatter_class=CustomFormatter,
        )
        parser.add_argument(
            "-v",
            "--version",
            action="version",
            version=get_version(self.name, self.version),
            help=VERSION_MESSAGE,
        )
        parser._positionals.title = POSITIONALS_TITLE
        parser._optionals.title = OPTIONALS_TITLE
        parser._actions[0].help = HELP_MESSAGE
        return parser

    def create_subparser(
        self,
    ) -> argparse._SubParsersAction[argparse.ArgumentParser]:
        """
        Create configured subparser to add commands.

        Returns
        -------
        argparse._SubParsersAction[argparse.ArgumentParser]
            Configured argparse's subparser.

        """
        return self.parser.add_subparsers(
            dest="command",
            metavar="[COMMAND]",
            title="Commands",
            prog=sys.argv[0],
        )

    def create_command(
        self, name: str, help_message: str
    ) -> argparse.ArgumentParser:
        """
        Create configured command to script.

        Parameters
        ----------
        name : str
            Name of the command.
        help_message : str
            Help message of the command.

        Returns
        -------
        ArgumentParser
            Configured argparse's parser command.

        """
        self.subparser = self.subparser or self.create_subparser()
        command: argparse.ArgumentParser = self.subparser.add_parser(
            name, help=help_message
        )
        command.formatter_class = CustomFormatter
        command._positionals.title = POSITIONALS_TITLE
        command._optionals.title = OPTIONALS_TITLE
        command._actions[0].help = get_command_help_message(name)
        command.description = help_message
        command.epilog = self.epilog
        return command

    def get_arguments(self) -> argparse.Namespace:
        """
        Get arguments the script was called with.

        Returns
        -------
        Namespace
            Arguments in argparse's namespace.

        """
        return self.parser.parse_args(initialize_parser(self.add_help))
