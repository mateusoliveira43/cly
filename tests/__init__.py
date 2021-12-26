"""
Add scripts folder to PYTHONPATH.

See module unit.cli.test_config for unit tests of module scripts.cli.config.
See module unit.cli.test_utils for unit tests of module scripts.cli.utils.
See module unit.example.test_command1 for unit tests of module
scripts.example.command1.
See module unit.example.test_main for unit tests of module
scripts.example.main.
See module integration.test_example for integration tests of module
scripts.example.

Misc variables:

    ABSOLUTE_PATH
    TODO ver o q vai ter de duplicidade e add aki

"""

import sys
from pathlib import Path

ABSOLUTE_PATH = Path(__file__).resolve().parent.parent / 'scripts'
if ABSOLUTE_PATH.exists():
    sys.path.append(ABSOLUTE_PATH.as_posix())
else:
    raise FileNotFoundError(f'ERROR: {ABSOLUTE_PATH} is not a valid path.')
