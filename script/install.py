#!/usr/bin/env python
# dotfiles
# Kashev Dalmia | @kashev | kashev.dalmia@gmail.com
# README.md

import os
import glob
import getpass

USER = getpass.getuser()
HOME_DIR = "/home/" + USER + "/"
CURR_DIR = os.getcwd() + "/"

DOT_INSTALL_FOLDERS = ["git"]

def delete_and_link(source, dest):
    """Delete the destination file if it exists and isn't a link,
       then create a link to the destination from the source.
    """
    if os.path.isfile(dest) and not os.path.islink(dest):
        os.remove(dest)

    if not os.path.isfile(dest):
        os.symlink(source, dest)

def install_folder(source, dest):
    """Symlink all the dotfiles in the source to the dest
       (if a symlink doesn't already exist)
    """
    for f in os.listdir(source): 
        delete_and_link(source + f, dest + f)

def install_sublime():
    """Install Sublime Text 3 as it is installed through this PPA:
       http://www.webupd8.org/2013/07/sublime-text-3-ubuntu-ppa-now-available.html
    """
    SUBLIME_TEXT_CONFIG_LOCATION = HOME_DIR + ".config/sublime-text-3/Packages/User/"
    install_folder(CURR_DIR + "sublimetext" + "/",
                   SUBLIME_TEXT_CONFIG_LOCATION)
    

def main():
    """Do all the installs."""
    for folder in DOT_INSTALL_FOLDERS:
        install_folder(CURR_DIR + folder + "/", HOME_DIR)
    install_sublime()

if __name__ == '__main__':
    main()
