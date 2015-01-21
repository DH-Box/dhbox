#!/bin/sh
### In rserver.sh (make sure this file is chmod +x):
# `/sbin/setuser xxxx` runs the given command as the user `xxxx`.
# If you omit that part, the command will be run as root.
sleep 5
echo "Starting Shellinabox"
# sudo service shellinabox start >>/var/log/shellinabox.log 2>&1
shellinaboxd -t >>/var/log/shellinabox.log 2>&1