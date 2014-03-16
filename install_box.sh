#! /bin/sh
#

# Update packages
sudo apt-get update -y && sudo apt-get dist-upgrade -y && sudo apt-get upgrade -y && sudo apt-get install -y unattended-upgrades python-pip

# Make a source directory for DHBox
sudo mkdir /dhbox
sudo mkdir /dhbox/mallet

# Install Amazon Cloud scripts
sudo wget --no-check-certificate -P /root https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz
sudo mkdir -p /root/aws-cfn-bootstrap-latest
sudo tar xvfz /root/aws-cfn-bootstrap-latest.tar.gz --strip-components=1 -C /root/aws-cfn-bootstrap-latest
sudo easy_install /root/aws-cfn-bootstrap-latest
sudo cfn-init -s DHBox --region us-east-1 -r NewServer

# Install ipython
yes | sudo pip install nltk ipython[all]

# Install MALLET
sudo wget --no-check-certificate -P /dhbox http://mallet.cs.umass.edu/dist/mallet-2.0.7.tar.gz
sudo tar xvfz /dhbox/mallet-2.0.7.tar.gz --strip-components=1 -C /dhbox/mallet
sudo ant -buildfile /dhbox/mallet/build.xml

sudo reboot
