# coding: utf-8
from __future__ import annotations
from typing import Union
import os
import sys
import shutil
import __main__
from pathlib import Path
from typing import overload
from .sys_info import SysInfo

# do not import from type_var here.
# this module is used by uno_lnk.py and type_var imports uno
# PathOrStr = Union[str, os.PathLike]

# python path on mac:  /Applications/LibreOffice.app/Contents/Resources/python
#   https://ask.libreoffice.org/t/where-is-the-python-executable-embedded-in-libreoffice-on-macos/50042


PLATFORM = SysInfo.get_platform()
if PLATFORM == SysInfo.PlatformEnum.WINDOWS:
    import winreg

_INSTALL_PATH = None


def get_soffice_install_path() -> Path:
    """
    Gets the Soffice install path.

    For windows this will be something like: ``C:\\Program Files\\LibreOffice``.
    For Linux this will be something like: ``/usr/lib/libreoffice``

    Returns:
        Path: install as Path.

    Note:
        If `OOOENV_LO_PROGRAM_PATH` is set in the environment, then that path is returned.
    """
    # sourcery skip: assign-if-exp, extract-duplicate-method, extract-method, hoist-statement-from-if, inline-immediately-returned-variable, low-code-quality
    global _INSTALL_PATH
    if install_pth := os.environ.get("OOOENV_LO_PROGRAM_PATH", ""):
        # supersede all other methods
        return Path(install_pth)

    if _INSTALL_PATH is not None:
        return _INSTALL_PATH
    if PLATFORM == SysInfo.PlatformEnum.WINDOWS:
        # get the path location from Registry
        value = ""
        for _key in (
            # LibreOffice 3.4.5,6,7 on Windows
            "SOFTWARE\\LibreOffice\\UNO\\InstallPath",
            # OpenOffice 3.3
            "SOFTWARE\\OpenOffice.org\\UNO\\InstallPath",
        ):
            try:
                value = winreg.QueryValue(winreg.HKEY_LOCAL_MACHINE, _key)  # type: ignore
            except Exception as detail:
                value = ""
                # _errMess = "%s" % detail
            else:
                break  # first existing key will do
        if value != "":
            _INSTALL_PATH = Path("\\".join(value.split("\\")[:-1]))  # drop the program
            return _INSTALL_PATH

        # failed to get path from Registry. Going Manual
        soffice = "soffice.exe"
        p_sf = Path(os.environ["PROGRAMFILES"], "LibreOffice", "program", soffice)
        if not p_sf.exists() or not p_sf.is_file():
            p_sf = Path(os.environ["PROGRAMFILES(X86)"], "LibreOffice", "program", soffice)
        if not p_sf.exists() or not p_sf.is_file():
            # perhaps running a developer version.
            # C:\Program Files\LibreOfficeDev 7\program
            p_sf = Path(os.environ["PROGRAMFILES"], "LibreOfficeDev 7", "program", soffice)
        if not p_sf.exists() or not p_sf.is_file():
            p_sf = Path(os.environ["PROGRAMFILES(X86)"], "LibreOfficeDev 7", "program", soffice)
        if not p_sf.exists():
            raise FileNotFoundError(f"LibreOffice '{p_sf}' not found.")
        if not p_sf.is_file():
            raise IsADirectoryError(f"LibreOffice '{p_sf}' is not a file.")
        # drop \program\soffice.exe
        # expect C:\Program Files\LibreOffice
        _INSTALL_PATH = p_sf.parent.parent
        return _INSTALL_PATH

    elif PLATFORM == SysInfo.PlatformEnum.MAC:
        _INSTALL_PATH = Path("/Applications/LibreOffice.app/Contents/MacOS")
        return _INSTALL_PATH
    else:
        # unix
        soffice = "soffice"
        # search system path
        s = shutil.which(soffice)
        p_sf = None
        if s is not None:
            # expect '/usr/bin/soffice'
            if os.path.islink(s):
                p_sf = Path(os.path.realpath(s)).parent
            else:
                p_sf = Path(s).parent
        if p_sf is None:
            s = "/usr/bin/soffice"
            if os.path.islink(s):
                p_sf = Path(os.path.realpath(s)).parent
            else:
                p_sf = Path(s).parent
        if not p_sf.exists():
            raise FileNotFoundError(f"LibreOffice '{p_sf}' not found.")
        if not p_sf.is_file():
            raise IsADirectoryError(f"LibreOffice '{p_sf}' is not a file.")
        # drop /program/soffice
        _INSTALL_PATH = p_sf.parent.parent
        return _INSTALL_PATH


def get_soffice_path() -> Path:
    """
    Gets path to soffice

    Returns:
        Path: path to soffice
    """
    if PLATFORM == SysInfo.PlatformEnum.WINDOWS:
        return Path(get_lo_path(), "soffice.exe")
    return Path(get_lo_path(), "soffice")


def _get_soffice_which_path() -> Path | None:
    """
    Gets the path to soffice using shutil.which

    Usually something like ``/usr/lib/libreoffice/program/soffice``
    """
    if link_path := shutil.which("soffice"):
        relative_path = os.path.realpath(link_path)
        if os.path.isabs(relative_path):
            return Path(relative_path)
        else:
            return Path(os.path.abspath(relative_path))
    return None


