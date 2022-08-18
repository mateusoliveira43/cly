from pathlib import Path

import pytest
import toml

import cly
from tests import ABSOLUTE_PATH

VERSION_LABELS = cly.__version__.split(".", maxsplit=2)


def read_variable_from_file(variable_name: str, file_path: Path) -> str:
    """
    Read a variable from a file.

    Parameters
    ----------
    variable_name : str
        Name of the variable in the file.
    file_path : Path
        Path of the file to be read.

    Returns
    -------
    str
        Variable value, if it exists in the file; empty string otherwise.

    """
    with open(file_path, mode="r", encoding="utf-8") as file:
        for line in file:
            if line.strip().startswith(variable_name):
                return line.strip().split("=", maxsplit=1)[1].strip()
        return ""


def test_pyproject_version() -> None:
    """
    Test if project's versions are the same.
    GIVEN `pyproject.toml:version` and `cli.__version__`
    WHEN compared
    THEN they should be the same
    """
    with open(
        Path(cly.__file__).resolve().parents[1] / "pyproject.toml",
        encoding="utf-8",
    ) as pyproject_file:
        pyproject = toml.loads(pyproject_file.read())

    pyproject_version = pyproject["tool"]["poetry"]["version"]

    assert cly.__version__ == pyproject_version


def test_sonar_version() -> None:
    assert cly.__version__ == read_variable_from_file(
        "sonar.projectVersion", ABSOLUTE_PATH / "sonar-project.properties"
    )


@pytest.mark.parametrize(
    "label", VERSION_LABELS, ids=["major", "minor", "patch"]
)
def test_version_format(label: str) -> None:
    """
    Test if project's version is in the correct format.
    GIVEN one of `cli.__version__` labels
    WHEN checked it's characters
    THEN they should be digits
    Parameters
    ----------
    label : str
        One of the labels of the project's version.
    """
    assert label.isdigit()
