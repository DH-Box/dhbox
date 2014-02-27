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

if [ "$OS" = "Linux" ];
  then
    if ! type "$sudo" > /dev/null;
      then
        # For Ubuntu
        sudo apt-get update
        # Gotta have git, and pip. Checking if it already exists.
        if ! type "$git" > /dev/null;
          then
            sudo apt-get install -y git-core python-pip python-zmq
        fi
        source $HOME/.bashrc
        # Installing virtualenv and virtualenvwrapper
        sudo pip install virtualenv
        mkdir $HOME/.virtualenvs
        sudo pip install virtualenvwrapper
        export WORKON_HOME=$HOME/.virtualenvs
        source $HOME/.bashrc
        # Installing our tools
        yes | sudo pip install nltk ipython[all] tornado jinja2
    else
      # For Debian
        apt-get update
        # Gotta have git, and bash completion. Checking if it already exists.
        if ! type "$git" > /dev/null;
          then
            apt-get install -y git-core bash-completion python-zmq
        fi

        if ! type "$pip" > /dev/null;
          then
            # install pip, the python package manager
            wget --no-check-certificate https://raw.github.com/pypa/pip/master/contrib/get-pip.py
            python get-pip.py
        fi
        source $HOME/.bashrc
        # Installing our tools
        yes | pip install nltk ipython[all]
    fi
elif [ "$OS" = "Darwin" ]; then
    # For Mac
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
    source $HOME/.bashrc
    # Installing virtualenv and virtualenvwrapper
    sudo pip install virtualenv
    sudo pip install virtualenvwrapper
    source `which virtualenvwrapper.sh`
    mkvirtualenv dhbox

    # Installing our tools
    sudo easy_install pyzmq
    yes | sudo pip install nltk ipython[all]
else
  echo "Unfortunately $OS isn't supported yet. Exiting..."
  exit
fi

# Install our scripts
git clone git://github.com/szweibel/dhbox.git $DHBOX_INSTALL_DIR

# Make backups of bash configuration files
x=$HOME/.bashrc
if [ -e $x ]; then
  mv $x "$x"_backup
fi;
# Add our scripts

echo "DHBOX_INSTALL_DIR=$HOME/.dhbox" >> $x
echo "source $DHBOX_INSTALL_DIR/dhbox.sh" >> $x
echo "export WORKON_HOME=$HOME/.virtualenvs" >> $x
echo "source `which virtualenvwrapper.sh`" >> $x


# if [ "$OS" = "Linux" ]; then
#   if ! type "$sudo" > /dev/null;
#     then
#       # For Ubuntu
#   else
#     # For Debian
#   fi
# elif  [ "$OS" = "Darwin" ]; then

# fi

# Reloading startup file
echo "source $HOME/.bashrc"
# Making the dhbox virtualenv
# mkvirtualenv dhbox
# Delete all .pyc files?
# find / -iname \*.pyc -exec rm {} \;

# Install the demo texts
python -m nltk.downloader book

echo 'got it!'
ipython notebook $DHBOX_INSTALL_DIR/test.ipynb