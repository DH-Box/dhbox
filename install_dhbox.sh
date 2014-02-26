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
    apt-get update
    # Gotta have git, and bash completion. Checking if it already exists.
    if ! type "$git" > /dev/null;
      then
        apt-get install -y git-core bash-completion python-zmq
    fi
elif [ "$OS" = "Darwin" ]; then
    # get xcode command line tools

    OSX_VERS=$(sw_vers -productVersion | awk -F "." '{print $2}')

    # Get Xcode CLI tools
    # https://devimages.apple.com.edgekey.net/downloads/xcode/simulators/index-3905972D-B609-49CE-8D06-51ADC78E07BC.dvtdownloadableindex
    TOOLS=clitools.dmg
    if [ ! -f "$TOOLS" ]; then
      if [ "$OSX_VERS" -eq 7 ]; then
          DMGURL=http://devimages.apple.com/downloads/xcode/command_line_tools_for_xcode_os_x_lion_april_2013.dmg
      elif [ "$OSX_VERS" -eq 8 ]; then
          DMGURL=http://devimages.apple.com/downloads/xcode/command_line_tools_for_xcode_os_x_mountain_lion_april_2013.dmg
      elif [ "$OSX_VERS" -eq 9 ]; then
          DMGURL=http://adcdownload.apple.com/Developer_Tools/command_line_tools_os_x_mavericks_for_xcode__late_october_2013/command_line_tools_os_x_mavericks_for_xcode__late_october_2013.dmg
      fi
      curl "$DMGURL" -o "$TOOLS"
    fi
    TMPMOUNT=`/usr/bin/mktemp -d /tmp/clitools.XXXX`
    hdiutil attach "$TOOLS" -mountpoint "$TMPMOUNT"
    installer -pkg "$(find $TMPMOUNT -name '*.mpkg')" -target /
    hdiutil detach "$TMPMOUNT"
    rm -rf "$TMPMOUNT"
    rm "$TOOLS"

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
echo "DHBOX_INSTALL_DIR=$HOME/.dhbox" >> $x
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

yes | pip install nltk ipython[all]
echo 'got it!'
ipython notebook $INSTALL_DIR/test.ipynb