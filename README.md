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
