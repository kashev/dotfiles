#!/usr/bin/env zsh
# dotfiles
# Kashev Dalmia | @kashev | kashev.dalmia@gmail.com

###########
# Aliases #
###########

alias sudo='sudo '     # enable use of aliases as sudo

alias bpy="bpython"     # http://bpython-interpreter.org/
alias bpy3="bpython3"   # http://bpython-interpreter.org/
alias pwdp="pwd -P"     # print working directory w/o symlinks
alias cdp="cd `pwd -P`" # change to the physical directory
alias diff="colordiff"  # why would you want diff without colors?

alias vscode="code" # How presumptive that Visual Studio Code is just code.

alias ubuntuversion="lsb_release -a"

# Update dotfiles
alias dotup="git -C ~/sw/dotfiles pull"

# Git Aliases - Mostly for Typo Mitigation
alias gits="git s"     # git s is defined in .gitconfig
alias gs="g s"         # g is defined as git in the oh-my-zsh plugin. Clobbers
                       # gs as ghostscript.
alias gitd="git d"     # git d is defined in .gitconfig
alias gitdd="git dtd"  # git dtd is definted in .gitconfig

# Development Aliases
alias clion="$HOME/sw/clion/bin/clion.sh"
alias pycharm="$HOME/sw/pycharm/bin/pycharm.sh"
alias dj="python manage.py"
alias android-studio="$HOME/sw/android-studio/bin/studio.sh"

# tar Aliases - http://xkcd.com/1168/
alias untar="tar -xvzf"
alias uptar="tar -zcvf"

# My laptop is trash.
alias fixbluetooth="sudo rfkill unblock bluetooth"

# Remove all .pyc files from current working directory.
alias rmpyc="find . -name \*.pyc -delete"

# When using grep, pipe to this to print only the filenames
alias sedfilename="sed 's=.*/=='"

# Python 3 is coming
alias mkvirtualenv3='mkvirtualenv --python=`which python3`'
