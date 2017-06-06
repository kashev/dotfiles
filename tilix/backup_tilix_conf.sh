#!/usr/bin/env bash
# Command to backup tilix configuration from dconf to file.
dconf dump /com/gexperts/Tilix/ > tilix.dconf
