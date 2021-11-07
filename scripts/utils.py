import subprocess
import sys
from typing import List, Optional, Union

SPACE = ' '


def parse_arguments(arguments: Union[str, List[str]]) -> str:
    """
    Parse arguments.

    Parameters
    ----------
    arguments : Union[str, List[str]]
        A string, or list of strings, containing the commands and arguments.

    Returns
    -------
    str
        Arguments.

    """
    if isinstance(arguments, list):
        return SPACE.join(arguments)
    return arguments


def get_returncode(arguments: Union[str, List[str]]) -> bool:
    """
    Get the returncode of the shell command.

    Parameters
    ----------
    arguments : Union[str, List[str]]
        A string, or list of strings, containing the commands and arguments.

    Returns
    -------
    shell_returncode : bool
        True if command's returncode was 0; else, False.

    """
    command = parse_arguments(arguments)
    # pylint:disable=subprocess-run-check
    output = subprocess.run(
        command,
        shell=True,
        capture_output=True
    )
    return not output.returncode


def get_output(arguments: Union[str, List[str]]) -> Optional[List[str]]:
    """
    Get the output of the shell command.

    Parameters
    ----------
    arguments : Union[str, List[str]]
        A string, or list of strings, containing the commands and arguments.

    Returns
    -------
    output : Optional[List[str]]
        A list of strings containing the output's words; else, None.

    """
    command = parse_arguments(arguments)
    # pylint:disable=subprocess-run-check
    output = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        encoding='utf-8'
    ).stdout.replace('\n', SPACE)
    if output:
        return [word for word in output.split(SPACE) if word]
    return None


def run_command(arguments: Union[str, List[str]]):
    """
    Run the shell command.

    Parameters
    ----------
    arguments : Union[str, List[str]]
        A string, or list of strings, containing the commands and arguments.

    Returns
    -------
    subprocess.CompletedProcess[str]
        Executes the command (success); else, exits return code (error) of the
        command.

    """
    command = parse_arguments(arguments)
    try:
        return subprocess.run(
            command,
            shell=True,
            check=True,
            encoding='utf-8'
        )
    except subprocess.CalledProcessError as error:
        print(f'ERROR: {error}')
        sys.exit(error.returncode)
