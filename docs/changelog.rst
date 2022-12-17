Changelog
=========

Latest Changes
--------------

- fix: jinja template line break. PR `#74 <https://github.com/mateusoliveira43/cly/pull/74>`_ by `@mateusoliveira43 <https://github.com/mateusoliveira43>`_.\n- fix: Remove type ignore comments from code. PR `#73 <https://github.com/mateusoliveira43/cly/pull/73>`_ by `@mateusoliveira43 <https://github.com/mateusoliveira43>`_.
- fix: CD versioning pipeline permission. PR `#72 <https://github.com/mateusoliveira43/cly/pull/72>`_ by `@mateusoliveira43 <https://github.com/mateusoliveira43>`_.

1.1.2
-----

In this version:

- Fix shell functions that print output in run time by using `subprocess.run` again.

1.1.1
-----

In this version:

- `installation script <https://github.com/mateusoliveira43/cly/blob/main/install_cly.py>`_ for CLY?!.
- Shell functions now accept a directory argument, to run commands in the
  directory the user wants.
- :py:func:`cly.utils.run_multiple_commands`: function to run multiple shell commands at once.
- Long help messages are broken in the CLI's help and only completely appear in
  the commands help.
- :py:func:`cly.testing.run_cli`: CLY?! now provides a test environment for the users.

1.0.1
-----

In this version:

- Fixing imports in cli package: using relative imports both for performance and
  for not breaking package use.
- Change cli package name to **cly** (this should be a major change, but since
  this is not a Python package that you will download, just copy, I am considering
  it a patch change).
- Change repository name to **cly**.
- Add name explanation to documentation.

1.0.0
-----

**First version of the template!**

In this version:

- Shell output formatting functions like coloring and underling.
- Docstring automation for commands help and it's options.
- Shell manipulation functions.
- Custom help formatter for argparse.
- Automated argparse wrapper.

For next versions, I want to:

- Create a testing environment, to facilitate testing CLIs built with the
  template.
- Further automate the template, like adding options to the subparser and the
  parser by parsing the commands' docstring.
- If only one command is added to ConfiguredParser, do not create a subparser.
