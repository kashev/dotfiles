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

alias ubuntuversion="lsb_release -a"

# Update dotfiles
alias dotup="git -C ~/sw/dotfiles pull"

# Git Aliases - Mostly for Typo Mitigation
alias gits="git s"     # git s is defined in .gitconfig
alias gs="g s"         # g is defined as git in the oh-my-zsh plugin. Clobbers
                       # gs as ghostscript.
alias gitd="git d"     # git d is defined in .gitconfig

# SVN Aliases - To Make SVN More Like Git
alias svnlog="svn log | less"

# Development Aliases
alias clion="$HOME/sw/clion/bin/clion.sh"
alias dj="python manage.py"
alias android-studio="$HOME/sw/android-studio/bin/studio.sh"

# tar Aliases - http://xkcd.com/1168/
alias untar="tar -xvzf"
alias uptar="tar -zcvf"

alias fixbluetooth="sudo rfkill unblock bluetooth"
