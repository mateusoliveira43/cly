# Python CLI script template

[![Continuos Integration](https://github.com/mateusoliveira43/python-cli-script-template/actions/workflows/ci.yml/badge.svg)](https://github.com/mateusoliveira43/python-cli-script-template/actions)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=mateusoliveira43_python-cli-script-template)](https://sonarcloud.io/summary/new_code?id=mateusoliveira43_python-cli-script-template)

- [Arquivo README em português](docs/README_PT.md)

Template to create Python command line interface scripts, using Python's standard library [argparse](https://docs.python.org/3/library/argparse.html).

Check the repository [Wiki](https://github.com/mateusoliveira43/python-cli-script-template/wiki) for more details.

# Example of use

In the scripts folder, the `example` Python package and `run_example` Python module are example of use of the template.

To run the example, run
```
[python|python3] scripts/run_example.py
[python|python3] scripts/run_example.py -h
[python|python3] scripts/run_example.py --help
```
to display the example script's help message. Run the script with Python 3 command is optional.

# Quality

To run the template quality measures, it is needed to install its requirements. To install then, run
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

## Code formatters

To format imports, run
```
isort -vm 3 --tc --gitignore .
```

## Security vulnerability scanners

To check common security issues in source code, run
```
bandit -r scripts
```

To check known security vulnerabilities in installed dependencies, run
```
safety check
```

## Sonarqube

TODO add sonar lint config to wiki

# License

This repository is licensed under the terms of [MIT License](LICENSE).
