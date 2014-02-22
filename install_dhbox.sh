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
# Gotta have git, and bash completion
apt-get install -y git bash-completion

# Install our scripts
git clone git://github.com/szweibel/dhbox.git $INSTALL_DIR

# install pip, the python package manager
wget --no-check-certificate https://raw.github.com/pypa/pip/master/contrib/get-pip.py
python get-pip.py

# Virtualenv not working!
# if not Debian
# pip install virtualenvwrapper
# if Debian
# pip install virtualenv
# apt-get install virtualenvwrapper

x=$HOME/.bashrc

if [ -e $x ]; then
  mv $x "$x"_backup
fi;
echo "INSTALL_DIR=$HOME/.bash/dhbox" >> $x
echo "source $INSTALL_DIR/dhbox.sh" >> $x
echo "export WORKON_HOME=$HOME/.virtualenvs" >> $x
echo "export PROJECT_HOME=$HOME/Devel" >> $x

# if not Debian
# echo "source /usr/local/bin/virtualenvwrapper.sh" >> $x

# if Debian
# echo "source /etc/bash_completion.d/virtualenvwrapper" >> $x

# Reloading startup file
echo "source ~/.bashrc"

# Making the dhbox virtualenv
mkvirtualenv dhbox
yes | pip install nltk ipython
echo 'got it!'