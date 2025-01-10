import json
import subprocess as sp
from typing import Dict, List

from clize import run


def disable_package(pkg_name: str) -> None:
    sp.run(f"adb shell pm disable-user --user 0 {pkg_name}".split())


def get_enabled_package_names() -> List[str]:
    return [
        s[len("package:") :]
        for s in sp.run(
            "adb shell pm list packages --user 0 -e".split(),
            capture_output=True,
            check=True,
        )
        .stdout.decode()
        .splitlines()
    ]


def disable_all_recommended_software():
    with open("uad_lists.json", "r") as file:
        uad_lists: Dict[str, Dict[str, str]] = json.load(file)
    for pkg_name in get_enabled_package_names():
        uad_info = uad_lists.get(pkg_name)
        if uad_info is None:
            continue
        if uad_info["removal"] == "Recommended":
            disable_package(pkg_name)


def disable_play_store():
    disable_package("com.android.vending")


def print_enabled_packages():
    for pkg_name in sorted(get_enabled_package_names()):
        print(pkg_name)


if __name__ == "__main__":
    run(
        disable_all_recommended_software,
        disable_play_store,
        print_enabled_packages,
        disable_package,
    )
