"""argparse's parser custom configuration."""

import argparse
import functools
import inspect
import sys
import textwrap
from typing import Any, Callable, Dict, Iterable, Optional

from .colors import color_text
from .docstring import get_help_from_docstring, get_param_help_from_docstring

USAGE_PREFIX = "Usage:\n  [python|python3] "
POSITIONALS_TITLE = "Arguments"
OPTIONALS_TITLE = "Options"
HELP_MESSAGE = "Show script's help message."
VERSION_MESSAGE = "Show script's version."
MAJOR_VERSION = 3
MINOR_VERSION = 7
PYTHON_MINIMUM_VERSION = (MAJOR_VERSION, MINOR_VERSION)
OptionalSubParser = Optional[argparse._SubParsersAction]


def check_python_minimum_version() -> None:
    """
    Check if user Python's version is valid to running the template.

    Raises
    ------
    SystemExit
        If user Python's version is invalid.

    """
    if sys.version_info < PYTHON_MINIMUM_VERSION:
        print(
            color_text(
                f"ERROR: Python version {sys.version_info.major}."
                f"{sys.version_info.minor} does not meet minimum requirement "
                f"of {MAJOR_VERSION}.{MINOR_VERSION}.",
                "red",
            )
        )
        raise SystemExit(1)


def decorate_kwargs(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Call decorated function only with it's key words arguments.

    Parameters
    ----------
    func : Callable[..., Any]
        Function to be decorated.

    Returns
    -------
    Callable[..., Any]
        Decorated function.

    """

    @functools.wraps(func)
    def wrap(**kwargs: Any) -> Any:
        for kwarg in set(kwargs.keys()) - set(func.__code__.co_varnames):
            kwargs.pop(kwarg)
        return func(**kwargs)

    return wrap


def iterate_through_params(
    commands: Dict[str, Callable[..., Any]],
    choices: Dict[str, argparse.ArgumentParser],
) -> None:
    """
    Iterate through commands' parameters help with docstrings content.

    Parameters
    ----------
    commands : Dict[str, Callable[..., Any]]
        Narrowed type ConfiguredParser' commands.
    choices : Dict[str, argparse.ArgumentParser]
        Narrowed type argparse's choices.

    """
    for command_name, command in commands.items():
        for param in inspect.signature(command).parameters.values():
            for action in choices[command_name]._actions[1:]:
                if action.dest == param.name and not action.help:
                    action.help = get_param_help_from_docstring(
                        param.name, command
                    )
                    break


class CustomFormatter(argparse.HelpFormatter):
    """Custom formatter for argparse's argument parser."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Call super class init's."""
        super().__init__(*args, **kwargs)

    def _format_usage(
        self,
        usage: Optional[str],
        actions: Iterable[argparse.Action],
        groups: Iterable[argparse._ArgumentGroup],
        prefix: Optional[str],
    ) -> str:
        """
        Format prefix of usage section.

        Parameters
        ----------
        usage : Optional[str]
            usage.
        actions : Iterable[argparse.Action]
            argparse actions.
        groups : Iterable[argparse._ArgumentGroup]
            argparse groups.
        prefix : Optional[str]
            usage prefix.

        Returns
        -------
        str
            Formatted usage section.

        """
        return super()._format_usage(usage, actions, groups, USAGE_PREFIX)

    def _format_action(self, action: argparse.Action) -> str:
        """
        Remove subparser's metavar when listing its parsers.

        Parameters
        ----------
        action : argparse.Action
            argparse action.

        Returns
        -------
        str
            subparser's section without metavar.

        """
        parts = super()._format_action(action)
        if action.nargs == argparse.PARSER:
            line_break = "\n"
            parts = line_break.join(parts.split(line_break)[1:])
        return parts

    def _format_action_invocation(self, action: argparse.Action) -> str:
        """
        Add metavar only once to arguments.

        Parameters
        ----------
        action : argparse.Action
            argparse action.

        Returns
        -------
        str
            How to use option with only one metavar.

        """
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        metavar = self._format_args(
            action, self._get_default_metavar_for_optional(action)
        )
        comma = ", "
        return f"{comma.join(action.option_strings)} {metavar}"

    def _fill_text(self, text: str, width: int, indent: str) -> str:
        """
        Format text to fit desired width.

        Breaks text in paragraphs so it does not exceed the width limit,
        respecting indentation.

        Parameters
        ----------
        text : str
            Text to be formatted.
        width : int
            Width limit.
        indent : str
            Indentation.

        Returns
        -------
        str
            Formatted text.

        """
        return "\n\n".join(
            textwrap.fill(
                line,
                width,
                initial_indent=indent,
                subsequent_indent=indent,
            )
            for line in text.split("\n\n")
        )


# pylint: disable=too-many-instance-attributes
class ConfiguredParser:
    """Configured argparse's argument parser."""

    name: str
    description: str
    epilog: str
    version: str
    add_help: bool
    parser: argparse.ArgumentParser
    subparser: OptionalSubParser
    commands: Optional[Dict[str, Callable[..., Any]]]

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
        self.subparser: OptionalSubParser = None
        self.commands: Optional[Dict[str, Callable[..., Any]]] = None

    def create_parser(self) -> argparse.ArgumentParser:
        """
        Create configured parser to create script.

        Returns
        -------
        argparse.ArgumentParser
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
            version=f"{self.name} version {self.version}",
            help=VERSION_MESSAGE,
        )
        parser._positionals.title = POSITIONALS_TITLE
        parser._optionals.title = OPTIONALS_TITLE
        parser._actions[0].help = HELP_MESSAGE
        return parser

    def create_subparser(
        self,
    ) -> "argparse._SubParsersAction[argparse.ArgumentParser]":
        """
        Create configured subparser to add commands.

        Returns
        -------
        argparse._SubParsersAction
            Configured argparse's subparser.

        """
        return self.parser.add_subparsers(
            dest="commands",
            metavar="command",
            title="Commands",
            prog=sys.argv[0],
            required=True,
        )

    def create_command(
        self,
        command: Callable[..., Any],
        alias: Optional[str] = None,
        help_message: Optional[str] = None,
    ) -> argparse.ArgumentParser:
        """
        Create configured command to script.

        Parameters
        ----------
        command : Callable[..., Any]
            Function that represents the command.
        alias : Optional[str]
            Alias to call command, by default None
        help_message : Optional[str]
            Help message of the command, by default None

        Returns
        -------
        argparse.ArgumentParser
            Configured argparse's parser command.

        """
        self.subparser = self.subparser or self.create_subparser()
        self.commands = self.commands or {}
        argparse_help = (
            help_message if help_message else get_help_from_docstring(command)
        )
        argparse_command: argparse.ArgumentParser = self.subparser.add_parser(
            alias if alias else command.__name__,
            help=argparse_help.split("\n", maxsplit=1)[0],
        )
        self.commands[alias if alias else command.__name__] = decorate_kwargs(
            command
        )
        argparse_command.formatter_class = CustomFormatter
        argparse_command._positionals.title = POSITIONALS_TITLE
        argparse_command._optionals.title = OPTIONALS_TITLE
        argparse_command._actions[0].help = "Show command's help message."
        argparse_command.description = argparse_help
        argparse_command.epilog = self.epilog
        return argparse_command

    def get_arguments(self) -> argparse.Namespace:
        """
        Get arguments the script was called with.

        Returns
        -------
        argparse.Namespace
            Arguments in argparse's namespace.

        """
        return self.parser.parse_args(
            sys.argv[1:] or ["--help"] if self.add_help else sys.argv[1:]
        )

    def populate_commands_param_help(
        self,
        commands: Dict[str, Callable[..., Any]],
    ) -> None:
        """
        Populate commands' parameters help with docstrings content.

        Parameters
        ----------
        commands : Dict[str, Callable[..., Any]]
            Narrowed type self.commands.

        """
        subparsers = self.parser._subparsers
        if isinstance(subparsers, argparse._ArgumentGroup):
            choices = subparsers._group_actions[0].choices
            if isinstance(choices, dict):
                iterate_through_params(commands, choices)

    def __call__(self) -> None:
        """Initialize the CLI parser."""
        if isinstance(self.commands, dict):
            self.populate_commands_param_help(self.commands)
            namespace = self.get_arguments()
            if namespace.commands:
                self.commands[namespace.commands](
                    **dict(namespace._get_kwargs())
                )
        else:
            self.get_arguments()
