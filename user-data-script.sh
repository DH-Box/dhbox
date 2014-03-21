#!/bin/sh
set -e -x

sudo apt-get --yes --quiet update
sudo apt-get --yes --quiet install git puppet-common

# Make a source directory for DHBox (and MALLET)
sudo mkdir -p /dhbox/mallet

sudo puppet module install maestrodev-ant
sudo puppet module install maestrodev-wget
#
# Fetch puppet configuration from public git repository.
#

sudo mv /etc/puppet /etc/puppet.orig
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
sudo tar xvfz /dhbox/mallet-2.0.7.tar.gz --strip-components=1 -C /dhbox/mallet
sudo ant -buildfile /dhbox/mallet/build.xml