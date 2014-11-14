#!/bin/sh
### In rserver.sh (make sure this file is chmod +x):
# `/sbin/setuser xxxx` runs the given command as the user `xxxx`.
# If you omit that part, the command will be run as root.
echo "Starting R-Studio"
exec sudo rstudio-server start
exec  /usr/lib/rstudio-server/bin/rserver >>/var/log/rserver.log 2>&1