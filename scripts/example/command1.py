"""Create command example."""


def command1(**kwargs):
    """Print example command."""
    print('Command 1 called.')
    if isinstance(kwargs.get('text'), str):
        print(f'Text argument called with {kwargs["text"]}.')
    if isinstance(kwargs.get('number'), int):
        print(f'Number argument called with {kwargs["number"]}.')
