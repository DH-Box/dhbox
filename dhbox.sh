#!/bin/bash
# DH Box Main Shell Script

# start DH Box
function dhbox {
    echo "Starting..."
    workon dhbox
    ipython notebook $DHBOX_INSTALL_DIR/notebooks/the-waves
}

# Update DH Box
function update-self {
    echo "Updating DH Box..."
    cd $DHBOX_INSTALL_DIR
    git pull origin master
}
