#! /bin/sh
#

# Update packages
apt-get update && apt-get dist-upgrade

# Make a source directory for DHBox
sudo mkdir ~/dhbox/mallet

# Install Amazon Cloud scripts
wget --no-check-certificate -P /root https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz
mkdir -p /root/aws-cfn-bootstrap-latest
tar xvfz /root/aws-cfn-bootstrap-latest.tar.gz --strip-components=1 -C /root/aws-cfn-bootstrap-latest
easy_install /root/aws-cfn-bootstrap-latest
sudo cfn-init -s DHBox --region us-east-1 -r NewServer
sudo rm /etc/init.d/startup.sh

# Install MALLET
wget --no-check-certificate -P ~/dhbox http://mallet.cs.umass.edu/dist/mallet-2.0.7.tar.gz
tar xvfz /dhbox/mallet-2.0.7.tar.gz --strip-components=1 -C ~/dhbox/mallet
sudo ant -buildfile /dhbox/mallet/build.xml

sudo reboot
