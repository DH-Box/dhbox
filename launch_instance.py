#!/usr/bin/python

from string import Template

import boto.ec2

PUPPET_SOURCE = 'https://bitbucket.org/rimey/hello-ec2-puppetboot.git'
info = {}
def get_script(filename='user-data-script.sh'):
    template = open(filename).read()
    return Template(template).substitute(
        puppet_source=PUPPET_SOURCE,
    )

def launch():
    connection = boto.ec2.connect_to_region('us-east-1')
    i = connection.run_instances(
        image_id = 'ami-032b416a',
        instance_type = 't1.micro',
        key_name = 'stevess',
        security_groups = ['default'],
        user_data=get_script(),
    )
    info['Instance'] = i.instances[0].id
    print info
    return info

if __name__ == '__main__':
    launch()