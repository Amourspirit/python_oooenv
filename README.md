# OOOENV

This project is strictly for LibreOffice python projects that need to set UNO environment.

A project as [OOO Development Tools](https://python-ooo-dev-tools.readthedocs.io/en/latest/index.html) would use this project

See also [OOO Development Tools - Develop Docs](https://python-ooo-dev-tools.readthedocs.io/en/latest/dev_docs/dev_notes.html)

## Usage

### Linux/Mac

In Linux and Mac all that is needed to run a project that requires LibreOffice UNO
is to link the UNO files into virtual environment.

To add UNO links to virtual environment run command:

```sh
oooenv cmd-link -a
```

To remove UNO links from virtual environment run command:

```sh
oooenv cmd-link -r
```

### Windows

Windows python projects cannot use linking to UNO Files.

In Windows the virtual environment configuration file is manipulated.

The Follow command toggles between original configuration and UNO environment configuration.

```ps
oooenv env -t
```

If virtual environment is managed by Poetry then it will be necessary to toggle into original config before running
`poetry update`.

When updates are done just run command again to toggle back to UNO environment configuration.
