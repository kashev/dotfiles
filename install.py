#!/usr/bin/env python
# dotfiles
# Kashev Dalmia | @kashev | kashev.dalmia@gmail.com
# install.py
#
# The dotfiles installer script.

# IMPORTS
import argparse
import logging
import os
import pep8
import yaml

# CONSTANTS
CONFIG_FILE = "config.yaml"


# FUNCTIONS

def validate_files():
    """ Validate and syntax check all the files it is possible to check in the
        entire project, including this script.
    """
    logging.info("Validating projet...")

    # pep8 this script for style.
    logging.info("Validating {}".format(__file__))
    pep8style = pep8.StyleGuide(quiet=True)
    pep8result = pep8style.check_files([os.path.realpath(__file__)])
    if pep8result.total_errors != 0:
        logging.warning(" {} does not conform to pep8 with {} errors.\n"
                        .format(__file__, pep8result.total_errors))
        pep8result.print_statistics()

    logging.info("Done.")


def delete_and_link(source, dest, force=False):
    """ Delete the destination file if it exists and isn't a link, then create
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
    """ Symlink all the dotfiles in the source to the dest. """
    logging.info("Installing symlinks for {}".format(os.path.basename(source)))
    for f in os.listdir(source):
        delete_and_link(os.path.join(source, f),
                        os.path.join(dest, f),
                        force)


def main():
    """ Parse command line arguments, then do all the installs. """
    parser = argparse.ArgumentParser(
        description="Install dotfiles and settings from "
                    "http://github.com/kashev/dotfiles")

    parser.add_argument("-f", "--force",
                        help="force creation of new symlinks",
                        action="store_true")
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")
    parser.add_argument("-c", "--check", "--validate",
                        help="only validate, don't install",
                        action="store_true")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # TODO: Check and install external dependencies in a portable way.

    # Validate Files : if the -c flag is passed, don't continue past this step.
    validate_files()
    if args.check:
        exit(0)

    # Load config file.
    with open(CONFIG_FILE, 'r') as f:
        data = f.read()
        configs = yaml.load(data)

    # Install all paths.
    paths = configs['paths']
    for source in paths:
        install_folder(os.path.join(os.getcwd(), source),
                       os.path.expanduser(paths[source]),
                       args.force)


if __name__ == '__main__':
    main()
