#!/bin/sh

##
# Runit run script for apache2
#

# # Activate the Ubuntu Apache environment
# . /etc/apache2/envvars
# # source /etc/apache2/envvars 
# apache2 -V

# exec /usr/sbin/apache2 -k start -DNO_DETACH
[ ! -d ${APACHE_RUN_DIR:-/var/run/apache2} ] && mkdir -p ${APACHE_RUN_DIR:-/var/run/apache2}
[ ! -d ${APACHE_LOCK_DIR:-/var/lock/apache2} ] && mkdir -p ${APACHE_LOCK_DIR:-/var/lock/apache2} && chown ${APACHE_RUN_USER:-www-data} ${APACHE_LOCK_DIR:-/var/lock/apache2}
exec /usr/sbin/apache2 -e debug >> /var/log/apache.log 2>&1