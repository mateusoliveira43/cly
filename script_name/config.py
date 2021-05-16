import argparse

script_name = 'script name'

__version__ = '1.0.0'

usage_prefix = 'Usage: [python|python3] '
script_description = 'Script description.'
script_epilog = 'Script epilog.'
positionals_title = 'Required options'
optionals_title = 'Options'
help_message = f'Shows {script_name} help message.'
version_message = f'Shows {script_name} version.'
version = f'{script_name} version {__version__}'


def get_command_help_messsage(command: str) -> str:
    """Gets the help message for a command.

    Parameters
    ----------
    command : str
       Name of the command.

    Returns
    -------
    str
        Command's help message.
    """
    return f'Shows {script_name} {command} command help message.'


class CustomFormatter(argparse.HelpFormatter):
    """Custom formatter for argparse's argument parser.

    Methods
    -------
    _format_usage(self, usage, actions, groups, prefix)
        Formats prefix of usage section.
    _format_action(self, action)
        Removes subparser's metavar when listing its parsers.
    """
    def __init__(self, *args, **kwargs):
        super(CustomFormatter, self).__init__(*args, **kwargs)

    def _format_usage(self, usage, actions, groups, prefix):
        return super(CustomFormatter, self)._format_usage(
            usage, actions, groups, usage_prefix)

    def _format_action(self, action):
        parts = super(CustomFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = '\n'.join(parts.split('\n')[1:])
        return parts
