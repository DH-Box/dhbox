#!/bin/bash
# Install Script for DH Box

echo ''
echo '#-------------------------------------------#'
echo '#           DH BOX Install Script           #'
echo '#-------------------------------------------#'

export INSTALL_DIR="$HOME/.bash/dhbox"
if [ -d $INSTALL_DIR ]; then
  echo "Looks like you have a $INSTALL_DIR directory installed.  Good job!"
  exit
fi;
# Gotta have git
apt-get install -y git

# Install our scripts
git clone git://github.com/szweibel/dhbox.git $INSTALL_DIR

# install pip, the python package manager
wget --no-check-certificate https://raw.github.com/pypa/pip/master/contrib/get-pip.py
python get-pip.py

for x in $HOME/.bashrc $HOME/.profile $HOME/.bash_profile ; do
  if [ -e $x ]; then
    mv $x "$x"_backup
  fi;
  echo "INSTALL_DIR=$HOME/.bash/dhbox" >> $x
  echo "source $INSTALL_DIR/dhbox.sh" >> $x
done