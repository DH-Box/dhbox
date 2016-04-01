#!/bin/sh
echo "starting file explorer"
exec node-file-manager -p 8081 -d /home 2>&1
