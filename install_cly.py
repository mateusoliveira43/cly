#!/usr/bin/env python3
"""
Install CLY?! package to project.

Install/update CLY?! latest version or pass version to script (in the format
major.minor.patch), to install/update specific version.

"""

import shutil
import subprocess  # nosec
import sys
from pathlib import Path

PROJECT_ROOT: Path = Path(__file__).resolve().parent
CLY: str = "git@github.com:mateusoliveira43/cly.git"
SOURCE: Path = PROJECT_ROOT / "cly/cly"


def get_cly() -> str:
    """
    Get CLY?!'s source code.

    Returns
    -------
    str
        Command to clone CLY?!'s Git repository.

    """
    try:
        return f"git clone --branch {sys.argv[1]} {CLY}"
    except IndexError:
        return f"git clone {CLY}"


def copy_files_to_scripts(folder: Path) -> None:
    """
    Copy package to the project's scripts folder.

    Files with the same name are overwritten.

    Parameters
    ----------
    folder : Path
        Folder or file to be copied.

    """
    for file in folder.glob("*"):
        if file.is_dir():
            copy_files_to_scripts(file)
        else:
            destination = (
                PROJECT_ROOT / "scripts/cly" / file.relative_to(SOURCE)
            )
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(src=file, dst=destination)


subprocess.run(get_cly(), shell=True, check=True, encoding="utf-8")  # nosec
copy_files_to_scripts(SOURCE)
shutil.rmtree(PROJECT_ROOT / "cly")
