import pytest


@pytest.fixture(scope="session")
def config_uno():
    def wraps(ver: str = "3.8.16") -> dict:
        config = {
            "home": "C:\\Program Files\\LibreOffice\\program",
            "implementation": "CPython",
            "version_info": f"{ver}.final.0",
            "virtualenv": "20.17.1",
            "include-system-site-packages": "False",
            "base-prefix": f"C:\\Program Files\\LibreOffice\\program\\python-core-{ver}",
            "base-exec-prefix": f"C:\\Program Files\\LibreOffice\\program\\python-core-{ver}",
            "base-executable": "C:\\Program Files\\LibreOffice\\program\\python.exe",
        }
        return config

    return wraps
