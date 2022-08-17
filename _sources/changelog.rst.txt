Changelog
=========

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