def get_uno_path() -> Path:
    """
    Searches known paths for path that contains uno.py

    This path is different for windows and linux.
    Typically for Windows ``C:\\Program Files\\LibreOffice\\program``
    Typically for Linux ``/usr/lib/python3/dist-packages``

    Raises:
        FileNotFoundError: if path is not found
        NotADirectoryError: if path is not a directory

    Returns:
        Path: First found path.

    Note:
        If `OOOENV_LO_UNO_PATH` is set, it will be returned without any checks.
    """
    if env_path := os.environ.get("OOOENV_LO_UNO_PATH", ""):
        # special environment variable, no arguments just return it
        return Path(env_path)

    if PLATFORM == SysInfo.PlatformEnum.WINDOWS:
        p_uno = Path(os.environ["PROGRAMFILES"], "LibreOffice", "program")
        if not p_uno.exists() or not p_uno.is_dir():
            p_uno = Path(os.environ["PROGRAMFILES(X86)"], "LibreOffice", "program")
        if not p_uno.exists():
            raise FileNotFoundError("Uno Source Dir not found.")
        if not p_uno.is_dir():
            raise NotADirectoryError("UNO source is not a Directory")
        return p_uno
    elif PLATFORM == SysInfo.PlatformEnum.MAC:
        return Path("/Applications/LibreOffice.app/Contents/MacOS/soffice")
    else:
        check_paths = ("/usr/lib/python3/dist-packages", "/usr/lib/libreoffice/program", "/opt/libreoffice/program")
        p_uno = None
        for pth in check_paths:
            p_uno = Path(pth)
            if p_uno.exists() and p_uno.is_dir() and (p_uno / "uno.py").exists():
                return p_uno
        # not found yet.
        # try using shutil.which to extract the path from the link.
        if which_path := _get_soffice_which_path():
            # '/usr/lib/libreoffice/program/soffice'
            p_uno = which_path.parent
            if p_uno.exists() and p_uno.is_dir() and (p_uno / "uno.py").exists():
                return p_uno

    raise FileNotFoundError("Uno Source Dir not found.")


def get_lo_path() -> Path:
    """
    Searches known paths for path that contains LibreOffice ``soffice``.

    This path is different for windows and linux.
    Typically for Windows ``C:\\Program Files\\LibreOffice\\program``
    Typically for Linux ``/usr/bin/soffice``

    Raises:
        FileNotFoundError: if path is not found
        NotADirectoryError: if path is not a directory

    Returns:
        Path: First found path.

    Note:
        If `OOOENV_LO_PROGRAM_PATH` is set, it will be returned without any checks.
    """
    # sourcery skip: assign-if-exp, extract-method, introduce-default-else
    if lo_path := os.environ.get("OOOENV_LO_PROGRAM_PATH", ""):
        # special environment variable, no arguments just return it
        return Path(lo_path)

    if PLATFORM == SysInfo.PlatformEnum.WINDOWS:
        return Path(get_soffice_install_path(), "program")

    elif PLATFORM == SysInfo.PlatformEnum.MAC:
        return Path("/Applications/LibreOffice.app/Contents/MacOS")
    else:
        # search system path
        s = shutil.which("soffice")
        p_sf = None
        if s is not None:
            # expect '/usr/bin/soffice'
            if os.path.islink(s):
                # follow link
                p_sf = Path(os.path.realpath(s)).parent
            else:
                p_sf = Path(s).parent
        if p_sf is None:
            p_sf = Path("/usr/bin/soffice")
            if not p_sf.exists() or not p_sf.is_file():
                raise FileNotFoundError("LibreOffice Source Dir not found.")
            p_sf = p_sf.parent

        if not p_sf.exists():
            raise FileNotFoundError("LibreOffice Source Dir not found.")
        if not p_sf.is_dir():
            raise NotADirectoryError("LibreOffice source is not a Directory")
        return p_sf


def get_lo_python_ex() -> str:
    """
    Gets the python executable for different environments.

    In Linux this is the current python executable.
    If a virtual environment is activated then that will be the
    python executable that is returned.

    In Windows this is the ``python.exe`` file in LibreOffice.
    Typically for Windows ``C:\\Program Files\\LibreOffice\\program\\python.exe``

    Raises:
        FileNotFoundError: In Windows if ``python.exe`` is not found.
        NotADirectoryError: In Windows if ``python.exe`` is not a file.

    Returns:
        str: file location of python executable.

    Note:
        If `OOOENV_LO_PY_EXE` environment variable is set, it will be returned without any checks.
    """
    if env_path := os.environ.get("OOOENV_LO_PY_EXE", ""):
        return env_path
    if PLATFORM != SysInfo.PlatformEnum.WINDOWS:
        return sys.executable
    p = Path(get_lo_path(), "python.exe")

    if not p.exists():
        raise FileNotFoundError("LibreOffice python executable not found.")
    if not p.is_file():
        raise NotADirectoryError("LibreOffice  python executable is not a file")
    return str(p)


@overload
def mkdirp(dest_dir: str) -> None:
    ...


@overload
def mkdirp(dest_dir: Path) -> None:
    ...


def mkdirp(dest_dir: Union[str, os.PathLike]) -> None:
    """
    Creates path and subpath not existing.

    Args:
        dest_dir (str | PathLike]): PathLike object
    """
    # Python ≥ 3.5
    pth = Path(dest_dir)
    if not pth.is_absolute():
        pth = pth.resolve()
    pth.mkdir(parents=True, exist_ok=True)
