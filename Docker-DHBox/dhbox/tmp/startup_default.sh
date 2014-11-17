#!/bin/bash
## A script to run once, the first time a container runs.
set -e

if [ -f /etc/configured ]; then
  echo 'already configured'
else
  #code that needs to run only once
  #needed to fix problems with ubuntu and cron
  update-locale
  date > /etc/configured
  # start apache and give Omeka our user's info
  sudo service apache2 restart
  sudo service mysql start
  wget -O /tmp/install.html --post-data "username=user&password=password&password_confirm=password&super_email=dhbox@dhbox.org&administrator_email=dhbox@dhbox.org&site_title=DHBox&description=DHBox&copyright=2014&author=DHBOX&tag_delimiter=,&fullsize_constraint=800&thumbnail_constraint=200&square_thumbnail_constraint=200&per_page_admin=10&per_page_public=10&show_empty_elements=0&path_to_convert=/usr/bin&install_submit=Install" localhost:8080/install/install.php
  sudo service apache2 stop
  sudo service mysql stop
  
  date > /etc/configured
fi