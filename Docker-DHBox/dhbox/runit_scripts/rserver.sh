#!/bin/sh
### In rserver.sh (make sure this file is chmod +x):
# `/sbin/setuser xxxx` runs the given command as the user `xxxx`.
# If you omit that part, the command will be run as root.

sleep 5
echo "Starting R-Studio"
rstudio-server start >>/var/log/rserver.log 2>&1

exec  /usr/lib/rstudio-server/bin/rserver --server-daemonize=0 >>/var/log/rserver.log 2>&1