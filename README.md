# Python script template

- [Arquivo README em português](README_PT.md)

Template to create Python scripts.

## Tasks

- [ ] Option to edit and translate error messages as well.
- [ ] Add more quality measures to code and CI pipeline.
- [ ] Remove docstring rule for tests files.
- [ ] Add poetry to template.

# About the Template

In the project's folder, run with your machine Python 3 command
```
[python|python3] ./script_name
[python|python3] ./script_name -h
[python|python3] ./script_name --help
```
to display the script's help message.

Run the script with Python 3 command is optional. You can run the script with
```
./script_name/__main__.py
```

If you do not have permission to run it in your Linux's system, run
```
chmod +x script.py
```
to grant run permission to the file.

- To change **script name**, change line 11 of `/script_name/__main__.py`.
- To change **description** message, change line 12 of `/script_name/__main__.py`.
- To change **usage** title, change line 4 of `/script_name/config.py`.
- To change **epilog** message, change line 5 of `/script_name/config.py`.
- To change **required options** title, change line 6 of `/script_name/config.py`.
- To change **options** title, change line 7 of `/script_name/config.py`.

To disable showing the **help** message when running the script without arguments, remove arguments from function in line 126 of `/script_name/__main__.py`.

Begin script's logic at function `main` (line 77) of `/script_name/__main__.py`.

# Quality

To run the template quality measures, it is needed to install the requirements. To install then, run
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The quality measures of the template are reproduced by the continuos integration (CI) pipeline of the project, as described in `.github/workflows/ci.yml`.

## Tests

To run tests and coverage report, run
```
pytest
```

To see the html report, check `tests/coverage-results/htmlcov/index.html`.

## Linter

To run linter, run
```
prospector .
```

# License

This repository is licensed under the terms of [MIT License](LICENSE).
