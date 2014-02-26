#!/bin/bash
# Install Script for DH Box

echo ''
echo '#-------------------------------------------#'
echo '#           DH BOX Install Script           #'
echo '#-------------------------------------------#'

export DHBOX_INSTALL_DIR="$HOME/.dhbox"

if [ -d $DHBOX_INSTALL_DIR ]; then
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

echo "$OS is the OS"

if [ "$OS" = "Linux" ]; then
    if [ ! type "$sudo" > /dev/null ]
      then
        apt-get update
        # Gotta have git, and bash completion. Checking if it already exists.
        if ! type "$git" > /dev/null;
          then
            apt-get install -y git-core bash-completion python-zmq
        fi

        # install pip, the python package manager
        wget --no-check-certificate https://raw.github.com/pypa/pip/master/contrib/get-pip.py
        python get-pip.py

        yes | pip install nltk ipython[all]
    else
      sudo apt-get update
      # Gotta have git, and bash completion. Checking if it already exists.
      if ! type "$git" > /dev/null;
        then
          sudo apt-get install -y git-core bash-completion python-zmq
      fi

      # install pip, the python package manager
      sudo wget --no-check-certificate https://raw.github.com/pypa/pip/master/contrib/get-pip.py
      python get-pip.py

      yes | sudo pip install nltk ipython[all]
    fi
elif [ "$OS" = "Darwin" ]; then

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
    if ! type "$wget" > /dev/null;
      then
        brew install wget
    fi

    if ! type "$pip" > /dev/null;
      then
        sudo easy_install pip
    fi
    sudo easy_install pyzmq
    yes | sudo pip install nltk ipython[all]
fi

# Install our scripts
git clone git://github.com/szweibel/dhbox.git $DHBOX_INSTALL_DIR

x=$HOME/.bashrc

# Make backups of bash configuration files
if [ -e $x ]; then
  mv $x "$x"_backup
fi;
# Add our scripts
echo "DHBOX_INSTALL_DIR=$HOME/.dhbox" >> $x
echo "source $DHBOX_INSTALL_DIR/dhbox.sh" >> $x


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


# Install the demo texts
python -m nltk.downloader book

echo 'got it!'
ipython notebook $DHBOX_INSTALL_DIR/test.ipynb