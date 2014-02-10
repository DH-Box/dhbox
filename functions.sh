# DH Box Utility Functions

# Apt-install function
apt-install()
{
    apt-get update
    DEBIAN_FRONTEND=noninteractive apt-get -y \
        -o DPkg::Options::=--force-confdef \
        -o DPkg::Options::=--force-confold \
        install $@
}

# Update DH Box
function update-self {
    echo "Updating DH Box..."
    cd $INSTALL_DIR
    git pull origin master
}

# Update apt apps
function update-apt {
    echo "Updating apt..."
    apt-get update
    apt-get upgrade -y
    apt-get autoremove -y
    apt-get autoclean
}

# Lets you ask a command.  Returns '0' on 'yes'
#  ask 'Do you want to rebase?' && git svn rebase || echo 'Rebase aborted'
function ask() {
    echo -n "$@" '[y/n] ' ; read ans
    case "$ans" in
        y*|Y*) return 0 ;;
        *) return 1 ;;
    esac
}

#Check for Root
function needs_root() {
    LUID=$(id -u)
    if [[ $LUID -ne 0 ]]; then
    echo "$0 must be run as root"
    exit 1
    fi
}

# Extract based upon file ext
function extract() {
     if [ -f $1 ] ; then
         case $1 in
             *.tar.bz2)   tar xvjf $1        ;;
             *.tar.gz)    tar xvzf $1     ;;
             *.bz2)       bunzip2 $1       ;;
             *.rar)       unrar x $1     ;;
             *.gz)        gunzip $1     ;;
             *.tar)       tar xvf $1        ;;
             *.tbz2)      tar xvjf $1      ;;
             *.tgz)       tar xvzf $1       ;;
             *.zip)       unzip $1     ;;
             *.Z)         uncompress $1  ;;
             *.7z)        7z x $1    ;;
             *)           echo "'$1' cannot be extracted via >extract<" ;;
         esac
     else
         echo "'$1' is not a valid file"
     fi
}

# Google the parameter
function google () {
  links http://google.com/search?q=$(echo "$@" | sed s/\ /+/g)
}


# echo "Installing R (enough for R Studio Server)"
# sudo aptitude -y install r-base r-base-core r-base-dev r-recommended gdebi-core libapparmor1

# echo "Installing PostgreSQL 9.1"
# sudo aptitude -y install postgresql-9.1 postgresql-client-9.1 postgresql-contrib-9.1 postgresql-doc-9.1 postgresql-server-dev-9.1

# echo "Installing MySQL 5.5"
# sudo aptitude -y install percona-toolkit mysql-client-5.5 mysql-server-5.5 mysql-server-core-5.5 mysql-source-5.5 libmysqlclient-dev
