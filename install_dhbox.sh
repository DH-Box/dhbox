#!/bin/bash
apt-get update
ret=`python -c 'import sys; print("%i" % (sys.hexversion<0x03000000))'`

if [ $ret ]; then
	echo "Python exists"
else
	echo "requires Python"
	exit 1
fi
if [ $ret -eq 0 ]; then
    echo "requires Python version < 3"
    exit 1
else 
    echo "Python version is < 3"
fi
apt-get install -y wget python-pip python-dev nodejs nodejs-legacy git build-essential checkinstall libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev npm

wget -qO- https://get.docker.com/ | sh
git clone https://github.com/DH-Box/dhbox.git
cd ~/dhbox/
pip install -r requirements.txt
sudo docker pull thedhbox/seed:latest
# sudo docker pull thedhbox/twordpress
sudo manage build_database
ln -s /usr/bin/nodejs /usr/bin/node
npm install -g bower gulp
sudo -u ${USERNAME} bower install --allow-root --no-interactive
echo "DH Box successfully installed!"
# gulp build
