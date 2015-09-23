#!/bin/bash
apt-get update
apt-get install wget pip nodejs nodejs-legacy git build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev npm
cd ~/Downloads/
wget http://python.org/ftp/python/2.7.5/Python-2.7.5.tgz
tar -xvf Python-2.7.5.tgz
cd Python-2.7.5
./configure
make
cd ~/
wget -qO- https://get.docker.com/ | sh
git clone https://github.com/DH-Box/dhbox.git
cd ~/dhbox/
pip install -r requirements.txt
cd ~/dhbox/seed/
sudo docker build -t dhbox/seed:latest .
cd ~/dhbox/
npm install -g bower gulp
npm install
sudo -u ${USERNAME} bower install --allow-root
gulp build
