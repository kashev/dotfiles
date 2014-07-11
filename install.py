#!/usr/bin/env python
# dotfiles
# Kashev Dalmia | @kashev | kashev.dalmia@gmail.com
# install.py
#
# The dotfiles installer script.

# FUTURE IMPORTS
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# IMPORTS
import argparse
import logging
import os
import pep8
import sys
import yaml


# CONSTANTS
CONFIG_FILE = "config.yaml"


# FUNCTIONS

def validate_config_file(config_file):
    # Check that the configuration file exists and is both valid yaml and
    # contains the information necessary to run the installer.
    logging.info("Validating {}".format(config_file))
    retval = True
    try:
        with open(config_file, 'r') as f:
            data = f.read()
            configs = yaml.load(data)

            paths = configs['paths']
            for source in paths:
                if not os.path.isdir(os.path.join(os.getcwd(), source)):
                    logging.critical("Config path {} must also have a "
                                     "config directory.".format(source))

    except IOError as e:
        logging.critical('Problem opening {}:\n{}'
                         .format(config_file, e))
        retval = False
    except yaml.parser.ParserError as e:
        logging.critical("{} is not a valid .yaml file:\n{}"
                         .format(config_file, e))
        retval = False
    except KeyError as e:
        logging.critical("{} does not contain the proper "
                         "configuration data:\n{}".format(config_file, e))
        retval = False

    return retval


def validate_files():
    """ Validate and syntax check all the files it is possible to check in the
        entire project, including this script.
    """
    logging.info("Validating projet...")
    retval = True
    # pep8 this script for style.
    logging.info("Validating {}".format(__file__))
    pep8style = pep8.StyleGuide(quiet=True)
    pep8result = pep8style.check_files([os.path.realpath(__file__)])
    if pep8result.total_errors != 0:
        logging.warning("{} does not conform to pep8 with {} errors."
                        .format(__file__, pep8result.total_errors))
        pep8result.print_statistics()

    retval &= validate_config_file(CONFIG_FILE)

    logging.info("Done.")
    return retval


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

    # Validate Files: if the -c flag is passed, don't continue past this step.
    valid = validate_files()
    if args.check or not valid:
        sys.exit(not valid)  # exit code of zero or false indicates no error.

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
