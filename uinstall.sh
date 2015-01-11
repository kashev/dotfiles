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
                        python \
                        python-dev \
                        python-pip \
                        pep8 \
                        python-yaml
sudo pip install virtualenvwrapper

# Install Sublime Text 3 (Web Upd8)
sudo apt-get -y install sublime-text-installer
# Get Sublime Text to Create Dotfiles Directories
subl
pkill subl
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
                        nautilus-open-terminal
# Restart nautilus, if it's open.
nautilus -q

# Install LaTeX Things
sudo apt-get -y install texlive \
                        latexmk

# Install SSH Server
sudo apt-get -y install openssh-server

# Finish Upgrade
sudo apt-get -y upgrade
