#!/bin/bash
############################## auto-run ############################
# Author: Johnny Miller, date: 10:02 PM, Nov.22, 2021              #
# Copyright (c) Johnny Miller                                      #
# Capability: Raspbian GNU/Linux 10 (buster),                      #
#             macOS Monterey 12.0.1 (21A559)                       #
# Purpose:                                                         #
#   1. Integrate easy and simple deployment,                       #
#   2. Reduce memory usage of IntelliJ IDEA to run services,       #
#   3. Improve the efficiency of local development                 #
# Inspiration: https://google.github.io/styleguide/shellguide.html #
####################################################################

# Exit immediately if a command exits with a non-zero status.
# https://stackoverflow.com/questions/19622198/what-does-set-e-mean-in-a-bash-script
set +e

############### Configurable Environment Variables ################
readonly logLevel=INFO
readonly emailMuted=true
readonly headless=false
readonly emailUsername="DEFAULT_EMAIL_USERNAME"
readonly emailPassword="DEFAULT_EMAIL_PASSWORD"
readonly startUpMode="collect johnny"

##################### Functions Declaration #######################
# Bash tips: Colors and formatting (ANSI/VT100 Control sequences) #
# https://misc.flogisoft.com/bash/tip_colors_and_formatting       #
# Pass arguments into a function                                  #
# https://bash.cyberciti.biz/guide/Pass_arguments_into_a_function #
###################################################################

#######################################
# Get formatted date
# Arguments:
#   None
# Returns:
#   Date formatted string like "2020-12-05 08:44:11+0800".
#######################################
function now() {
    date "+%Y-%m-%d %H:%M:%S%z"
}

#######################################
# Log trace. Without any color.
# Arguments:
#   $1 input string.
# Returns:
#   Trace log.
#######################################
function logTrace() {
    printf "$(now) TRACE --- %b\n" "$1"
}

#######################################
# Log info. (GREEN)
# Arguments:
#   $1 input string.
# Returns:
#   Info log.
#######################################
function logInfo() {
    printf "$(now)  \e[32mINFO --- %b\e[0m\n" "$1"
}

#######################################
# Log warn. (YELLOW)
# Arguments:
#   $1 input string.
# Returns:
#   Warn log.
#######################################
function logWarn() {
    printf "$(now)  \e[33mWARN --- %b\e[0m\n" "$1"
}

#######################################
# Log error. (RED)
# Arguments:
#   $1 input string.
# Returns:
#   Error log.
#######################################
function logError() {
    printf "$(now) \e[31mERROR --- %b\e[0m\n" "$1"
}

#######################################
# Git current branch.
# Arguments:
#   None.
# Returns:
#   Current Git branch.
#######################################
function gitCurrentBranch() {
    git rev-parse --abbrev-ref HEAD
}

#######################################
# Git pull.
# Arguments:
#   None.
# Returns:
#   Pull from current branch.
#######################################
function gitPull() {
    git pull
}

#######################################
# Show Python version.
# Arguments:
#   None.
# Returns:
#   Pull from current branch.
#######################################
function showVersion() {
    python3 -V
}

function executePreRunPhase() {
    showVersion
    logWarn "[PRE-RUN] Current Git branch: $(gitCurrentBranch), pulling codes from Git…"
    gitPull
    logWarn "[PRE-RUN] Current directory: $(pwd), list of current directory:"
    ls -l -h -a
    pipenvOutput=`pipenv shell 2>&1`
    activated=`echo $pipenvOutput | grep -c "already activated"`
    if [ "$activated" -eq 1 ];
    then
        logWarn "[PRE-RUN] $pipenvOutput"
    else
        logInfo "[PRE-RUN] Just activated pipenv virtual environment"
    fi
}

function executeRunPhase() {
    logInfo "Runtime environment variables:\nLOG_LEVEL=$logLevel,\nEMAIL_MUTED=$emailMuted,\nHEADLESS=$headless,\nEMAIL_USERNAME=$emailUsername,\nEMAIL_PASSWORD=$emailPassword,\nSTART_UP_MODE=$startUpMode"\
    # shellcheck disable=SC2086
    LOG_LEVEL=$logLevel EMAIL_MUTED=$emailMuted HEADLESS=$headless EMAIL_USERNAME=$emailUsername EMAIL_PASSWORD=$emailPassword python3 -m home_guardian $startUpMode || {
        homeGuardianResult=$?
        logError "[RUN] Home Guardian exited with non-zero status: $homeGuardianResult"
        exit $homeGuardianResult
    }
    logInfo "[RUN] Home Guardian exited with status: $?"
}

################### MAIN PROCEDURE START ###################
clear
# Pre-run phase
executePreRunPhase
# Run phase
executeRunPhase
