"""Add scripts folder to PYTHONPATH for pytest."""

import sys
from pathlib import Path

# TODO melhorar testes ainda, deixar tudo temático

ABSOLUTE_PATH = Path(__file__).resolve().parent.parent / 'scripts'
if ABSOLUTE_PATH.exists():
    sys.path.append(ABSOLUTE_PATH.as_posix())
else:
    raise FileNotFoundError(f'ERROR: {ABSOLUTE_PATH} is not a valid path.')
