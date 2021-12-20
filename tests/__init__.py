import sys
from pathlib import Path

HELP_FLAGS = ['-h', '--help']
VERSION_FLAGS = ['-v', '--version']
OPTIONAL_FLAGS = ['-o', '--optional']
INVALID_FLAGS = ['-k', '--invalid']

USAGE = 'Usage:\n  [python|python3] file_name'  # TODO add full message

UNRECOGNIZED_ARGUMENTS = 'error: unrecognized arguments'
INVALID_CHOICE = 'invalid choice'
INVALID_INT_VALUE = 'invalid int value'

ABSOLUTE_PATH = Path(__file__).resolve().parent.parent / 'scripts'
if ABSOLUTE_PATH.exists():
    sys.path.append(ABSOLUTE_PATH.as_posix())
else:
    raise FileNotFoundError(f'ERROR: {ABSOLUTE_PATH} is not a valid path.')
