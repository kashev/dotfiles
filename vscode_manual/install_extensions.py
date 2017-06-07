#!/usr/bin/env python
# Install VSCode Extensions from file.

from __future__ import print_function

import subprocess


EXTENSIONS_FILE = "extensions.txt"


def extensions(filename):
    """ Yield each of the extensions in the given file. """
    with open(filename) as extension_file:
        for extension in extension_file:
            yield extension


def install_extension(extension):
    """ Install the given extension. """
    cmd_list = ["code", "--install-extension", extension]
    print(" ".join(cmd_list), end="")
    subprocess.call(cmd_list, shell=True)


def main():
    for extension in extensions(EXTENSIONS_FILE):
        install_extension(extension)


if __name__ == '__main__':
    main()
