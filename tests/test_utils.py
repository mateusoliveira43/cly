from script_name.utils import parse_arguments


def test_parse_arguments():
    TEST_DATA = [
        {'input': ['the', 'dark', 'knight'], 'output': 'the dark knight'},
        {'input': ['-r', 'command', '-v', '1'], 'output': '-r command -v 1'},
    ]
    for scenario in TEST_DATA:
        output = parse_arguments(scenario['input'])
        assert output == scenario['output']
