#!/usr/bin/env bash

# Abort if a command fails!
set -e

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ ! -n "$HOST" ];then
    echo "missing option \"HOST\", aborting"
    exit 1
fi
if [ ! -n "$USER" ];then
    echo  "missing option \"USER\", aborting"
    exit 1
fi
if [ ! -n "$PASSWORD" ];then
    echo  "missing option \"PASSWORD\", aborting"
    exit 1
fi

if [ ! -n "$DIRECTORY" ];then
    echo  "missing option \"DIRECTORY\", aborting"
    exit 1
fi

# Go into the directory, where the site was generated
cd "$DIR/_site/"


echo "Uploading..."
# TODO: SSL does currently not work on cyon :(

# lftp -d -e "
# open $HOST
# set ftp:ssl-auth TLS
# set ftp:ssl-allow true
# set ssl:verify-certificate yes
# set ssl:check-hostname off
# set ftp:ssl-protect-data true
# set cmd:fail-exit true
# user \"$USER\" \"$PASSWORD\"
# mirror --reverse --delete --ignore-time --verbose --parallel . .
# bye
# "
echo "BROKEN!"

# Complete!
echo "Done!"
exit 0
