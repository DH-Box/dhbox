#!/bin/bash
# Install Script for DH Box

echo ''
echo '#-------------------------------------------#'
echo '#           DH BOX Install Script           #'
echo '#-------------------------------------------#'

# make sure a bash profile exists, create one if it doesn't
touch $HOME/.profile
touch $HOME/.bashrc

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

if [ "$OS" = "Linux" ];
  then
    if hash sudo 2>/dev/null;
      then
        # For Ubuntu
        THE_OS="Ubuntu"
        echo "Installing for Ubuntu"
        sudo apt-get update
        # Gotta have git, and pip. Checking if it already exists.
        if ! type "$git" > /dev/null;
          then
            sudo apt-get install -y git-core python-pip python-zmq python-matplotlib python-virtualenv
        fi
        . $HOME/.profile

        # Installing virtualenv and virtualenvwrapper
        # mkdir $HOME/.virtualenvs
        # yes | sudo pip install virtualenvwrapper
        # . /usr/local/bin/virtualenvwrapper.sh
        # export WORKON_HOME=$HOME/.virtualenvs
        # . $HOME/.profile
        # mkvirtualenv dhbox
        # Installing our tools
        yes | sudo pip install nltk ipython[all] tornado jinja2
    else
      # DEBIAN DOES NOT HAVE VIRTUALENV YET
      # For Debian
      THE_OS="Debian"
      echo "Installing for Debian"
        apt-get update
        # Gotta have git, and bash completion. Checking if it already exists.
        if ! hash git 2>/dev/null;
          then
            echo "Installing Git"
            apt-get install -y git-core bash-completion python-zmq python-matplotlib
        fi

        if ! hash pip 2>/dev/null;
          then
            echo "Installing Pip"
            # install pip, the python package manager
            wget --no-check-certificate https://raw.github.com/pypa/pip/master/contrib/get-pip.py
            python get-pip.py
        fi
        source $HOME/.profile
        # Installing our tools
        yes | pip install nltk ipython[all]
    fi
elif [ "$OS" = "Darwin" ]; then
    # For Mac
    echo "Installing for Mac"
    THE_OS="Mac"
    # Get correct permissions for Homebrew
    sudo chown 'whoami' usr/local/lib/
    # install Mac Homebrew for easy installation of other stuff.
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
    . $HOME/.profile
    # Installing virtualenv and virtualenvwrapper
    sudo pip install virtualenv
    sudo pip install virtualenvwrapper
    . `which virtualenvwrapper.sh`
    mkvirtualenv dhbox

    # Installing our tools
    sudo easy_install pyzmq
    brew tap Homebrew/python
    yes | pip install pyparsing python-dateutil
    brew install freetype
    brew install pkg-config
    yes | pip install nltk ipython[all] matplotlib
    # Install matplotlib for charts
else
  echo "Unfortunately $OS isn't supported yet. Exiting..."
  exit
fi
# Install our scripts
echo "Installing DH Box into $DHBOX_INSTALL_DIR"
git clone git://github.com/szweibel/dhbox.git $DHBOX_INSTALL_DIR

VIRTLOCATION="which virtualenvwrapper.sh"
# Make backups of bash configuration files
for x in $HOME/.bashrc $HOME/.profile $HOME/.bash_profile ;
do
    if [ -e $x ]; then
      mv $x "$x"_backup
      # Add our scripts
      echo "DHBOX_INSTALL_DIR=$HOME/.dhbox" >> $x
    fi;
done
# Reloading startup file
if [ $THE_OS = "Ubuntu" ]; then
  . $HOME/.profile
  . $HOME/.bashrc
  echo ". $DHBOX_INSTALL_DIR/dhbox.sh" >> $HOME/.bashrc
  echo ". $DHBOX_INSTALL_DIR/dhbox.sh" >> $HOME/.profile
else
  echo "source $DHBOX_INSTALL_DIR/dhbox.sh" >> $HOME/.bashrc
  echo "source $DHBOX_INSTALL_DIR/dhbox.sh" >> $HOME/.profile
  source $HOME/.profile
  source $HOME/.bashrc
fi
# Delete all .pyc files?
# find / -iname \*.pyc -exec rm {} \;
# Install the demo texts
python -m nltk.downloader book
echo 'got it!'
ipython notebook $HOME/.dhbox/notebooks/the-waves