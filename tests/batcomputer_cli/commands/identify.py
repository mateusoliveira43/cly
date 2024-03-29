import sys
from typing import List

from ..database import CHARACTERS, get_alias_data, get_oracle_data


def identify(
    aliases: List[str],
    oracle: bool = False,
) -> None:
    """
    Identify the person behind each alias.

    For each alias, get person behind it, if it is stored in Batcomputer. Else,
    informs each one not yet identified.

    Parameters
    ----------
    aliases : List[str]
        One or more alias to be identified, separated by spaces.
    oracle : bool, optional
        Use Oracle's help to get more data, by default False

    """
    responses = [
        (
            get_oracle_data(alias.lower())
            if oracle
            else get_alias_data(alias.lower()),
            sys.stdout,
        )
        if CHARACTERS.get(alias.lower())
        else (f"{alias.title()} not identified by Batcomputer yet", sys.stderr)
        for alias in aliases
    ]
    for response in responses:
        print(response[0], file=response[1])
