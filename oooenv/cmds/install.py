from __future__ import annotations
from pathlib import Path
from ..utils import local_paths


def pip_e(package_path: str = ".") -> str:
    """
    Install root path in virtual environment site-packages directory.

    Basically the same thing as ``pip -e .`` but without the need for pip.

    Args:
        package_path (str, optional): Path to package. Defaults to ``"."``.

    Returns:
        str: Message indicating success or failure. Empty string on failure.
    """
    try:
        root_path = Path(local_paths.get_virtual_env_path()).parent
        if package_path and package_path != ".":
            root_path = root_path / package_path

        if not root_path.exists():
            return f"No such package path as: {str(root_path)}"
        site_packages_dir = local_paths.get_site_packages_dir()
        if site_packages_dir is None:
            return ""
        file_name = site_packages_dir / f"{root_path.name.replace('.', '_').replace(' ', '_')}.pth"
        with open(file_name, "w") as f:
            f.write(str(root_path))
        return f"Created file: {file_name}"
    except Exception as e:
        return f"Failed to create file: {file_name}\n{e}"
