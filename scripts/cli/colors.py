import math
import shutil
import sys

COMMA = ", "
DEFAULT = "\033[0m"
UNDERLINE = "\033[4m"
COLORS = {
    "green": "\033[1;92m",
    "red": "\033[1;91m",
    "yellow": "\033[1;93m",
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
        return "".join(options)
    return f"{COMMA.join(options[:-1])} or {options[-1]}"


def get_color(color: str) -> str:
    """
    Get available color by name.

    Parameters
    ----------
    color : str
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
            " is not a valid color. Available colors: "
            f"{format_options(list(COLORS.keys()))}."
        )
        sys.exit(1)


def underline_text(text: str, color: str = None) -> str:
    """
    Underline text.

    Parameters
    ----------
    text : str
        Text to underline.
    color : str, optional
        One of the available colors' name for end character of text, by defult
        None.

    Returns
    -------
    str
        Underlined text.

    """
    end_character = DEFAULT
    if color:
        end_character += get_color(color)
    return f"{UNDERLINE}{text}{end_character}"


def color_text(text: str, color: str) -> str:
    """
    Color text with one of the available colors.

    Parameters
    ----------
    text : str
        Text to color.
    color : str
        One of the available colors' name.

    Returns
    -------
    str
        Colored text.

    """
    return f"{get_color(color)}{text}{DEFAULT}"


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
        "underline": UNDERLINE,
        "default": DEFAULT,
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
