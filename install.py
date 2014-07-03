#!/usr/bin/env python
# dotfiles
# Kashev Dalmia | @kashev | kashev.dalmia@gmail.com
# install.py

import argparse
import getpass
import logging
import os

HOME_DIR = os.path.join("/home", getpass.getuser())

DOT_INSTALL_FOLDERS = ["git"]


def delete_and_link(source, dest, force=False):
    """Delete the destination file if it exists and isn't a link,
       then create a link to the destination from the source.
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
    """Symlink all the dotfiles in the source to the dest
       (if a symlink doesn't already exist)
    """
    for f in os.listdir(source):
        logging.info("Installing symlinks for {}".format(f))
        delete_and_link(os.path.join(source, f),
                        os.path.join(dest, f),
                        force)


def install_sublime():
    """Install Sublime Text 3 settings assuming it is installed through
       this PPA:
    http://www.webupd8.org/2013/07/sublime-text-3-ubuntu-ppa-now-available.html
    """
    ST3_LOC = os.path.join(HOME_DIR,
                           ".config",
                           "sublime-text-3",
                           "Packages",
                           "User")

    logging.info("Installing Sublime Text 3 settings to {}".format(ST3_LOC))
    install_folder(os.path.join(os.getcwd(), "sublimetext"),
                   ST3_LOC)
    logging.info("Done.")


def main():
    """Parse command line arguments, then do all the installs."""
    parser = argparse.ArgumentParser(
        description="Install dotfiles and settings from "
                    "github.com/kashev/dotfiles.")

    parser.add_argument("-f", "--force",
                        help="force creation of new symlinks",
                        action="store_true")
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    for folder in DOT_INSTALL_FOLDERS:
        install_folder(os.path.join(os.getcwd(), folder),
                       HOME_DIR,
                       args.force)

    install_sublime()


if __name__ == '__main__':
    main()
