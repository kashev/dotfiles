#!/usr/bin/env zsh
# dotfiles
# Kashev Dalmia | @kashev | kashev.dalmia@gmail.com

###########
# Aliases #
###########

alias sudo='sudo '     # enable use of aliases as sudo

alias pwdp="pwd -P"     # print working directory w/o symlinks
alias cdp="cd `pwd -P`" # change to the physical directory
alias diff="colordiff"  # why would you want diff without colors?

# Versions
alias ubuntuversion="lsb_release -a"
alias osxversion="uname -a"

# Git Aliases - Mostly for Typo Mitigation
alias gits="git s"     # git s is defined in .gitconfig
alias gs="g s"         # g is defined as git in the oh-my-zsh plugin. Clobbers gs as ghostscript.
alias gitd="git d"     # git d is defined in .gitconfig
alias gitdd="git dtd"  # git dtd is definted in .gitconfig

# tar Aliases - http://xkcd.com/1168/
alias untar="tar -xvzf"
alias uptar="tar -zcvf"

# When using grep, pipe to this to print only the filenames
alias sedfilename="sed 's=.*/=='"

# Python
alias mkvirtualenv3='mkvirtualenv --python=`which python3`'
alias bpy="bpython"     # http://bpython-interpreter.org/
alias rmpyc="find . -name \*.pyc -delete"  # Remove all .pyc files from current working directory.

# Programs
alias vscode="code"

# OSX Specific stuff
uname -a | grep 'Darwin' &> /dev/null
if [ $? -eq 0 ]; then
    alias chrome="open -a 'Google Chrome'"
fi