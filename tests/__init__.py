import sys
import os

absolute_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../script_name')
)
sys.path.append(absolute_path)
