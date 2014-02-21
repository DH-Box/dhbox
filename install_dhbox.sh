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
# Gotta have git, and dependencies!
apt-get install libcurl4-gnutls-dev libexpat1-dev gettext \
  libz-dev libssl-dev git
yes
git clone git://github.com/szweibel/dhbox.git $INSTALL_DIR
for x in $HOME/.bashrc $HOME/.profile $HOME/.bash_profile ; do
  if [ -e $x ]; then
    mv $x "$x"_backup
  fi;
  echo "INSTALL_DIR=$HOME/.bash/dhbox" >> $x
  echo "source $INSTALL_DIR/dhbox.sh" >> $x
done