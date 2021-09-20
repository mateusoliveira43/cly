import subprocess
from typing import List, Optional

SPACE = ' '


def parse_arguments(arguments: List[str]) -> str:
    """Parses the arguments list.

    Parameters
    ----------
    arguments : List[str]
        A list of strings containing the commands and arguments.

    Returns
    -------
    parsed_arguments : str
        String concaneted by single spaces with the values of the list.
    """
    return SPACE.join(arguments)


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
        capture_output=True,
        encoding='utf-8'
    ).stdout.replace('\n', SPACE)
    if output:
        return [word for word in output.split(SPACE) if word]
    return None


def run_command(arguments: List[str]):
    """Runs the shell command.

    Parameters
    ----------
    arguments : List[str]
        A list of strings containing the commands and arguments.

    Returns
    -------
    subprocess.CompletedProcess[str]
        Executes the command and exits 0 (success) to shell; else, throws an
        error.
    """
    command = parse_arguments(arguments)
    return subprocess.run(
        command,
        shell=True,
        check=True,
        encoding='utf-8'
    )
