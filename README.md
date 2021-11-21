# Python script template

- [Arquivo README em português](docs/README_PT.md)

Template to create Python scripts.

## Tasks

- [ ] Option to edit and translate error messages as well.
- [ ] Add more quality measures to code and CI pipeline.
- [ ] Remove docstring rule for tests files.
- [ ] Add poetry to template.

# About the Template

In the project's folder, run with your machine Python 3 command
```
[python|python3] ./scripts
[python|python3] ./scripts -h
[python|python3] ./scripts --help
```
to display the script's help message.

Run the script with Python 3 command is optional. You can run the script with
```
./scripts/__main__.py
```

If you do not have permission to run it in your Linux's system, run
```
chmod +x ./scripts/__main__.py
```
to grant run permission to the file.

- To change **script name**, change line 11 of `/scripts/__main__.py`.
- To change **description** message, change line 12 of `/scripts/__main__.py`.
- To change **usage** title, change line 4 of `/scripts/config.py`.
- To change **epilog** message, change line 5 of `/scripts/config.py`.
- To change **required options** title, change line 6 of `/scripts/config.py`.
- To change **options** title, change line 7 of `/scripts/config.py`.

To disable showing the **help** message when running the script without arguments, remove `--help` argument from function in line 163 of `/scripts/config.py`.

Begin script's logic at function `main` (line 59) of `/scripts/__main__.py`.

# Quality

To run the template quality measures, it is needed to install the requirements. To install then, run
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The quality measures of the template are reproduced by the continuos integration (CI) pipeline of the project. CI configuration in `.github/workflows/ci.yml` file.

## Tests

To run tests and coverage report, run
```
pytest
```

To see the html report, check `tests/coverage-results/htmlcov/index.html`.

Tests and coverage configuration in `pytest.ini` file.

## Linter

To run linter, run
```
prospector .
```

Linter configuration in `.prospector.yml` file.

# License

This repository is licensed under the terms of [MIT License](LICENSE).
