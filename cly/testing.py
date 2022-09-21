"""Testing environment for CLY?! object."""

import sys
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from typing import List, Tuple
from unittest.mock import patch

from .config import ConfiguredParser


def run_cli(cli: ConfiguredParser, arguments: List[str]) -> Tuple[int, str]:
    """
    Run CLY?! object with desired arguments and capturing output.

    Parameters
    ----------
    cli : ConfiguredParser
        CLY?! object.
    arguments : List[str]
        Arguments to pass to CLY?! object.

    Returns
    -------
    Tuple[int, str]
        Exit code from CLI?! object execution and it's output.

    """
    try:
        with patch.object(sys, "argv", ["file_name", *arguments]):
            output = StringIO()
            with redirect_stdout(output):
                with redirect_stderr(output):
                    cli()
            return 0, output.getvalue()
    except SystemExit as sys_exit:  # NOSONAR
        return sys_exit.code, output.getvalue()
