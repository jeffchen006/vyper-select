import argparse
import hashlib
import json
from zipfile import ZipFile
import shutil
import re
import stat
import urllib.request
from pathlib import Path
from packaging.version import Version
from Crypto.Hash import keccak
import sys
import os
import requests
from typing import Dict, List, Optional, Union
from base64 import b64encode

import tempfile
import threading


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


# import importlib  
# constants = importlib.import_module("vyper-select.constants")
from .constants import (
    LINUX_AMD64,
    MACOSX_AMD64,
    WINDOWS_AMD64,
    EARLIEST_RELEASE,
    VYPER_SELECT_DIR,
    ARTIFACTS_DIR,
)

# lock = importlib.import_module("vyper-select.lock")
# from lock import get_process_lock



Path.mkdir(ARTIFACTS_DIR, parents=True, exist_ok=True)


BINARY_DOWNLOAD_BASE = "https://github.com/vyperlang/vyper/releases/download/v{}/{}"
GITHUB_RELEASES = "https://api.github.com/repos/vyperlang/vyper/releases?per_page=500"





# pylint: disable=consider-using-with
def get_available_versions() -> list:
    """Return a list of all Vyper versions available for download."""
    version_list = []
    for release in _get_releases():
        version = release["tag_name"].lstrip("v")
        asset = next((i for i in release["assets"] if _get_os_name() in i["name"]), False)
        if asset:
            version_list.append(version)
    return sorted(version_list, reverse=True)



def _check_for_installed_version(version: str) -> bool:
    path = ARTIFACTS_DIR.joinpath(f"vyper-{version}")
    return path.exists()



def get_executable(version: str) -> Path:
    """Return the path to the executable for the given version."""
    vyper_bin = ARTIFACTS_DIR.joinpath(f"vyper-{version}").joinpath(f"vyper-{version}")
    if not vyper_bin.exists():
        raise argparse.ArgumentTypeError(
            f"vyper {version} has not been installed."
        )
    return vyper_bin



def current_version():
    version = os.environ.get("VYPER_VERSION")
    source = "VYPER_VERSION"
    if version:
        if version not in installed_versions():
            raise argparse.ArgumentTypeError(
                f"Version '{version}' not installed (set by {source}). Run `vyper-select install {version}`."
            )
    else:
        source = VYPER_SELECT_DIR.joinpath("global-version")
        if Path.is_file(source):
            with open(source, encoding="utf-8") as f:
                version = f.read()
        else:
            raise argparse.ArgumentTypeError(
                "No vyper version set. Run `vyper-select use VERSION` or set VYPER_VERSION environment variable."
            )
    return version, source



def installed_versions() -> list:
    return [
        f.replace("vyper-", "") for f in sorted(os.listdir(ARTIFACTS_DIR)) if f.startswith("vyper-")
    ]


def valid_install_arg(arg: str) -> str:
    if arg == "all":
        return arg
    return valid_version(arg)



def get_installable_versions() -> list:
    installable = list(set(get_available_versions()) - set(installed_versions()))
    installable.sort(key=Version)
    return installable



def install_artifacts(versions: list) -> bool:
    releases = get_available_versions()

    for version in releases:
        if "all" not in versions:
            if versions and version not in versions:
                continue
        os_name = _get_os_name()


        if _check_for_installed_version(version):
            print(f"vyper {version} already installed")
            continue

        if version not in releases:
            print(f"vyper {version} is not available")
            continue
        

        data = _get_releases()
        try:
            release = next(i for i in data if i["tag_name"] == f"v{version}")
            asset = next(i for i in release["assets"] if _get_os_name() in i["name"])
        except StopIteration:
            print(f"Vyper binary not available for version {version}")
            continue

        
        artifact_file_dir = ARTIFACTS_DIR.joinpath(f"vyper-{version}")
        Path.mkdir(artifact_file_dir, parents=True, exist_ok=True)
        print(f"Installing '{version}'...")


        url = BINARY_DOWNLOAD_BASE.format(version, asset["name"])

        artifact_file_dir = artifact_file_dir.joinpath(f"vyper-{version}")
        urllib.request.urlretrieve(url, artifact_file_dir)

        if os_name != "windows":
            # make it an executable
            artifact_file_dir.chmod(artifact_file_dir.stat().st_mode | stat.S_IEXEC)
        
        print(f"Version '{version}' installed.")

    return True



def _get_releases() -> Dict:
    data = requests.get(GITHUB_RELEASES)
    if data.status_code != 200:
        msg = (
            f"Status {data.status_code} when getting Vyper versions from Github:"
            f" '{data.json()['message']}'"
        )
        if data.status_code == 403:
            msg += (
                "\n\nIf this issue persists, generate a Github API token and store"
                " it as the environment variable `GITHUB_TOKEN`:\n"
                "https://github.blog/2013-05-16-personal-api-tokens/"
            )
        raise ConnectionError(msg)
    return data.json()



def switch_global_version(version: str, always_install: bool) -> None:
    if version in installed_versions():
        with open(f"{VYPER_SELECT_DIR}/global-version", "w", encoding="utf-8") as f:
            f.write(version)
        print("Switched global version to", version)
    elif version in get_available_versions():
        if always_install:
            install_artifacts([version])
            switch_global_version(version, always_install)
        else:
            raise argparse.ArgumentTypeError(f"'{version}' must be installed prior to use.")
    else:
        raise argparse.ArgumentTypeError(f"Unknown version '{version}'")



def valid_version(version: str) -> str:

    releases = get_available_versions()

    if version not in releases:
        raise argparse.ArgumentTypeError(f"Invalid version '{version}'.")


    if Version(version) < Version(EARLIEST_RELEASE[_get_os_name()]):
        raise argparse.ArgumentTypeError(
            f"Invalid version - only vyper versions above '{EARLIEST_RELEASE[_get_os_name()]}' are available"
        )

    latest_release = releases[0]
    # pylint: disable=consider-using-with
    if Version(version) > Version(latest_release):
        raise argparse.ArgumentTypeError(
            f"Invalid version '{latest_release}' is the latest available version"
        )

    return version






def _get_os_name() -> str:
    if sys.platform.startswith("linux"):
        return "linux"
    if sys.platform == "darwin":
        return "darwin"
    if sys.platform == "win32":
        return "windows"
    raise OSError(f"Unsupported OS: '{sys.platform}'")



# if __name__ == "__main__":
#     # the following are simply tests. 
#     platform = _get_os_name()
#     print(platform)

#     releases = get_available_versions()
#     print(releases)

#     # releases = _get_releases()
#     # print(releases)

#     # # test install
#     # install_artifacts(["0.3.6"])

#     switch_global_version("0.3.6", True)
