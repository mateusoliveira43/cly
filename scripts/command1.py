# pylint:disable=unused-argument
def command1(text: str = None, number: int = None, **kwargs):
    """Print example command."""
    print('Command 1 called.')
    if isinstance(text, str):
        print(f'Text argument called with {text}.')
    if isinstance(number, int):
        print(f'Number argument called with {number}.')
