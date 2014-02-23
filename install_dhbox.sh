#!/bin/bash
# Install Script for DH Box

echo ''
echo '#-------------------------------------------#'
echo '#           DH BOX Install Script           #'
echo '#-------------------------------------------#'

export INSTALL_DIR="$HOME/.bash/dhbox"

if [ -d $INSTALL_DIR ]; then
  echo "Looks like you already have DH Box installed.  Good job!"
  exit
fi;

# Detect the platform (similar to $OSTYPE)
OS="`uname`"
case $OS in
  'Linux')
    OS='Linux'
    alias ls='ls --color=auto'
    ;;
  'FreeBSD')
    OS='FreeBSD'
    alias ls='ls -G'
    ;;
  'Windows')
    OS='Windows'
    ;;
  'darwin')
    OS='Mac'
    ;;
  'SunOS')
    OS='Solaris'
    ;;
  'AIX') ;;
  *) ;;
esac

if [OS -eq 'Linux']
  then
    apt-get update
    # Gotta have git, and bash completion. Checking if it already exists.
    if ! type "$git" > /dev/null;
      then
        apt-get install -y git-core bash-completion
    fi
    # need this weird lib
    apt-get install python-zmq
elif [OS -eq 'Mac']
  then
    # install Mac Homebrew for easy installation of other stuff. Check if it exists.
    if ! type "$brew" > /dev/null;
      then
        ruby -e "$(curl -fsSL https://raw.github.com/Homebrew/homebrew/go/install)"
    fi
    # Gotta have git. Check for it.
    if ! type "$git" > /dev/null;
      then
        brew install git
    fi
fi

# Install our scripts
git clone git://github.com/szweibel/dhbox.git $INSTALL_DIR

# install pip, the python package manager
wget --no-check-certificate https://raw.github.com/pypa/pip/master/contrib/get-pip.py
python get-pip.py

x=$HOME/.bashrc

# Make backups of bash configuration files
if [ -e $x ]; then
  mv $x "$x"_backup
fi;
# Add our scripts
echo "INSTALL_DIR=$HOME/.bash/dhbox" >> $x
echo "source $INSTALL_DIR/dhbox.sh" >> $x


# Virtualenv not working!
# if not Debian
# pip install virtualenvwrapper
# if Debian
# pip install virtualenv
# apt-get install virtualenvwrapper
# echo "export WORKON_HOME=$HOME/.virtualenvs" >> $x
# echo "export PROJECT_HOME=$HOME/Devel" >> $x
# if not Debian
# echo "source /usr/local/bin/virtualenvwrapper.sh" >> $x
# if Debian
# echo "source /etc/bash_completion.d/virtualenvwrapper" >> $x

# Reloading startup file
echo "source ~/.bashrc"
# Making the dhbox virtualenv
# mkvirtualenv dhbox

yes | pip install nltk ipython
echo 'got it!'
ipython notebook $INSTALL_DIR/test.ipynb