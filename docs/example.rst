Example of use
==============

The `batcomputer_cli folder
<https://github.com/mateusoliveira43/cly/tree/main/tests/batcomputer_cli>`_
and the `batcomputer.py
<https://github.com/mateusoliveira43/cly/blob/main/tests/batcomputer.py>`_
file are an example of use of the framework, with a Batman Theme.

To display the example script's help, run::

    [python|python3] tests/batcomputer.py

or::

    [python|python3] tests/batcomputer.py -h

or::

    [python|python3] tests/batcomputer.py --help

Run the script with Python 3 command is optional.

Another examples of use of the framework:

- `Docky <https://github.com/mateusoliveira43/docky>`_: Run Docker commands
  with Python.
- `Dev <https://github.com/mateusoliveira43/python-project-template/tree/main/scripts/dev_cli>`_:
  Development scripts to run less and shorter development related commands.

How to use
----------

The idea of use of this framework is to copy the :py:mod:`cly` package to
your project and use it. A suggestion would be to have a ``scripts`` folder
and stores your scripts like this::

    scripts/
    ├── cly/
    ├── script_name_cli/
    └── script_name.py

Then, to call it, you would run ``scripts/script_name.py``.

Do not forget that to run a Python script without the Python3 command, it is
needed to add a **shebang**, at the beginning of the file, and grant run
permission to it. An example of Python shebang::

    #!/usr/bin/env python3

To grant run permission to a file in your Linux's system, run::

    chmod +x file_name

You can also add the CLI to your project scripts. For example, in your
``pyproject.toml``, you can add something like::

    [tool.poetry.scripts]
    script_name = "scripts.script_name_cli.__main__:CLI"

Then, you can call it with just ``script_name``, after installing the project.

Understanding the example
-------------------------

To understand what the framework does, let's check out how would be the example
implementation with pure argparse::

    import argparse
    import functools
    import sys
    from typing import Any, Callable

    from . import __version__
    from .commands.identify import identify
    from .commands.list_aliases import list_aliases


    def decorate_kwargs(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrap(**kwargs: Any) -> Any:
            for kwarg in set(kwargs.keys()) - set(func.__code__.co_varnames):
                kwargs.pop(kwarg)
            return func(**kwargs)

        return wrap


    COMMANDS = {
        "id": decorate_kwargs(identify),
        "ls": decorate_kwargs(list_aliases),
    }

    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description="Run Batcomputer analysis on selected areas.",
        epilog="Wayne Enterprises \N{office building}",
        allow_abbrev=False,
        # formatter_class=CustomFormatter, Defined in cly package
    )
    parser._positionals.title = "Arguments"
    parser._optionals.title = "Options"
    parser._actions[0].help = "Show script's help message."
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"Batcomputer version {__version__}",
        help="Show script's version.",
    )
    parser.add_argument(
        "-o",
        "--oracle",
        action="store_true",
        help="Use Oracle's help to get more data.",
    )

    subparser = parser.add_subparsers(
        dest="commands",
        metavar="command",
        title="Commands",
        prog=sys.argv[0],
        required=True,
    )

    identify_command = subparser.add_parser(
        "id",
        help="Identify the person behind each alias.",
    )
    identify_command.add_argument(
        dest="aliases",
        metavar="aliases",
        nargs="+",
        help="One or more alias to be identified, separated by spaces.",
    )

    subparser.add_parser(
        "ls",
        help="List all aliases in Batcomputer.",
    )


    def CLI() -> None:
        namespace = parser.parse_args(sys.argv[1:] or ["--help"])
        if namespace.commands:
            COMMANDS[namespace.commands](**dict(namespace._get_kwargs()))

You can copy this content into ``tests/batcomputer_cli/__main__.py`` and run the
example to check it out.

Now let's check the example further::

    from cly import config

    from . import __version__
    from .commands.identify import identify
    from .commands.list_aliases import list_aliases

    CLI_CONFIG = {
        "name": "Batcomputer",
        "description": "Run Batcomputer analysis on selected areas.",
        "epilog": "Wayne Enterprises \N{office building}",
        "version": __version__,
    }

    CLI = config.ConfiguredParser(CLI_CONFIG)
    CLI.parser.add_argument(
        "-o",
        "--oracle",
        action="store_true",
        help="Use Oracle's help to get more data.",
    )

    identify_command = CLI.create_command(identify, alias="id")
    identify_command.add_argument(dest="aliases", metavar="aliases", nargs="+")

    CLI.create_command(list_aliases, alias="ls")

When we call the ``ConfiguredParser`` class, it creates a
``argparse.ArgumentParser``, doing everything the parser calls do in the pure
argparse example, except adding the ``oracle`` argument.

When we call the ``create_command`` function, it creates a subparser, if one
does not already exists, and adds the command to it. If you notice, in the
pure argparse example, the parser configuration is lost in the subparser. This
does not happens with the framework, because it passes the same configurations
to the subparser. With **CLY?!**, you do not need to pass the help for the
commands' arguments, since it is parsed from the command's docstring.

Finally, **CLY?!** implements a ``__call__`` method for parsing the user
inputs. The pure argparse example have 77 lines of code, against 25 lines of code of
when using the framework.
