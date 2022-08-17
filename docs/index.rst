Welcome to Python CLI script template's documentation!
======================================================

Python Command Line Interface (CLI) script template using Python standard
library `argparse <https://docs.python.org/3/library/argparse.html>`_. Build
CLIs without dependencies!

Motivation
----------

I like to build CLIs for automation and avoid writing long instructions in the
shell. One example would be a initialization script for a python project.
Instead of running ``virtualenv .venv``, then ``source .venv/bin/activate`` and
finally ``pip install requirements.txt`` before running the project commands,
you could put the instructions on a shell script (do not forget to run it with
``source``) and run the script instead of three commands.

For simple tasks, like the previous example, a ``bash`` script can save the
day, but as the script gets bigger and needs more features, maintain and read
it becomes a hard work. That is why I like to write them in Python. And because
I like to write scripts that could probably run before the project's
dependencies are installed, I want them to have no dependencies (only Python
standard libraries). But if that is not a problem to you, you probably should
use a more robust solution, like `typer <https://github.com/tiangolo/typer>`_.

The goal of this template is to improve productivity when writing new CLI
scripts using Python's standard library `argparse
<https://docs.python.org/3/library/argparse.html>`_. This is done by
automatically creating a subparser, if it do not already exists, when a command
is created, reusing the parser configuration into the subparser configuration
(the commands) and parsing the commands' docstring to get help for it and it's
options.

.. toctree::
   :maxdepth: 2
   :hidden:

   example.rst
   changelog.rst
   modules/modules.rst
