# Python script template

- [Arquivo README em português](README_PT.md)

Template to create Python scripts.

## Tasks

- [ ] Option to translate error messages as well.

# About the Template

In the project's folder, run
```
[python3] ./script.py
[python3] ./script.py -h
[python3] ./script.py --help
```
to display the script's help message.

Run the script with Python 3 command is optional. If you do not have permission to run it in your Linux's system, run
```
chmod +x script.py
```
to grant run permission to the file.

- To change **usage** title, change line 15 of `script.py`.
- To change **script name**, change line 84 of `script.py`.
- To change **usage** message, change line 86 of `script.py`.
- To change **description** message, change line 87 of `script.py`.
- To change **epilog** message, change line 88 of `script.py`.
- To change **required options** title, change line 92 of `script.py`.
- To change **options** title, change line 93 of `script.py`.
- To change **help** message, change line 94 of `script.py`.

Follow **Required options**, **Options** and **Commands** examples to create script's required options, options and commands.

To disable showing the **help** message when running the script without arguments, remove arguments from function in line 130 of `script.py`.

Begin script's logic at line 132 of `script.py`.

# License

This repository is licensed under the terms of [MIT License](LICENSE).
