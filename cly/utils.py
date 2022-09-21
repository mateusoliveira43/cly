"""Utils functions for calling shell."""

# Scripts that manipulate the shell must always be careful with possible
# security implications.
import subprocess  # nosec
from pathlib import Path
from typing import List, Optional, Sequence, Tuple, Union

from .colors import color_text

SPACE = " "


def print_error_message(command: subprocess.Popen[str]) -> None:
    """
    Print error message from a command.

    Parameters
    ----------
    command : subprocess.Popen[str]
        Command to get information from.

    """
    print(
        color_text(
            f"ERROR: Command '{command.args}' returned "  # type: ignore
            f"non-zero exit status {command.returncode}.",
            "red",
        )
    )


def parse_arguments(arguments: Union[str, List[str]]) -> str:
    """
    Parse arguments into a string.

    Parameters
    ----------
    arguments : Union[str, List[str]]
        A string, or list of strings, containing the commands and arguments.

    Returns
    -------
    str
        Parsed arguments.

    """
    if isinstance(arguments, list):
        return SPACE.join(arguments)
    return arguments


def get_output(
    arguments: Union[str, List[str]], directory: Optional[Path] = None
) -> subprocess.CompletedProcess:  # type: ignore
    """
    Get the output information of the shell command.

    **Be careful about security implications when manipulating the shell!**

    Parameters
    ----------
    arguments : Union[str, List[str]]
        A string, or list of strings, containing the commands and arguments.
    directory : Optional[pathlib.Path]
        Directory to run shell command, by default runs in current directory.

    Returns
    -------
    subprocess.CompletedProcess
        Command's output information.

    """
    return subprocess.run(
        parse_arguments(arguments),
        shell=True,  # nosec
        check=False,
        capture_output=True,
        encoding="utf-8",
        cwd=directory,
    )


def get_returncode(
    arguments: Union[str, List[str]], directory: Optional[Path] = None
) -> int:
    """
    Get the returncode of the shell command.

    **Be careful about security implications when manipulating the shell!**

    Parameters
    ----------
    arguments : Union[str, List[str]]
        A string, or list of strings, containing the commands and arguments.
    directory : Optional[pathlib.Path]
        Directory to run shell command, by default runs in current directory.

    Returns
    -------
    int
        Command's returncode.

    """
    return get_output(arguments, directory).returncode


def get_standard_output(
    arguments: Union[str, List[str]],
    lines: bool = False,
    directory: Optional[Path] = None,
) -> Optional[List[str]]:
    """
    Get the standard output of the shell command.

    **Be careful about security implications when manipulating the shell!**

    Parameters
    ----------
    arguments : Union[str, List[str]]
        A string, or list of strings, containing the commands and arguments.
    lines : bool
        Separate output in lines instead of separating in words, by default
        False.
    directory : Optional[pathlib.Path]
        Directory to run shell command, by default runs in current directory.

    Returns
    -------
    output : Optional[List[str]]
        A list of strings containing the output's words or lines; else, None.

    """
    output = get_output(arguments, directory).stdout
    if output:
        if lines:
            return [line for line in output.split("\n") if line]
        return [
            word for word in output.replace("\n", SPACE).split(SPACE) if word
        ]
    return None


def get_command_after_execution(
    arguments: Union[str, List[str]], directory: Optional[Path] = None
) -> subprocess.Popen[str]:
    """
    Get shell command information after it executes.

    The command output is printed to the user.

    Parameters
    ----------
    arguments : Union[str, List[str]]
        Shell command and arguments to be executed.
    directory : Optional[Path]
        Directory to run shell command, by default runs in current directory.

    Returns
    -------
    subprocess.Popen[str]
        Executed command.

    """
    command = subprocess.Popen(
        parse_arguments(arguments),
        shell=True,  # nosec
        encoding="utf-8",
        cwd=directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    with command:
        while command.poll() is None:
            print(command.stdout.readline(), end="")  # type: ignore
        print(command.stdout.read(), end="")  # type: ignore
    return command


def run_command(
    arguments: Union[str, List[str]], directory: Optional[Path] = None
) -> None:
    """
    Run the shell command.

    **Be careful about security implications when manipulating the shell!**

    Parameters
    ----------
    arguments : Union[str, List[str]]
        A string, or list of strings, containing the commands and arguments.
    directory : Optional[pathlib.Path]
        Directory to run shell command, by default runs in current directory.

    Raises
    ------
    SystemExit
        If command fails.

    """
    command = get_command_after_execution(arguments, directory)
    if command.returncode:
        print_error_message(command)
        raise SystemExit(command.returncode)


def run_multiple_commands(
    commands: Sequence[Tuple[Union[str, List[str]], Optional[Path]]]
) -> None:
    """
    Run multiple shell commands.

    **Be careful about security implications when manipulating the shell!**

    Parameters
    ----------
    commands: Sequence[Tuple[Union[str, List[str]], Optional[pathlib.Path]]]
        List of commands, where each command is a tuple of commands and
        arguments and directory, to be executed.

    Raises
    ------
    SystemExit
        If one of the command fails.

    """
    executed_commands = [
        get_command_after_execution(arguments, directory)
        for arguments, directory in commands
    ]
    error_commands = [
        print_error_message(command)  # type: ignore
        for command in executed_commands
        if command.returncode
    ]
    if error_commands:
        raise SystemExit(len(error_commands))
