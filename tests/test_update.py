from __future__ import annotations
from typing import Dict
import pytest
import sys
from pytest import MonkeyPatch


if __name__ == "__main__":
    pytest.main([__file__])


@pytest.mark.skipif(sys.platform != "win32", reason="Only runs on windows")
def test_needs_updating(config_uno, monkeypatch: MonkeyPatch):
    from oooenv.cmds import manage_env_cfg
    from oooenv.cmds import updater

    def mock_read_pyvenv_cfg(fnm):
        return config_uno("3.8.12")

    def mock_get_uno_python_ver():
        return manage_env_cfg.Version(3, 8, 16)

    monkeypatch.setattr(manage_env_cfg, "read_pyvenv_cfg", mock_read_pyvenv_cfg)
    monkeypatch.setattr(manage_env_cfg, "get_uno_python_ver", mock_get_uno_python_ver)

    assert updater.needs_updating()


@pytest.mark.skipif(sys.platform != "win32", reason="Only runs on windows")
def test_needs_no_updating(config_uno, monkeypatch: MonkeyPatch):
    from oooenv.cmds import manage_env_cfg
    from oooenv.cmds import updater

    def mock_read_pyvenv_cfg(fnm):
        return config_uno("3.8.16")

    def mock_get_uno_python_ver():
        return manage_env_cfg.Version(3, 8, 16)

    monkeypatch.setattr(manage_env_cfg, "read_pyvenv_cfg", mock_read_pyvenv_cfg)
    monkeypatch.setattr(manage_env_cfg, "get_uno_python_ver", mock_get_uno_python_ver)

    assert updater.needs_updating() is False


@pytest.mark.skipif(sys.platform != "win32", reason="Only runs on windows")
def test_update_cfg(config_uno, monkeypatch: MonkeyPatch):
    from oooenv.cmds import manage_env_cfg
    from oooenv.cmds import updater

    def mock_read_pyvenv_cfg(fnm):
        return config_uno("3.7.2")

    def mock_get_uno_python_ver():
        return manage_env_cfg.Version(3, 8, 16)

    def mock_save_config(cfg: Dict[str, str], fnm: str = "pyvenv.cfg"):
        assert cfg["version_info"].startswith("3.8.16")
        return None

    monkeypatch.setattr(manage_env_cfg, "read_pyvenv_cfg", mock_read_pyvenv_cfg)
    monkeypatch.setattr(manage_env_cfg, "get_uno_python_ver", mock_get_uno_python_ver)
    monkeypatch.setattr(manage_env_cfg, "save_config", mock_save_config)

    updater.update_cfg()
