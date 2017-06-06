#!/usr/bin/env bash
# dotfiles
# Kashev Dalmia | @kashev | kashev.dalmia@gmail.com
# uinstall.sh
#
# Script for setting up a fresh Ubuntu install.

# Add Extra PPAs for...
# Sublime Text 3 (Web Upd8)
sudo add-apt-repository -y ppa:webupd8team/sublime-text-3
# JDK (Web Upd8)
sudo add-apt-repository -y ppa:webupd8team/java
# Tilix (Web Upd8)
sudo add-apt-repository ppa:webupd8team/terminix
# Chrome GNOME Shell connector
sudo add-apt-repository ppa:ne0sight/chrome-gnome-shell

# Update PPA list
sudo apt -y update

# Get Required Dotfiles Packages
sudo apt -y install git \
                    vim \
                    zsh \
                    build-essential \
                    python python3 \
                    python-dev python3-dev \
                    python-pip \
                    pep8 \
                    python-yaml
sudo pip install virtualenvwrapper

# Install Sublime Text 3 (Web Upd8)
sudo apt -y install sublime-text-installer
# Get Sublime Text to Create Dotfiles Directories
subl
pkill subl
# Install Package Control
wget \
    --directory-prefix="$HOME/.config/sublime-text-3/Installed Packages/" \
    https://sublime.wbond.net/Package%20Control.sublime-package

# TODO: Install Visual Studio Code

# Get Visual Studio Code to make Config Directories
code
pkill code

# Install Terminator
sudo apt install terminator
terminator
pkill terminator

# Install Tilix.
sudo apt install tilix

# Clone Dotfiles
mkdir ~/sw
pushd ~/sw
git clone https://github.com/kashev/dotfiles.git
pushd dotfiles
python install.py -vf
popd
popd

# Install Gnome 3
sudo apt -y install gnome-shell \
                    ubuntu-gnome-desktop

# Install JDK for JetBrains IDEs
sudo apt install -y oracle-java8-installer

# Install Google Chrome
sudo apt -y install libxss1 \
                    libappindicator1 \
                    libindicator7

pushd /tmp
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb

# Install Gnome Shell Chrome connector
sudo apt install chrome-gnome-shell

# Install Other Utilities
sudo apt -y install htop \
                    gimp \
                    vlc \
                    browser-plugin-vlc \
                    meld \
                    colordiff \
                    filezilla \
                    lftp \
                    bpython \
                    bpython3

# Install LaTeX Things
sudo apt -y install texlive \
                    latexmk \
                    texlive-latex-extra \
                    texlive-science

# Install SSH Server
sudo apt -y install openssh-server

# Finish Upgrade
sudo apt -y upgrade
