#!/bin/bash
# DH Box Main Shell Script

# start DH Box
function dhbox {
    echo "Starting..."
    # workon dhbox
    ipython notebook $HOME/.dhbox/notebooks/the-waves
}

# Update DH Box
function update-self {
    echo "Updating DH Box..."
    cd $HOME/.dhbox
    git pull origin master
}
