#!/bin/bash

set -e
if [ -f /etc/configured ]; then
  echo 'already configured'
else
  #code to run only one time...
  adduser --disabled-password --gecos "" $THEUSER
  usermod -a -G sudo $THEUSER
  echo "$THEUSER:$PASS" | chpasswd
  usermod -a -G dhbox $THEUSER
  date > /etc/configured
fi