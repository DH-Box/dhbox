#!/bin/sh

##
# Runit run script for apache2
#

# Activate the Ubuntu Apache environment
. /etc/apache2/envvars

exec /usr/sbin/apache2 -k start -DNO_DETACH