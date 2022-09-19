CHARACTERS = {
    "batman": "Bruce Wayne",
    "joker": "Jack Napier",
    "two-face": "Harvey Dent",
}

ACTORS = {
    "batman": "Christian Bale",
    "joker": "Heath Ledger",
    "two-face": "Aaron Eckhart",
}

LINES = {
    "batman": (
        "Sometimes the truth isn't good enough, sometimes people deserve more."
        " Sometimes people deserve to have their faith rewarded..."
    ),
    "joker": "Why so serious?",
    "two-face": (
        "You either die a hero or you live long enough to see yourself become "
        "the villain."
    ),
}

ICONS = {
    "batman": "\N{bat}",
    "joker": "\N{clown face}",
    "two-face": "",
}


def get_alias_data(alias: str) -> str:
    """
    Get alias' data from Batcomputer.

    Parameters
    ----------
    alias : str
        Alias already identified by Batcomputer.

    Returns
    -------
    str
        Alias' data.

    """
    return f"{CHARACTERS[alias]} A.K.A. {alias.title()} {ICONS[alias]}"


def get_oracle_data(alias: str) -> str:
    """
    Get more alias' data with Oracle's help.

    Parameters
    ----------
    alias : str
        Alias already identified by Batcomputer.

    Returns
    -------
    str
        Alias' data.

    """
    return (
        f'{get_alias_data(alias)}\n  "{LINES[alias]}"\n  '
        f"Portrayed by {ACTORS[alias]} in The Dark Knight (2008)"
    )
