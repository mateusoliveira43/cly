import math
import shutil
import subprocess
import sys
from typing import List, Optional, Union

SPACE = ' '
COMMA = ', '
DEFAULT = '\033[0m'
UNDERLINE = '\033[4m'
COLORS = {
    'green': '\033[1;92m',
    'red': '\033[1;91m',
    'yellow': '\033[1;93m',
}


def format_options(options: list) -> str:
    """
    Format a list of options separating them with comma and 'or'.

    Parameters
    ----------
    options : list
        List of options.

    Returns
    -------
    str
        Formated options.

    """
    if len(options) < 2:
        return ''.join(options)
    return f'{COMMA.join(options[:-1])} or {options[-1]}'


def get_color(color: COLORS) -> str:
    """
    Get available color by name.

    Parameters
    ----------
    color : COLORS
        One of the available colors' name.

    Returns
    -------
    str
        Unicode character of color, if available; else, exits error returncode
        1.

    """
    try:
        return COLORS[color]
    except KeyError:
        print(
            f'{COLORS["red"]}ERROR: {UNDERLINE}{color}{DEFAULT}{COLORS["red"]}'
            ' is not a valid color. Available colors: '
            f'{format_options(list(COLORS.keys()))}.'
        )
        sys.exit(1)


def underline_text(text: str, color: COLORS = None) -> str:
    """
    Underline text.

    Parameters
    ----------
    text : str
        Text to underline.
    color : COLORS, optional
        Color of end character of text, by defult None.

    Returns
    -------
    str
        Underlined text.

    """
    end_character = DEFAULT
    if color:
        end_character += get_color(color)
    return f'{UNDERLINE}{text}{end_character}'


def color_text(text: str, color: COLORS) -> str:
    """
    Color text with one of the available colors.

    Parameters
    ----------
    text : str
        Text to color.
    color : COLOR
        One of the available colors.

    Returns
    -------
    str
        Colored text.

    """
    return f'{get_color(color)}{text}{DEFAULT}'


def get_print_length(message: str) -> int:
    """
    Get the length user sees in shell of message.

    Parameters
    ----------
    message : str
        Message to disregard length of characters user do not see in shell.

    Returns
    -------
    int
        Length user sees in shell.

    """
    checker = {
        **COLORS,
        'underline': UNDERLINE,
        'default': DEFAULT,
    }
    message_length = len(message)
    for style in checker.values():
        if style in message:
            message_length -= message.count(style) * len(style)
    return message_length


def print_flashy(message: str) -> None:
    """
    Print centralized message by ">" and "<" with width equal to user shell.

    Parameters
    ----------
    message : str
        Message to centralize.

    """
    width, _ = shutil.get_terminal_size()
    message_width = get_print_length(message) + 2
    left = math.floor((width - message_width) / 2)
    right = width - left - message_width
    print(f"{'>'*left} {message} {'<'*right}")


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
    arguments: Union[str, List[str]]
) -> subprocess.CompletedProcess:
    """
    Get the output information of the shell command.

    Parameters
    ----------
    arguments : Union[str, List[str]]
        A string, or list of strings, containing the commands and arguments.

    Returns
    -------
    int
        Command's output information.

    """
    command = parse_arguments(arguments)
    return subprocess.run(
        command,
        shell=True,
        check=False,
        capture_output=True,
        encoding='utf-8'
    )


def get_returncode(arguments: Union[str, List[str]]) -> int:
    """
    Get the returncode of the shell command.

    Parameters
    ----------
    arguments : Union[str, List[str]]
        A string, or list of strings, containing the commands and arguments.

    Returns
    -------
    int
        Command's returncode.

    """
    output = get_output(arguments)
    return output.returncode


def get_standard_output(
    arguments: Union[str, List[str]], lines: bool = False
) -> Optional[List[str]]:
    """
    Get the standard output of the shell command.

    Parameters
    ----------
    arguments : Union[str, List[str]]
        A string, or list of strings, containing the commands and arguments.
    lines : bool, optional
        Separate output in lines instead of word, by default False.

    Returns
    -------
    output : Optional[List[str]]
       A list of strings containing the output's words; else, None.

    """
    output = get_output(arguments).stdout
    if output:
        if lines:
            return [line for line in output.split('\n') if line]
        return [
            word for word in output.replace('\n', SPACE).split(SPACE) if word
        ]
    return None


def run_command(
    arguments: Union[str, List[str]]
) -> subprocess.CompletedProcess:
    """
    Run the shell command.

    Parameters
    ----------
    arguments : Union[str, List[str]]
        A string, or list of strings, containing the commands and arguments.

    Returns
    -------
    subprocess.CompletedProcess[str]
        Executes the command (success); else, exits error returncode of the
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
        message = str(error).replace("'", UNDERLINE, 1)
        message = (DEFAULT + COLORS['red']).join(message.rsplit("'", 1))
        print(color_text(f'ERROR: {message}', 'red'))
        sys.exit(error.returncode)
