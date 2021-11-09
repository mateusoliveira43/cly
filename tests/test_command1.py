from scripts.command1 import command1


def test_command1_without_options(capsys):
    """Test command1 without options."""
    command1()
    output, error = capsys.readouterr()
    assert not error
    assert output == 'Command 1 called.\n'


def test_command1_with_text(capsys):
    """Test command1 with text."""
    command1(text='text')
    output, error = capsys.readouterr()
    assert not error
    assert 'Text argument called with text.\n' in output


def test_command1_with_number(capsys):
    """Test command1 with number."""
    command1(number=1)
    output, error = capsys.readouterr()
    assert not error
    assert 'Number argument called with 1.\n' in output
