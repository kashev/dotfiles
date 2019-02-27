#!/usr/bin/env bash
# dotfiles
# Kashev Dalmia | @kashev | kashev.dalmia@gmail.com
# uinstall.sh
#
# Script for setting up a fresh Ubuntu install.

set -e
set -x
sudo -v

# Add Extra PPAs for...
# Sublime Text 3 (Official PPA). Install the key, then install the dev channel.
# NOTE: only works for paid users.
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
echo "deb https://download.sublimetext.com/ apt/dev/" | sudo tee /etc/apt/sources.list.d/sublime-text.list

# Visual Studio Code
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'

# JDK (Web Upd8) - TODO: do we really want this still?
# sudo add-apt-repository -y ppa:webupd8team/java

# Tilix (Web Upd8)
sudo add-apt-repository ppa:webupd8team/terminix

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

# Install Sublime Text 3 (official PPA)
sudo apt -y install sublime-text

# Get Sublime Text to Create Dotfiles Directories
subl
pkill subl
# Install Package Control
wget \
    --directory-prefix="$HOME/.config/sublime-text-3/Installed Packages/" \
    https://sublime.wbond.net/Package%20Control.sublime-package

# Install VS Code
sudo apt -y install code

# Get Visual Studio Code to make Config Directories
code
pkill code

# Install Tilix.
sudo apt -y install tilix
# Add a symlink that tilix will want.
sudo ln -s /etc/profile.d/vte-2.91.sh /etc/profile.d/vte.sh

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

# Install JDK for JetBrains IDEs TODO: do we really want this?
# sudo apt install -y oracle-java8-installer

# Install Google Chrome
sudo apt -y install libxss1 \
                    libappindicator1 \
                    libindicator7

pushd /tmp
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb

# Install Other Utilities
sudo apt -y install htop \
                    gimp \
                    silversearcher-ag \
                    vlc \
                    browser-plugin-vlc \
                    meld \
                    colordiff \
                    filezilla \
                    lftp \
                    bpython \
                    bpython3

# Install SSH Server
sudo apt -y install openssh-server

# Finish Upgrade
sudo apt -y upgrade
