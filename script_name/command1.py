def command1(example: str = None, verbose: int = None, **kwargs):
    print('COMMAND 1!!!')
    if example:
        print('EXAMPLE', example)
    if verbose:
        print('VERBOSE', verbose)
    print(kwargs)
    # TODO look argparse documentation for examples
    # https://docs.python.org/3/library/argparse.html#the-add-argument-method
