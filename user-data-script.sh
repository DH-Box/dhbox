#!/bin/sh
set -e -x

apt-get --yes --quiet update
apt-get --yes --quiet install git puppet-common

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
# Change permissions so Omeka can run
#
sudo chmod -R 777 /usr/local/projects/Omeka/
#
# Install MALLET
#
sudo wget --no-check-certificate -P /dhbox http://mallet.cs.umass.edu/dist/mallet-2.0.7.tar.gz
sudo tar xvfz /dhbox/mallet-2.0.7.tar.gz --strip-components=1 -C /dhbox/mallet
sudo ant -buildfile /dhbox/mallet/build.xml