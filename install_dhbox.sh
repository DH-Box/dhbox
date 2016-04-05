#!/bin/bash
apt-get update
apt-get install -y wget python-pip python-dev nodejs nodejs-legacy git build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev npm

parsedVersion=$(echo "${version//./}")
if [[ "$parsedVersion" -lt "300" && "$parsedVersion" -gt "270" ]]
then 
	echo "Python version acceptable"
else
    echo "Please install Python version > 2.7.0 < 3.0"
    exit 1
fi
wget -qO- https://get.docker.com/ | sh
git clone https://github.com/DH-Box/dhbox.git
cd ~/dhbox/
pip install -r requirements.txt
sudo docker pull thedhbox/seed:latest
sudo docker pull thedhbox/twordpress
ln -s /usr/bin/nodejs /usr/bin/node
npm install -g bower gulp
npm install
sudo -u ${USERNAME} bower install --allow-root --no-interactive
gulp build
