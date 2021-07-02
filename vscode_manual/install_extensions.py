#!/usr/bin/env python3
# Install VSCode Extensions from file.
#
# Instead of writing this, could have just written:
#     cat extensions.txt | xargs -L 1 code --install-extension

import subprocess

from typing import List


EXTENSIONS_FILE = "extensions.txt"


def run_cmd(cmd_list : List[str], show: bool=True):
    if show:
        print(" ".join(cmd_list))
    subprocess.call(cmd_list, shell=False)


def open_code() -> None:
    run_cmd(["code"])


def extensions(filename):
    """ Yield each of the extensions in the given file. """
    with open(filename) as extension_file:
        for extension in extension_file:
            yield extension.strip()


def install_extension(extension):
    """ Install the given extension. """
    cmd_list = ["code", "--install-extension", extension]
    run_cmd(cmd_list)


def main():
    open_code()
    for extension in extensions(EXTENSIONS_FILE):
        install_extension(extension)


if __name__ == '__main__':
    main()
