#!/bin/bash

set -e
if [ -f /etc/configured ]; then
  echo 'already configured'
else
  #code to run only one time...
  # wget -O /tmp/install.html --post-data "username=$THEUSER&password=$PASS&password_confirm=$PASS&super_email=$EMAIL&administrator_email=$EMAIL&site_title=DHBox&description=DHBox&copyright=2014&author=DHBOX&tag_delimiter=,&fullsize_constraint=800&thumbnail_constraint=200&square_thumbnail_constraint=200&per_page_admin=10&per_page_public=10&show_empty_elements=0&path_to_convert=/usr/bin&install_submit=Install" localhost:8080/install/install.php
  adduser --disabled-password --gecos "" $THEUSER
  usermod -a -G sudo $THEUSER
  echo "$THEUSER:$PASS" | chpasswd
  date > /etc/configured
  # rm -- "$0"
fi