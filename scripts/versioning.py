#!/usr/bin/env python3
"""
Get versioning information for CD pipeline of the project in JSON format.

Gets the following information in JSON format:
- if version is new (isVersionNew key).
- the version (version key).
- the text for the release (releaseBody key).

This information is used by the Continuous Delivery pipeline of the project to
automatically create a tag and release for the project, or, add latest changes
to Release Notes (changelog) in the documentation.

"""

import json
from pathlib import Path

from cly import __version__
from cly.utils import get_standard_output

previous_version = get_standard_output("git describe --tag --abbrev=0") or [""]


def get_release_body() -> str:
    """
    Get text for GitHub Release.

    Gets text between new version and previous version from docs/changelog.rst
    file.

    Returns
    -------
    str
        Text between new version and previous version.

    """
    text = ""
    append = False
    with open(
        Path(__file__).parent.parent / "docs/changelog.rst",
        encoding="utf-8",
    ) as changelog:
        for line in changelog:
            if line.strip() == previous_version[0]:
                break
            if line.strip() == __version__:
                append = True
            if append:
                text += line

    if not text:
        print("No release body provided")
        raise SystemExit(1)

    return text


versioning = {
    "isVersionNew": previous_version[0] != __version__,
    "version": __version__,
    "releaseBody": get_release_body(),
}
print(json.dumps(versioning))
