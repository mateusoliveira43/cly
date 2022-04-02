# Python CLI script template

[![Continuos Integration](https://github.com/mateusoliveira43/python-cli-script-template/actions/workflows/ci.yml/badge.svg)](https://github.com/mateusoliveira43/python-cli-script-template/actions)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=mateusoliveira43_python-cli-script-template&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=mateusoliveira43_python-cli-script-template)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

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

To run the template quality measures, it is needed to install its development requirements. To install then, run
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
```
or
```
poetry install --no-root
poetry shell
```

The quality measures of the template are reproduced by the continuos integration (CI) pipeline of the project. CI configuration in `.github/workflows/ci.yml` file.

## Tests

To run tests and coverage report, run
```
pytest
```

To see the html report, check `tests/coverage-results/htmlcov/index.html`.

Tests and coverage configuration in `pyproject.toml` file.

## Linter

To run Python linter, run
```
prospector .
```

Python linter configuration in `.prospector.yaml` file.

## Code formatters

To format imports, run
```
isort .
```

isort configuration in `pyproject.toml` file.

To check all repository's files format, run
```
ec -v
```

File format configuration in `.editorconfig` file.

## Security vulnerability scanners

To check common security issues in source code, run
```
bandit -r scripts
```

To check known security vulnerabilities in installed dependencies, run
```
safety check -r requirements/dev.txt --full-report
```

## SonarCloud Code Analysis

TODO add sonar lint config to wiki

[SonarCloud](https://sonarcloud.io/) analyzes the source code of the project through the CI pipeline.

## Pre-commit

To configure pre-commit automatically when cloning the repo, run
```
pip install pre-commit
git config --global init.templateDir ~/.git-template
pre-commit init-templatedir --hook-type commit-msg ~/.git-template
```
Must be installed globally. More information in https://pre-commit.com/#automatically-enabling-pre-commit-on-repositories

To configure pre-commit locally, run
```
pip install pre-commit
pre-commit install --hook-type commit-msg
```
with your virtual environment active.

To test it, run
```
pre-commit run --all-files
```

# License

This repository is licensed under the terms of [MIT License](LICENSE).
