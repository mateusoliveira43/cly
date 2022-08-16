"""Create command example."""

from ..database import CHARACTERS, get_alias_data, get_oracle_data


def list_aliases(
    oracle: bool = False,
) -> None:
    """
    List all aliases in Batcomputer.

    Parameters
    ----------
    oracle : bool, optional
        Use Oracle's help to get more data, by default False

    """
    aliases = [
        get_oracle_data(alias) if oracle else get_alias_data(alias)
        for alias in CHARACTERS
    ]
    print(*aliases, sep="\n")
