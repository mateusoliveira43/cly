Changelog
=========

1.1.1
-----

In this version:

- TODO


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
