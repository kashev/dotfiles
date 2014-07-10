#!/usr/bin/env python
# dotfiles
# Kashev Dalmia | @kashev | kashev.dalmia@gmail.com
# install.py

# IMPORTS
import argparse
import getpass
import logging
import os
import subprocess


# CONSTANTS

HOME_DIR = os.path.join("/home", getpass.getuser())

# ST3 Location as installed through this PPA:
# http://www.webupd8.org/2013/07/sublime-text-3-ubuntu-ppa-now-available.html
ST3_LOC = os.path.join(HOME_DIR,
                       ".config",
                       "sublime-text-3",
                       "Packages",
                       "User")

# Install paths for everything. The key is a folder in this repository, and
# the value is the place where the files in the folder should be installed.
INSTALL_PATHS = {
    "git": HOME_DIR,
    "vim": HOME_DIR,
    "sublimetext": ST3_LOC
}

# Constants related to packages to be installed. Currently Ubuntu only.
PACKAGE_MANAGER_SUDO = ["sudo"]
PACKAGE_MANAGER_ADD_REPO = ["add-apt-repository"]
PACKAGE_MANAGER_UPDATE = ["apt-get", "update"]
PACKAGE_MANAGER_INSTALL = ["apt-get", "install"]
REPOSITORIES_TO_ADD = ["ppa:webupd8team/sublime-text-3"]
PACKAGES_TO_INSTALL = ["vim", "git", "sublime-text-installer"]


# FUNCTIONS

def install_linux_packages():
    subprocess.call(PACKAGE_MANAGER_SUDO +
                    PACKAGE_MANAGER_ADD_REPO +
                    REPOSITORIES_TO_ADD)

    subprocess.call(PACKAGE_MANAGER_SUDO +
                    PACKAGE_MANAGER_UPDATE)

    subprocess.call(PACKAGE_MANAGER_SUDO +
                    PACKAGE_MANAGER_INSTALL +
                    PACKAGES_TO_INSTALL)


def delete_and_link(source, dest, force=False):
    """Delete the destination file if it exists and isn't a link, then create
       a link to the destination from the source. The force option causes
        symlinks to be recreated, even if they already exist.
    """
    try:
        if os.path.isfile(dest) and (force or not os.path.islink(dest)):
            logging.info("Deleting existing {}".format(dest))
            os.remove(dest)

        if not os.path.isfile(dest):
            logging.info("Creating symlink {} to {}".format(source, dest))
            os.symlink(source, dest)

    except Exception as e:
        logging.critical("Error Creating Symlink {} to {} : {}"
                         .format(source, dest, e))


def install_folder(source, dest, force=False):
    """Symlink all the dotfiles in the source to the dest."""
    logging.info("Installing symlinks for {}".format(os.path.basename(source)))
    for f in os.listdir(source):
        delete_and_link(os.path.join(source, f),
                        os.path.join(dest, f),
                        force)


def main():
    """Parse command line arguments, then do all the installs."""
    parser = argparse.ArgumentParser(
        description="Install dotfiles and settings from "
                    "http://github.com/kashev/dotfiles")

    parser.add_argument("-f", "--force",
                        help="force creation of new symlinks",
                        action="store_true")
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Install external dependencies.
    install_linux_packages()

    # Install all paths.
    for source in INSTALL_PATHS:
        install_folder(os.path.join(os.getcwd(), source),
                       INSTALL_PATHS[source],
                       args.force)


if __name__ == '__main__':
    main()
