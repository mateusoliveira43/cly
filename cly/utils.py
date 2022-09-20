"""Utils functions for calling shell."""

# Scripts that manipulate the shell must always be careful with possible
# security implications.
import subprocess  # nosec
from pathlib import Path
from typing import List, Optional, Sequence, Tuple, Union

from .colors import color_text

SPACE = " "


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
    command = parse_arguments(arguments)
    return subprocess.run(
        command,
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
    output = get_output(arguments, directory)
    return output.returncode


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


def run_command(
    arguments: Union[str, List[str]], directory: Optional[Path] = None
) -> subprocess.CompletedProcess:  # type: ignore
    """
    Run the shell command.

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
        Executes the command.

    Raises
    ------
    SystemExit
        If command fails.

    """
    command = parse_arguments(arguments)
    try:
        return subprocess.run(
            command,
            shell=True,  # nosec
            check=True,
            encoding="utf-8",
            cwd=directory,
        )
    except subprocess.CalledProcessError as error:
        print(color_text(f"ERROR: {error}", "red"))
        raise SystemExit(error.returncode) from error


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
        subprocess.run(
            parse_arguments(arguments),
            shell=True,  # nosec
            check=False,
            encoding="utf-8",
            cwd=directory,
        )
        for arguments, directory in commands
    ]
    error_commands = [
        print(
            color_text(
                f"ERROR: Command '{command.args}' returned non-zero "
                f"exit status {command.returncode}.",
                "red",
            )
        )
        for command in filter(lambda c: c.returncode > 0, executed_commands)
    ]
    raise SystemExit(len(error_commands))
