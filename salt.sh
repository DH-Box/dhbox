#!/bin/bash

# Install saltstack
add-apt-repository ppa:saltstack/salt -y
apt-get update -y
apt-get install salt-minion -y
apt-get install salt-master -y
apt-get upgrade -y

# Set salt master location and start minion
sed -i 's/#master: salt/master: [salt_master_fqdn]/' /etc/salt/minion
salt-minion -d