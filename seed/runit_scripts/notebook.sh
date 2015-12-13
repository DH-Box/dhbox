#!/bin/sh
### In notebook.sh (make sure this file is chmod +x):
# `/sbin/setuser xxxx` runs the given command as the user `xxxx`.
# If you omit that part, the command will be run as root.

echo "Starting Jupyter Notebook"
cd /home
exec jupyter notebook --no-browser --port 8888 --ip='*'