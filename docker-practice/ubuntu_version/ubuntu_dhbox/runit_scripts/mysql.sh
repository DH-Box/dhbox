#!/bin/sh -e
echo "starting mysql"
exec 2>&1
exec mysqld_safe --console --user=mysql