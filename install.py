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
import shutil
import subprocess
import sys
# As this script is meant to be installed on a fresh installation, non default
# imports are in a try-except block to cleanly handle uninstalled dependencies.
try:
    import pep8
    import yaml
except ImportError as e:
    logging.critical("Missing dependency: {}. "
                     "Run 'sudo pip install pep8 pyyaml' or install the "
                     "packages 'pep8' and 'python-yaml' with your system "
                     "package manager."
                     .format(e))
    sys.exit(1)


# CONSTANTS
CONFIG_FILE = "config.yaml"


# FUNCTIONS

def check_pep8(*files):
    """Check that the files conform to pep8. Return True if they do."""
    logging.info("Validating files for pep8 conformance...")

    flist = [f for f in files]

    pep8style = pep8.StyleGuide(quiet=True)
    pep8result = pep8style.check_files(flist)

    if pep8result.total_errors != 0:
        logging.warning("1 or more files does not conform to pep8: {} errors."
                        .format(pep8result.total_errors))
        pep8result.print_statistics()
        return False
    else:
        return True


def validate_config_file(config_file):
    # Check that the configuration file exists and is both valid yaml and
    # contains the information necessary to run the installer. Check for
    # existance of necessary keys by simply referecing them.
    logging.info("Validating {}...".format(config_file))
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
                paths[source]['dot']
                paths[source]['path']

            configs["settings"]

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
    # pep8 this script for style. The return value doesn't matter for project
    # validity, so don't use the return value.
    check_pep8(__file__)

    retval &= validate_config_file(CONFIG_FILE)

    logging.info("Done.")
    return retval


def clone_submodules():
    subprocess.call(["git", "submodule", "update", "--init", "--recursive"])


def delete_and_link(source, dest, force=False):
    """ Delete the destination file if it exists and isn't a link, then create
        a link to the destination from the source. The force option causes
        symlinks to be recreated, even if they already exist.
    """
    try:
        if os.path.lexists(dest) and (force or not os.path.islink(dest)):
            logging.info("Deleting existing {}".format(dest))
            if os.path.isfile(dest) or os.path.islink(dest):
                os.remove(dest)
            elif os.path.isdir(dest):
                shutil.rmtree(dest)

        if not os.path.lexists(dest):
            logging.info("Creating symlink {} to {}".format(source, dest))
            os.symlink(source, dest)

    except Exception as e:
        logging.critical("Error Creating Symlink {} to {} : {}"
                         .format(source, dest, e))


def install_folder(source, dest, force=False, prepend_dot=False):
    """ Symlink all the dotfiles in the source to the dest. The force option
        is passed to delete_and_link(). The prepend_dot option exists to
        prepend a dot to the filename for copying."""
    logging.info("Installing symlinks for {}".format(os.path.basename(source)))
    prepend = '.' if prepend_dot else ''
    for f in os.listdir(source):
        delete_and_link(os.path.join(source, f),
                        os.path.join(dest, prepend + f),
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

    require_logout = False

    # TODO: Check and install external dependencies in a portable way.

    # Validate Files: if the -c flag is passed, don't continue past this step.
    valid = validate_files()
    if args.check or not valid:
        sys.exit(not valid)  # exit code of zero or false indicates no error.

    # The rest of the script expects submodules to be cloned and present.
    clone_submodules()

    # Load config file.
    with open(CONFIG_FILE, 'r') as f:
        data = f.read()
        configs = yaml.load(data)

    # Install all paths.
    paths = configs['paths']
    for source in paths:
        install_folder(os.path.join(os.getcwd(), source),
                       os.path.expanduser(paths[source]['path']),
                       args.force,
                       paths[source]['dot'])

    # Change system settings.
    settings = configs['settings']
    for setting in settings:
        if setting == "shell":
            shell = settings[setting]
            if shell != os.environ['SHELL']:
                logging.info("Changing default shell to '{}'.".format(shell))
                print("Type your password for 'chsh' : ", end="")
                subprocess.call(["chsh", "-s " + shell])
                require_logout = True

    if require_logout:
        print("Log in and log back out to apply all changes.")

if __name__ == '__main__':
    main()
