# Python script template

- [Arquivo README em português](README_PT.md)

Template to create Python scripts.

## Tasks

- [ ] Option to edit and translate error messages as well.
- [ ] Add linter and quality measures to code.

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

- To change **script name**, change line 3 of `/script_name/config.py`.
- To change **usage** title, change line 7 of `/script_name/config.py`.
- To change **description** message, change line 8 of `/script_name/config.py`.
- To change **epilog** message, change line 9 of `/script_name/config.py`.
- To change **required options** title, change line 10 of `/script_name/config.py`.
- To change **options** title, change line 11 of `/script_name/config.py`.
- To change **help** message, change line 12 of `/script_name/config.py`.

Follow **Required options**, **Options** and **Commands** examples to create script's required options, options and commands.

To disable showing the **help** message when running the script without arguments, remove arguments from function in line 126 of `/script_name/__main__.py`.

Begin script's logic at line 127 of `/script_name/__main__.py`.

# Tests

To run the template tests, it is needed to install the testing tools. To install then, run
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

To run tests, run
```
pytest
```

# License

This repository is licensed under the terms of [MIT License](LICENSE).
