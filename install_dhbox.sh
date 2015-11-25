#!/bin/bash
apt-get update
apt-get install -y wget python-pip nodejs nodejs-legacy git build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev npm python-pip
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
cd seed/
sudo docker build -t thedhbox/seed:latest .
cd ../lamp-seed/
sudo docker build -t tlamp .
cd ../wp-seed/
sudo docker build -t twordpress .
cd ~/dhbox/
ln -s /usr/bin/nodejs /usr/bin/node
npm install -g bower gulp
npm install
sudo -u ${USERNAME} bower install --allow-root --no-interactive
gulp build
