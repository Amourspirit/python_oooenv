# OOOENV

This project is strictly for LibreOffice python projects that need to set UNO environment.

A project as [OOO Development Tools](https://python-ooo-dev-tools.readthedocs.io/en/latest/index.html) would use this project

See also:

- [LibreOffice Virtual Environment Guides](https://python-ooo-dev-tools.readthedocs.io/en/latest/guide/virtual_env/index.html)
- [OOO Development Tools - Develop Docs](https://python-ooo-dev-tools.readthedocs.io/en/latest/dev_docs/dev_notes.html)
- [LibreOffice Python Script Modern Code Editor Examples](https://github.com/Amourspirit/libreoffice-modern-code-editing-py)

## Installation

**oooenv** [PyPI](https://pypi.org/project/oooenv)

```shell
pip install oooenv
```

## Usage

View command options

```shell
oooenv -h
```

### Linux/Mac

In Linux and Mac all that is needed to run a project that requires LibreOffice UNO
is to link the UNO files into virtual environment.

To add UNO links to virtual environment run command:

```shell
oooenv cmd-link -a
```

To remove UNO links from virtual environment run command:

```shell
oooenv cmd-link -r
```

### Windows

Windows python projects cannot use linking to UNO Files.

In Windows the virtual environment configuration file is manipulated.

The Follow command toggles between original configuration and UNO environment configuration.

```powershell
oooenv env -t
```

To update the configuration to match the installed version of LibreOffice's python.

This command should not be run until `oooenv env -t` has be run at least once.

```powershell
oooenv update --update
```

If virtual environment is managed by Poetry then it will be necessary to toggle into original config before running `poetry update`.

When updates are done just run command again to toggle back to UNO environment configuration.

## Environment Variables

Special environment variables can be set. These are completely optional.
This can be useful for docker containers.

- `OOOENV_LO_UNO_PATH` The path where `uno.py` is located.
- `OOOENV_LO_PROGRAM_PATH` The path to LibreOffice such as `C:\Program Files\LibreOffice\program` or `/usr/lib/libreoffice/program`.
- `OOOENV_LO_PROGRAM_PATH` The path to LibreOffice installed directory, such as `C:\Program Files\LibreOffice` or `/usr/lib/libreoffice`.
- `OOOENV_LO_PY_EXE` The path to LibreOffice Python. On Windows this is usually `C:\Program Files\LibreOffice\program\python.exe` and Linux is usually the virtual environment's python.
- `OOOENV_VIRTUAL_ENV` The path containing the virtual environment for your project. Usually this is `venv` or `.venv`.`
- `OOOENV_SITE_PACKAGES` The site packages directory of the virtual environment for your project.
