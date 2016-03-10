#!/bin/sh
### In rserver.sh (make sure this file is chmod +x):
# `/sbin/setuser xxxx` runs the given command as the user `xxxx`.
# If you omit that part, the command will be run as root.
sleep 5
echo "Starting Wetty"
exec wetty -p 3000 2>&1