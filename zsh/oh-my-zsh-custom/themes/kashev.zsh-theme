#!/usr/bin/env zsh
# dotfiles
# Kashev Dalmia | @kashev | kashev.dalmia@gmail.com
# kashev.zsh-theme
#
# Custom theme for oh-my-zsh, based on gnzh (based on bira), with parts
# lovingly stolen from the following themes:
#
# gnzh - base theme
# mortalscumbag - dots for git status
# minimal - svn status as well, dots
# 3den - time

# Load Color Modules
autoload -U colors zsh/terminfo # Used in the color alias below
colors
# Allow for functions in the prompt.
setopt prompt_subst

# Easier Color Aliases
for color in RED GREEN YELLOW BLUE MAGENTA CYAN WHITE; do
    eval PR_$color='%{$fg[${(L)color}]%}'
done
eval PR_NO_COLOR="%{$terminfo[sgr0]%}"
eval PR_BOLD="%{$terminfo[bold]%}"

# PWD Function
# http://stevelosh.com/blog/2010/02/my-extravagant-zsh-prompt/
function get_pwd() {
    echo "${PWD/$HOME/~}"
}

# Virual Env Function
# http://stevelosh.com/blog/2010/02/my-extravagant-zsh-prompt/
function virtualenv_info {
    [ $VIRTUAL_ENV ] && echo '('`basename $VIRTUAL_ENV`') '
}

# Git Stuff
# mortalscumbag
function my_git_prompt() {
  tester=$(git rev-parse --git-dir 2> /dev/null) || return

  INDEX=$(git status --porcelain 2> /dev/null)
  STATUS=""

  # is branch ahead?
  if $(echo "$(git log origin/$(current_branch)..HEAD 2> /dev/null)" | grep '^commit' &> /dev/null); then
    STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_AHEAD"
  fi

  # is anything staged?
  if $(echo "$INDEX" | grep -E -e '^(D[ M]|[MARC][ MD]) ' &> /dev/null); then
    STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_STAGED"
  fi

  # is anything unstaged?
  if $(echo "$INDEX" | grep -E -e '^[ MARC][MD] ' &> /dev/null); then
    STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_UNSTAGED"
  fi

  # is anything untracked?
  if $(echo "$INDEX" | grep '^?? ' &> /dev/null); then
    STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_UNTRACKED"
  fi

  # is anything unmerged?
  if $(echo "$INDEX" | grep -E -e '^(A[AU]|D[DU]|U[ADU]) ' &> /dev/null); then
    STATUS="$STATUS$ZSH_THEME_GIT_PROMPT_UNMERGED"
  fi

  if [[ -n $STATUS ]]; then
    STATUS=" $STATUS"
  fi

  echo "$ZSH_THEME_GIT_PROMPT_PREFIX$(my_current_branch)$STATUS$ZSH_THEME_GIT_PROMPT_SUFFIX"
}

function my_current_branch() {
  echo $(current_branch || echo "(no branch)")
}

# Set User and Host, with Color

# Check the UID
if [[ $UID -ne 0 ]]; then # normal user
    eval PR_USER='${PR_GREEN}%n${PR_NO_COLOR}'
    eval PR_USER_OP='${PR_GREEN}%#${PR_NO_COLOR}'
    local PR_PROMPT='$PR_NO_COLOR➤$PR_NO_COLOR'
else # root
    eval PR_USER='${PR_RED}%n${PR_NO_COLOR}'
    eval PR_USER_OP='${PR_RED}%#${PR_NO_COLOR}'
    local PR_PROMPT='$PR_RED➤$PR_NO_COLOR'
fi

# Check if we are on SSH or not
if [[ -n "$SSH_CLIENT"  ||  -n "$SSH2_CLIENT" ]]; then
    eval PR_HOST='${PR_YELLOW}%M${PR_NO_COLOR}' #SSH
else
    eval PR_HOST='${PR_GREEN}%M${PR_NO_COLOR}' # no SSH
fi

# Return Code
local return_code="%(?..%{$PR_RED%}%? ↵%{$PR_NO_COLOR%})"

local user_host='${PR_USER}\
${PR_WHITE}\
@\
${PR_NO_COLOR}\
${PR_HOST}'

local current_dir='%{$PR_BLUE%}\
$(get_pwd)\
%{$PR_NO_COLOR%}'

local git_branch='$(my_git_prompt)%{$PR_NO_COLOR%}'

ZSH_THEME_GIT_PROMPT_PREFIX="%{$PR_YELLOW%}[ "
ZSH_THEME_GIT_PROMPT_SUFFIX=" %{$PR_NO_COLOR$PR_YELLOW%}]%{$PR_NO_COLOR%}"
ZSH_THEME_GIT_PROMPT_AHEAD="%{$PR_BOLD$PR_MAGENTA%}↑"
ZSH_THEME_GIT_PROMPT_STAGED="%{$PR_BOLD$PR_GREEN%}●"
ZSH_THEME_GIT_PROMPT_UNSTAGED="%{$PR_BOLD$PR_YELLOW%}●"
ZSH_THEME_GIT_PROMPT_UNTRACKED="%{$PR_BOLD$PR_RED%}●"
ZSH_THEME_GIT_PROMPT_UNMERGED="%{$PR_BOLD$PR_RED%}✕"

# Configure SVN information like Git Configuration
ZSH_THEME_SVN_PROMPT_PREFIX=$ZSH_THEME_GIT_PROMPT_PREFIX
ZSH_THEME_SVN_PROMPT_SUFFIX=$ZSH_THEME_GIT_PROMPT_SUFFIX
ZSH_THEME_SVN_PROMPT_DIRTY=$ZSH_THEME_GIT_PROMPT_DIRTY
ZSH_THEME_SVN_PROMPT_CLEAN=$ZSH_THEME_GIT_PROMPT_CLEAN

# Set the Prompts
PROMPT="\
╭── ${user_host} ${current_dir} ${git_branch} $(virtualenv_info)
╰─$PR_PROMPT "
RPROMPT="${return_code} %D{[%I:%M:%S]}"
