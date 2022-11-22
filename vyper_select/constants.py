import os
from pathlib import Path

# DIRs path
if "VIRTUAL_ENV" in os.environ:
    HOME_DIR = Path(os.environ["VIRTUAL_ENV"])
else:
    HOME_DIR = Path.home()

VYPER_SELECT_DIR = HOME_DIR.joinpath(".vyper-select")
ARTIFACTS_DIR = VYPER_SELECT_DIR.joinpath("artifacts")

# CLI Flags
INSTALL_VERSIONS = "INSTALL_VERSIONS"
USE_VERSION = "USE_VERSION"
SHOW_VERSIONS = "SHOW_VERSIONS"
UPGRADE = "UPGRADE"

LINUX_AMD64 = "linux-amd64"
MACOSX_AMD64 = "macosx-amd64"
WINDOWS_AMD64 = "windows-amd64"

EARLIEST_RELEASE = {"darwin": "0.1.0-beta.16", "linux": "0.1.0-beta.16", "windows": "0.1.0-beta.16"}
