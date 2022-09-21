"""Configuration file for Sphinx."""

# -- Path setup --------------------------------------------------------------

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1].as_posix()

sys.path.append(PROJECT_ROOT)


# -- Project information -----------------------------------------------------

project = "CLY?!"
copyright = "2022, Mateus Oliveira"
author = "Mateus Oliveira"


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx_rtd_theme",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
]
nitpick_ignore = [
    ("py:class", "argparse.Action"),
    ("py:class", "argparse.ArgumentParser"),
    ("py:class", "argparse.HelpFormatter"),
    ("py:class", "argparse.Namespace"),
    ("py:class", "argparse._ArgumentGroup"),
    ("py:class", "argparse._SubParsersAction"),
    ("py:class", "pathlib.Path"),
    ("py:class", "subprocess.CompletedProcess"),
    ("py:class", "subprocess.Popen"),
]


# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
