#! /bin/sh
# /etc/init.d/startup
#
apt-get update && apt-get dist-upgrade
wget --no-check-certificate -P /root https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.tar.gz
mkdir -p /root/aws-cfn-bootstrap-latest
tar xvfz /root/aws-cfn-bootstrap-latest.tar.gz --strip-components=1 -C /root/aws-cfn-bootstrap-latest
easy_install /root/aws-cfn-bootstrap-latest
sudo cfn-init -s DHBox --region us-east-1 -r NewServer
sudo rm /etc/init.d/startup.sh

sudo service shellinabox start