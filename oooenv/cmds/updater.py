from __future__ import annotations

from . import manage_env_cfg


def needs_updating(fnm: str = "pyvenv_uno.cfg") -> bool:
    """
    Checks if the current environment needs updating.

    Returns:
        bool: True if needs updating.
    """
    try:
        cfg_version = manage_env_cfg.get_libreoffice_py_ver_from_cfg(fnm=fnm)
        uno_py_version = manage_env_cfg.get_uno_python_ver()
        return cfg_version != uno_py_version
    except Exception:
        return False


def update_cfg(fnm: str = "pyvenv_uno.cfg") -> None:
    """
    Updates a config file to the current UNO Python version.

    Only updates if the current version is different from the config version.

    Args:
        fnm (str, optional): Config File to update. Defaults to "pyvenv_uno.cfg".
    """
    cfg_version = manage_env_cfg.get_libreoffice_py_ver_from_cfg(fnm=fnm)
    uno_py_version = manage_env_cfg.get_uno_python_ver()
    if cfg_version == uno_py_version:
        return
    cfg = manage_env_cfg.read_pyvenv_cfg(fnm=fnm)
    ver_old = str(cfg_version)
    ver_new = str(uno_py_version)
    for key, value in cfg.items():
        cfg[key] = value.replace(ver_old, ver_new)
    manage_env_cfg.save_config(cfg, fnm=fnm)
