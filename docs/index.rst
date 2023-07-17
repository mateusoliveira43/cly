Welcome to CLY?!'s documentation!
=================================

**Build CLIs without dependencies!**

A framework to create Command Line Interface (CLI) with Python, using only
Python standard libraries, like `argparse <https://docs.python.org/3/library/argparse.html>`_.

Check the project's source code `here <https://github.com/mateusoliveira43/cly/>`_.

Requirements
------------

To use the framework, it is necessary the following tools:

- `Python <https://wiki.python.org/moin/BeginnersGuide/Download>`_
  3.7 or higher

Usage
-----

To use **CLY?!** in your project, in your project's root, run::

   curl -fsSL https://raw.githubusercontent.com/mateusoliveira43/cly/main/install_cly.py | python -

This will copy **CLY?!** (latest version) files to the ``scripts`` folder of your project.

To install (or update) a specific version of **CLY?!**, run::

   curl -fsSL https://raw.githubusercontent.com/mateusoliveira43/cly/main/install_cly.py | python - <version>

Where version is one of `these <https://github.com/mateusoliveira43/cly/tags>`_.

Name
----

The name of the package is a little joke. If you read each letter instead of reading
the word, the **Y** sounds like **WHY**. Why should you use this framework? That
is the reason it has a question mark in the name (and the question I try to
answer in the next section). And it also has a exclamation mark as a reply to
it, now the **Y** taking the role as **.py** file extension.

In other words, the name of the package is **"Why should I use this framework
to build CLIs? Because It is written in Python!"**.

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

**CLY?!**'s goal is to improve productivity when writing new CLI scripts using
Python's standard library `argparse <https://docs.python.org/3/library/argparse.html>`_.
This is done by automatically creating a subparser, if it do not already exists,
when a command is created, reusing the parser configuration into the subparser
configuration (the commands) and parsing the commands' docstring to get help for
it and it's options.

.. toctree::
   :maxdepth: 2
   :hidden:

   example.rst
   contributing.rst
   changelog.rst
   modules/modules.rst
