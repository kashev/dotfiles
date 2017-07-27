#!/usr/bin/env python
# dotfiles
# Kashev Dalmia | @kashev | kashev.dalmia@gmail.com
# install.py

""" The dotfiles installer script. """


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
    import yaml
except ImportError as err:
    logging.critical("Missing dependency: {}. "
                     "Run 'sudo pip install pyyaml' or install the package "
                     "'python-yaml' with your system package manager."
                     .format(err))
    sys.exit(1)


# CONSTANTS
CONFIG_FILE = "config.yaml"


# FUNCTIONS


def validate_config_file(config_file):
    """ Check that the configuration file exists and is both valid yaml and
        contains the information necessary to run the installer. Checks for
        existance of necessary keys by simply referecing them.
    """
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

            configs['options']

    except IOError as err:
        logging.critical('Problem opening {}:\n{}'
                         .format(config_file, err))
        retval = False
    except yaml.parser.ParserError as err:
        logging.critical("{} is not a valid .yaml file:\n{}"
                         .format(config_file, err))
        retval = False
    except KeyError as err:
        logging.critical("{} does not contain the proper "
                         "configuration data:\n{}".format(config_file, err))
        retval = False
    except yaml.scanner.ScannerError as err:
        logging.critical("{} has an incorrect syntax: "
                         "{}\n".format(config_file, err))
        retval = False

    return retval


def validate_files():
    """ Validate and syntax check all the files it is possible to check in the
        entire project, including this script.
    """
    logging.info("Validating projet...")

    retval = True
    retval &= validate_config_file(CONFIG_FILE)

    logging.info("Done.")
    return retval


def get_login_shell():
    """ Gets the current login shell:
        getent passwd $LOGNAME | cut -d: -f7
    """
    output = subprocess.check_output("getent passwd $LOGNAME",
                                     shell=True)
    return output.strip().rsplit(':', 1)[1]


def change_login_shell(shell):
    """ Change the default login shell using chsh. Returns True only if a
        change was made and a log-in/log-out may be required.
    """
    new_shell = "/bin/{}".format(shell)
    old_shell = get_login_shell()

    if new_shell != old_shell:
        try:
            logging.info("Changing default shell to '{}'.".format(shell))
            print("Please enter your password for 'chsh' to {} : "
                  .format(shell), end="")
            sys.stdout.flush()
            subprocess.check_call(["chsh", "-s", new_shell])
            return True
        except subprocess.CalledProcessError as err:
            logging.warning("Could not change login shell: {}".format(err))
            return False
    else:
        return False


def clone_submodules(output=False):
    """ Clones all git submodules in the project. """
    logging.info("Cloning all submodules...")
    output_text = subprocess.check_output(["git", "submodule", "update",
                                           "--init", "--recursive"])
    if output:
        print(output_text, end='')
    logging.info("Done.")


def delete_and_link(source, dest, force=False):
    """ Delete the destination file if it exists and isn't a link, then create
        a link to the destination from the source. The force option causes
        symlinks to be recreated, even if they already exist.
    """
    try:
        if os.path.lexists(dest):
            # if force flag is on, delete the existing data
            if force:
                logging.info("Deleting existing {}".format(dest))
                if os.path.isfile(dest) or os.path.islink(dest):
                    os.remove(dest)
                elif os.path.isdir(dest):
                    shutil.rmtree(dest)
            # if the force flag is not on and the target destination already
            # exists, then check to see if the target link is already set. If
            # not, back it up, and continue as if it were not there.
            else:
                if not (os.path.islink(dest) and
                        (os.path.realpath(dest) == os.path.realpath(source))):
                    logging.info("Backing up {} to {}.original"
                                 .format(dest, dest))
                    os.rename(dest, dest + '.original')

        if not os.path.lexists(dest):
            logging.info("Creating symlink {} to {}".format(source, dest))
            os.symlink(source, dest)

    except Exception as err:
        logging.critical("Error Creating Symlink {} to {} : {}"
                         .format(source, dest, err))


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


def parse_args():
    """ Parse command line arguments. """
    parser = argparse.ArgumentParser(
        description=("Install dotfiles and settings from "
                     "http://github.com/kashev/dotfiles"))

    parser.add_argument("-f", "--force",
                        help="deletes whatever is in the way. use with extreme"
                             " caution to avoid loss of data",
                        action="store_true")

    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true")

    parser.add_argument("-c", "--check",
                        help="check config, don't install",
                        action="store_true")

    parser.add_argument("--change-shell",
                        help="change the login shell",
                        action="store_true")

    return parser.parse_args()


def main():
    """ Install all dotfiles. """
    args = parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    # Validate Files: if the -c flag is passed, don't continue past this step.
    valid = validate_files()
    if args.check or not valid:
        sys.exit(not valid)  # exit code of zero or false indicates no error.

    # The rest of the script expects submodules to be cloned and present.
    clone_submodules(args.verbose)

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

    # Create virtualenv storage folder, if it does not exist.
    virtualenvs_dir = os.path.expanduser("~/.virtualenvs")
    if not os.path.exists(virtualenvs_dir):
        logging.info("Creating virtualenvs dir : {}".format(virtualenvs_dir))
        os.makedirs(virtualenvs_dir)
    # These hook files are not symlinked because the contents of the
    # virtualenvs directory should not be version controlled.
    for f in os.listdir("virtualenv_hooks"):
        shutil.copy(os.path.join("virtualenv_hooks", f), virtualenvs_dir)

    # Apply system options.
    options = configs['options']
    for option in options:

        # Only change the login shell if explicitly told to.
        if option == 'shell' and args.change_shell:
            change_login_shell(options[option])

if __name__ == '__main__':
    main()
