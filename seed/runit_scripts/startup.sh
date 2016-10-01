#!/bin/bash

set -e
if [ -f /etc/configured ]; then
  echo 'already configured'
else
  #code to run only one time...
  adduser --disabled-password --gecos "" $THEUSER
  usermod -a -G sudo $THEUSER
  echo "$THEUSER:$PASS" | chpasswd
  chown -R $THEUSER /anaconda
  date > /etc/configured
fi