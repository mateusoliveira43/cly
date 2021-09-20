def command2(example: str = None, verbose: int = None, **kwargs):
    print('COMMAND 1!!!')
    if example:
        print('EXAMPLE', example)
    if verbose:
        print('VERBOSE', verbose)
