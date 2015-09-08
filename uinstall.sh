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
# Update PPA list
sudo apt-get -y update

# Get Required Dotfiles Packages
sudo apt-get -y install git \
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
sudo apt-get -y install sublime-text-installer
# Get Sublime Text to Create Dotfiles Directories
subl
pkill subl
# Install Package Control
wget \
    --directory-prefix="$HOME/.config/sublime-text-3/Installed Packages/" \
    https://sublime.wbond.net/Package%20Control.sublime-package
# Clone Dotfiles
mkdir ~/sw
cd ~/sw
git clone https://github.com/kashev/dotfiles.git
cd dotfiles
python install.py -vf


# Install Gnome 3
sudo apt-get -y install gnome-shell \
                        ubuntu-gnome-desktop

# Install JDK for JetBrains IDEs
sudo apt-get install -y oracle-java8-installer

# Install Google Chrome
sudo apt-get -y install libxss1 \
                        libappindicator1 \
                        libindicator7
cd /tmp
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb

# Install Other Utilities
sudo apt-get -y install htop \
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
sudo apt-get -y install texlive \
                        latexmk \
                        texlive-latex-extra \
                        texlive-science

# Install SSH Server
sudo apt-get -y install openssh-server

# Finish Upgrade
sudo apt-get -y upgrade
