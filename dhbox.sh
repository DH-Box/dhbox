#!/bin/bash
# DH Box Main Shell Script

# start DH Box
function dhbox (){
    echo "Starting..."
    ipython notebook $DHBOX_INSTALL_DIR/test.ipynb
}

# Update DH Box
function update-self {
    echo "Updating DH Box..."
    cd $DHBOX_INSTALL_DIR
    git pull origin master
}

# Google the parameter
function google () {
  links http://google.com/search?q=$(echo "$@" | sed s/\ /+/g)
}

