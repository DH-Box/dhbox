#!/bin/sh
set -e -x

sudo apt-get --yes --quiet update
sudo apt-get --yes --quiet install git puppet-common default-jdk ant
sudo mv /etc/puppet /etc/puppet.orig

# Make a source directory for DHBox (and MALLET)
sudo mkdir -p /dhbox/mallet
#
# Fetch puppet configuration from public git repository.
#

sudo git clone $puppet_source /etc/puppet
#
# Run puppet.
#
sudo puppet apply /etc/puppet/manifests/init.pp
#
# Change permissions so Omeka can run
#
sudo chmod -R 777 /usr/local/projects/Omeka/
#
# Install MALLET
#
sudo wget --no-check-certificate -P /dhbox http://mallet.cs.umass.edu/dist/mallet-2.0.7.tar.gz
sudo tar xfz /dhbox/mallet-2.0.7.tar.gz --strip-components=1 -C /dhbox/mallet
sudo ant -buildfile /dhbox/mallet/build.xml