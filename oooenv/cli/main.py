#!/usr/bin/env python
# coding: utf-8
from __future__ import annotations
import importlib.metadata
import argparse
import sys
import os
from pathlib import Path
from oooenv.cmds import uno_lnk, manage_env_cfg, updater
from oooenv.utils import local_paths

# region parser

# region        Create Parsers


def _create_parser(name: str) -> argparse.ArgumentParser:
    return argparse.ArgumentParser(description=name)


# endregion     Create Parsers

# region Process Sub Commands


def _args_process_cmd(a_parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.command == "cmd-link":
        _args_action_cmd_link(a_parser=a_parser, args=args)
    elif args.command == "env":
        _args_action_cmd_toggle_env(a_parser=a_parser, args=args)
    elif args.command == "info" and sys.platform == "win32":
        _args_action_cmd_info_win(a_parser=a_parser, args=args)
    elif args.command == "update" and sys.platform == "win32":
        _args_action_cmd_update(a_parser=a_parser, args=args)
    else:
        a_parser.print_help()


# endregion Process Sub Commands


# region command link
def _args_cmd_link(parser: argparse.ArgumentParser) -> None:
    add_grp = parser.add_argument_group()
    add_grp.add_argument(
        "-a",
        "--add",
        help="Add uno links to virtual environment.",
        action="store_true",
        dest="add",
        default=False,
    )

    add_grp.add_argument(
        "-s",
        "--uno-src",
        help="Optional source directory that contains uno.py and unohelper.py. If ommited then defaults are used.",
        action="store",
        dest="src_dir",
        default=None,
    )
    parser.add_argument(
        "-r",
        "--remove",
        help="Remove uno links to virtual environment.",
        action="store_true",
        dest="remove",
        default=False,
    )


def _args_action_cmd_link(a_parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if not (args.add or args.remove):
        a_parser.error("No action requested, add --add or --remove")
    if args.add:
        uno_lnk.add_links(args.src_dir)
    elif args.remove:
        uno_lnk.remove_links()


# endregion command link

# region process env commands


def _args_cmd_toggle_evn(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-t",
        "--toggle-env",
        help="Toggle virtual environment to and from LibreOffice environment",
        action="store_true",
        dest="toggle_env",
        default=False,
    )
    parser.add_argument(
        "-u",
        "--uno-env",
        help="Displays if the current Virtual Environment is UNO Environment.",
        action="store_true",
        dest="uno_env",
        default=False,
    )
    parser.add_argument(
        "-c",
        "--custom-env",
        help="Set a custom environment. cfg file must exist and be manually configured. Value is suffix of cfg file. For example: -c myenv will use pyenv_myenv.cfg",
        action="store",
        dest="custom_env",
        required=False,
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Displays the current version of LiberOffice Python. This is parsed from LibreOffice Python executable.",
        action="store_true",
        dest="lo_py_version",
        default=False,
    )


def _args_action_cmd_toggle_env(a_parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.uno_env:
        if manage_env_cfg.is_env_uno_python():
            print("UNO Environment")
        else:
            print("NOT a UNO Environment")
        return

    if args.toggle_env:
        manage_env_cfg.toggle_cfg()
        return
    if args.custom_env:
        manage_env_cfg.toggle_cfg(suffix=args.custom_env)
        return


# endregion process env commands


# region command update
def _args_cmd_update(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-c",
        "--is-current",
        help="Check if the uno cfg is up to date.",
        action="store_true",
        dest="uno_up_to_date",
        default=False,
    )
    parser.add_argument(
        "-u",
        "--update",
        help="Updates the uno cfg file.",
        action="store_true",
        dest="cfg_update",
        default=False,
    )


def _args_action_cmd_update(a_parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.uno_up_to_date:
        if updater.needs_updating():
            print("Update Needed")
        else:
            print("No Update Needed")
        return

    if args.cfg_update:
        if not updater.needs_updating():
            print("No Update Needed")
            return
        updater.update_cfg()
        if manage_env_cfg.is_env_uno_python():
            # if we are in a uno environment then we need to reload the cfg
            cfg = manage_env_cfg.read_pyvenv_cfg(fnm="pyvenv_uno.cfg")
            manage_env_cfg.save_config(cfg=cfg)

        print("Update Complete")
        return


# endregion command update


# region Info Windows
def _args_cmd_info_win(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-v",
        "--version",
        help="Displays the current version of LiberOffice Python. This is parsed from LibreOffice Python executable.",
        action="store_true",
        dest="lo_py_version",
        default=False,
    )


def _args_action_cmd_info_win(a_parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    if args.lo_py_version:
        ver = manage_env_cfg.get_uno_python_ver()
        print(ver)
        return


# endregion Info Windows


# region process arg command for global
def _args_cmd_global(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "-v",
        "--version",
        help="Show the current version of oooenv.",
        action="store_true",
        dest="show_version",
        default=False,
    )


def _args_action_global(a_parser: argparse.ArgumentParser, args: argparse.Namespace) -> str | None:
    # sourcery skip: assign-if-exp, reintroduce-else
    if args.show_version:
        # return importlib.metadata.version(__package__ or __name__)
        return importlib.metadata.version("oooenv")
    return None


# endregion process arg command for global

# endregion parser


def main() -> int:
    os.environ["project_root"] = str(Path(__file__).parent)
    os.environ["env-site-packages"] = str(local_paths.get_site_packages_dir())
    parser = _create_parser("main")
    subparser = parser.add_subparsers(dest="command")

    # region Global
    _args_cmd_global(parser=parser)
    # endregion Global

    # region OS Specific Commands
    if os.name != "nt":
        # linking is not useful in Windows.
        cmd_link = subparser.add_parser(
            name="cmd-link",
            help="Add/Remove links in virtual environments to uno files.",
        )
        _args_cmd_link(parser=cmd_link)

    if sys.platform == "win32":
        _add_windows_sub_parsers(subparser)
    # endregion OS Specific Commands

    # region Read Args
    args = parser.parse_args()
    if global_action := _args_action_global(a_parser=parser, args=args):
        print(global_action)
        return 0
    # endregion Read Args

    _args_process_cmd(a_parser=parser, args=args)
    return 0


def _add_windows_sub_parsers(subparser):
    cmd_env_toggle = subparser.add_parser(
        name="env",
        help="Manage Virtual Environment configuration.",
    )
    _args_cmd_toggle_evn(parser=cmd_env_toggle)
    cmd_win_info = subparser.add_parser(
        name="info",
        help="LibreOffice information.",
    )
    _args_cmd_info_win(parser=cmd_win_info)
    cmd_win_update = subparser.add_parser(
        name="update",
        help="Manage updating of cfg files.",
    )
    _args_cmd_update(parser=cmd_win_update)


if __name__ == "__main__":
    raise SystemExit(main())
