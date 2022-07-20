# -*- coding: utf-8 -*-
from __future__ import with_statement
from __future__ import absolute_import
import sys
import os
import argparse
from io import open
from typing import Tuple, Union
import beer_engine
from urllib.request import urlopen


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if __mode__ in ["pyinstaller", "local"]:
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    elif __mode__ == "deb":
        if os.path.basename(relative_path) == "logo.png":
            return "/usr/include/wheelers-wort-works/logo.png"
        elif os.path.basename(relative_path) == "commit.txt":
            return os.path.expanduser("~/.config/Wheelers-Wort-Works/commit.txt")
        return os.path.join(
            os.path.expanduser("/usr/include/wheelers-wort-works"), relative_path
        )


def get_args():
    parser = argparse.ArgumentParser(
        description="Arguments", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-f",
        "--file",
        required=False,
        action="store",
        default=None,
        help="The file to open `--file file_name.berf[x]`",
    )
    parser.add_argument(
        "-u",
        "--update",
        required=False,
        action="store_true",
        help="Using the current `update.py`, download the latest GitHub files",
    )
    parser.add_argument(
        "-U",
        "--coreupdate",
        required=False,
        action="store_true",
        help="Pull `update.py` from GitHub, then download the latest GitHub files",
    )
    parser.add_argument(
        "-l", "--local", required=False, action="store_true", help="Use the local mode"
    )
    parser.add_argument(
        "-d",
        "--deb",
        required=False,
        action="store_true",
        help="Use the debian mode (only use on a Debian/Ubuntu system)",
    )

    return parser.parse_args()


def check_for_update() -> Tuple[bool, bool, str]:
    update_available = False
    update = False
    commit = ""
    try:
        with urlopen("https://github.com/jimbob88/wheelers-wort-works") as response:
            text = response.read().decode("utf-8")
            sec = "".join(
                text[text.find('<a class="commit-tease-sha mr-1"'):].partition("</a>")[
                    :2
                ]
            )

            commit = sec.split('"')[3].split("/")[-1]
            if os.path.isfile(resource_path("commit.txt")):
                prev_commit = list(open(resource_path("commit.txt"), "r"))[0]
            else:
                prev_commit = 0
            if prev_commit != commit:
                update = True
                update_available = True
            else:
                print("Already the Latest Edition")
    except Exception:
        update = True
    return (update, update_available, commit)


__mode__ = "local"
BASE_URL = "https://raw.githubusercontent.com/jimbob88/wheelers-wort-works/master"
if __name__ == "__main__":
    args = get_args()
    if args.deb:
        __mode__ = "deb"
    if args.local:
        __mode__ = "local"

    update, update_available, commit = check_for_update()

    if args.update or args.coreupdate:
        commit = commit or list(open(resource_path("commit.txt"), "r"))[0]

        if args.update and update:
            with open(resource_path("update.py"), "r") as f:
                exec(f.read())
            update()
            with open(resource_path("commit.txt"), "w") as f:
                f.write(commit)
        if args.coreupdate and update:
            with urlopen(
                f"{BASE_URL}/update.py"
            ) as response:
                update_text = response.read().decode("utf-8")
                exec(update_text)
            update()
            print(
                "Updating {file} from {url}".format(
                    file="update.py",
                    url=f"{BASE_URL}/update.py",
                )
            )
            with open(resource_path("update.py"), "w") as f:
                f.write(update_text)
            with open(resource_path("commit.txt"), "w") as f:
                f.write(commit)
        if __mode__ == "deb":
            exit()
    if args.file is None:
        beer_engine.__mode__ = __mode__
        beer_engine.main(update_available=update_available)

    elif os.path.splitext(args.file)[1] in [".berf", ".berfx"]:
        beer_engine.__mode__ = __mode__
        file = (
            os.path.expanduser(args.file)
            if os.path.isfile(args.file)
            else os.path.join(os.getcwd(), args.file)
        )

        beer_engine.main(file=file, update_available=update_available)
