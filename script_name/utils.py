import subprocess
from typing import List, Optional


def parse_arguments(arguments: List[str]) -> str:
    """Parses the arguments list.

    Parameters
    ----------
    arguments : List[str]
        A list of strings containing the commands and arguments.

    Returns
    -------
    parsed_arguments : str
        String concaneted by the values of the list.
    """
    separator = ' '
    return separator.join(arguments)


def get_returncode(arguments: List[str]) -> bool:
    """Gets the returncode of the shell command.

    Parameters
    ----------
    arguments : List[str]
        A list of strings containing the commands and arguments.

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


def get_output(arguments: List[str]) -> Optional[List[str]]:
    """Gets the output of the shell command.

    Parameters
    ----------
    arguments : List[str]
        A list of strings containing the commands and arguments.

    Returns
    -------
    output : Optional[List[str]]
        A list of strings containing the output's words; else, None.
    """
    command = parse_arguments(arguments)
    output = subprocess.run(
        command,
        shell=True,
        capture_output=True
    ).stdout.decode('utf-8').replace('\n', ' ').strip()
    if output:
        return output.split(' ')
    return None


def run_command(arguments: List[str]):
    """Runs the shell command.

    Parameters
    ----------
    arguments : List[str]
        A list of strings containing the commands and arguments.

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
