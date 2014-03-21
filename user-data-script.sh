#!/bin/sh
set -e -x

apt-get --yes --quiet update
apt-get --yes --quiet install git puppet-common shellinabox default-jdk

#
# Fetch puppet configuration from public git repository.
#

mv /etc/puppet /etc/puppet.orig
git clone $puppet_source /etc/puppet

#
# Run puppet.
#

puppet apply /etc/puppet/manifests/init.pp

chmod -R 777 /usr/local/projects/Omeka/

#
# Install MALLET
#
mkdir -p /dhbox/mallet
wget --no-check-certificate -P /dhbox http://mallet.cs.umass.edu/dist/mallet-2.0.7.tar.gz
tar xfz /dhbox/mallet-2.0.7.tar.gz --strip-components=1 -C /dhbox/mallet
ant -buildfile /dhbox/mallet/build.xml