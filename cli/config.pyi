import argparse
from typing import Any, Dict, List

from _typeshed import Incomplete

from cli.colors import color_text as color_text

USAGE_PREFIX: str
POSITIONALS_TITLE: str
OPTIONALS_TITLE: str
HELP_MESSAGE: str
VERSION_MESSAGE: str
MAJOR_VERSION: int
MINOR_VERSION: int
PYTHON_MINIMUM_VERSION: Incomplete

def check_python_minimum_version() -> None: ...
def get_version(name: str, version: str) -> str: ...
def get_command_help_message(command: str) -> str: ...
def initialize_parser(add_help: bool = ...) -> List[str]: ...

class CustomFormatter(argparse.HelpFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...

class ConfiguredParser:
    name: Incomplete
    description: Incomplete
    epilog: Incomplete
    version: Incomplete
    add_help: Incomplete
    parser: Incomplete
    subparser: Incomplete
    def __init__(
        self, config: Dict[str, str], add_help: bool = ...
    ) -> None: ...
    def create_parser(self) -> argparse.ArgumentParser: ...
    def create_subparser(
        self,
    ) -> argparse._SubParsersAction: ...  # type: ignore
    def create_command(
        self, name: str, help_message: str
    ) -> argparse.ArgumentParser: ...
    def get_arguments(self) -> argparse.Namespace: ...
