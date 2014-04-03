#!/bin/sh
set -e -x -a


#
# Get a repository for R, install Openssl
#
wget http://ftp.us.debian.org/debian/pool/main/o/openssl/libssl0.9.8_0.9.8o-4squeeze14_amd64.deb
dpkg -i libssl0.9.8_0.9.8o-4squeeze14_amd64.deb
echo "deb http://ftp.ussg.iu.edu/CRAN/bin/linux/debian wheezy-cran3/" >> /etc/apt/sources.list
#
# Installing apt packages
#
apt-get --yes --quiet update
apt-get --yes --force-yes --quiet install git puppet-common shellinabox default-jdk r-base gdebi-core ant python python-pip ipython-notebook
#
# Install R Studio
#
wget http://download2.rstudio.org/rstudio-server-0.98.501-amd64.deb
yes | gdebi rstudio-server-0.98.501-amd64.deb
#
# Adding Users
#
export users="$dhbox_users"
wget --no-check-certificate -P /dhbox https://raw.githubusercontent.com/DH-Box/dhbox/master/users.py
python /dhbox/users.py
#
# Fetch puppet configuration from public git repository.
#
mv /etc/puppet /etc/puppet.orig
git clone $puppet_source /etc/puppet
#
# Run puppet.
#
puppet apply /etc/puppet/manifests/init.pp
#
# Configure user permissions
#
chmod -R 777 /usr/local/projects/Omeka/
#
# Install MALLET
#
mkdir -p /dhbox/mallet
wget --no-check-certificate -P /dhbox http://mallet.cs.umass.edu/dist/mallet-2.0.7.tar.gz
tar xfz /dhbox/mallet-2.0.7.tar.gz --strip-components=1 -C /dhbox/mallet
ant -buildfile /dhbox/mallet/build.xml
#
# Install some Python stuff?
#

