from __future__ import annotations
import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, NamedTuple, cast
from ..utils import local_paths

# from ..lib.connect import LoSocketStart
from ..utils import uno_paths


class Version(NamedTuple):
    major: int
    minor: int
    revision: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.revision}"


def get_uno_python_exe() -> str:
    """
    Gets Python Exe Path

    Raises:
        Exception: If not on Windows.
    """
    # sourcery skip: raise-specific-error
    if sys.platform != "win32":
        raise Exception("Method only support Windows")
    p = Path(uno_paths.get_soffice_install_path(), "program", "python.exe")
    return str(p)


def get_uno_python_ver() -> Version:
    """
    Gets Uno Python Version

    Raises: Exception if not on Windows.
    """
    python_exe = get_uno_python_exe()
    output = subprocess.check_output([python_exe, "--version"]).decode("UTF8").strip()
    # something like Python 3.8.10
    parts = output.split()
    major, minor, rev = parts[1].split(".")
    return Version(major=int(major), minor=int(minor), revision=int(rev))


def read_pyvenv_cfg(fnm: str = "pyvenv.cfg") -> Dict[str, str]:
    pyvenv_cfg = _get_pyvenv_cfg_path(fnm=fnm)
    result = {}
    with open(pyvenv_cfg, "r") as file:
        # strip of new line and remove anything after #
        # # for comment
        data = (row.partition("#")[0].rstrip() for row in file)
        # chain generator
        # remove empty lines
        data = (row for row in data if row)
        # each line should now be key value pairs separated by =
        for row in data:
            key, value = row.split("=")
            result[key.strip()] = value.strip()
    return result


def get_libreoffice_py_ver_from_cfg(fnm: str = "pyvenv_uno.cfg") -> Version:
    """
    Gets LibreOffice Python Version from passed in cfg file.

    Args:
        fnm (str, optional): Config to get version from. Defaults to "pyvenv_uno.cfg".

    Raises:
        ValueError: if version_info not found in cfg.

    Returns:
        Version: Version of LibreOffice Python found in cfg.
    """
    cfg = read_pyvenv_cfg(fnm=fnm)
    version_info = cast(str, cfg.get("version_info", ""))
    if not version_info:
        raise ValueError(f"version_info not found in {fnm}")
    major, minor, revision, _ = version_info.split(".", maxsplit=3)
    return Version(major=int(major), minor=int(minor), revision=int(revision))


def is_env_uno_python(cfg: dict | None = None) -> bool:
    if cfg is None:
        cfg = read_pyvenv_cfg()
    home = cfg.get("home", "")
    if not home:
        return False
    lo_path = _get_lo_path()
    return home.lower() == lo_path.lower()


def backup_cfg() -> None:
    src = _get_pyvenv_cfg_path()
    cfg = read_pyvenv_cfg()
    if is_env_uno_python(cfg):
        dst = src.parent / "pyvenv_uno.cfg"
    else:
        dst = src.parent / "pyvenv_orig.cfg"
    local_paths.copy_file(src=src, dst=dst)


def save_config(cfg: Dict[str, str], fnm: str = "pyvenv.cfg"):
    lst = [f"{k} = {v}" for k, v in cfg.items()]
    if lst:
        lst.append("")
    f_out = _get_venv_path() / fnm
    with open(f_out, "w") as file:
        file.write("\n".join(lst))
    print("Saved cfg")


def toggle_cfg(suffix: str = "") -> None:
    env_path = _get_venv_path()
    if suffix:
        src = env_path / f"pyvenv_{suffix.strip()}.cfg"
        if not src.exists():
            print('File not found: "{src}"')
            print("No action taken")
            return
        dst = env_path / "pyvenv.cfg"
        local_paths.copy_file(src=src, dst=dst)
        print(f"Set to {suffix.strip()} environment.")
        return

    cfg = read_pyvenv_cfg()
    if is_env_uno_python(cfg):
        src = env_path / "pyvenv_orig.cfg"
        dst = env_path / "pyvenv.cfg"
        local_paths.copy_file(src=src, dst=dst)
        print("Set to Original Environment")
        return

    src = env_path / "pyvenv_orig.cfg"
    if not src.exists():
        save_config(cfg=cfg, fnm="pyvenv_orig.cfg")

    uno_cfg = env_path / "pyvenv_uno.cfg"
    if not uno_cfg.exists():
        _set_config_save(cfg)
    src = env_path / "pyvenv_uno.cfg"
    dst = env_path / "pyvenv.cfg"
    local_paths.copy_file(src=src, dst=dst)
    print("Set to UNO Environment")


def _set_config_save(cfg):
    # need to create the file.
    ver = str(get_uno_python_ver())
    hm = _get_lo_path()
    if "version" in cfg:
        del cfg["version"]
    cfg["home"] = hm
    cfg["implementation"] = "CPython"
    cfg["version_info"] = f"{ver}.final.0"
    cfg["include-system-site-packages"] = "false"
    cfg["base-prefix"] = f"{hm}\\python-core-{ver}"
    cfg["base-exec-prefix"] = f"{hm}\\python-core-{ver}"
    cfg["base-executable"] = f"{hm}\\python.exe"
    save_config(cfg=cfg, fnm="pyvenv_uno.cfg")


def _get_lo_path() -> str:
    lo_path = os.environ.get("ODEV_CONN_SOFFICE", None)
    if lo_path:
        index = lo_path.rfind("program")
        lo_path = lo_path[: index + 7] if index > -1 else None
    if not lo_path:
        lo_path = str(uno_paths.get_soffice_install_path() / "program")
    return lo_path


def _get_venv_path() -> Path:
    v_path = os.environ.get("VIRTUAL_ENV", None)
    if v_path is None:
        raise ValueError("Unable to get Virtual Environment Path")
    return Path(v_path)


def _get_pyvenv_cfg_path(fnm: str = "pyvenv.cfg") -> Path:
    # sourcery skip: raise-specific-error
    v_path = _get_venv_path()
    pyvenv_cfg = Path(v_path, fnm)
    if not pyvenv_cfg.exists():
        raise FileNotFoundError(str(pyvenv_cfg))
    if not pyvenv_cfg.is_file():
        raise Exception(f'Not a file: "{pyvenv_cfg}"')
    return pyvenv_cfg
