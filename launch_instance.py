#!/usr/bin/python
from string import Template
import boto.ec2
import sys, os, time

PUPPET_SOURCE = 'https://github.com/szweibel/puppetboot.git'
info = {}

def get_script(filename='user-data-script.sh', users=[{'name':'dhbox', 'pass':'test'}]):
    template = open(filename).read()
    return Template(template).substitute(puppet_source=PUPPET_SOURCE, dhbox_users=str(users))

def launch(name='dhbox', users=[]):
    connection = boto.ec2.connect_to_region('us-east-1')
    i = connection.run_instances(
        image_id = 'ami-032b416a',
        instance_type = 't1.micro',
        key_name = 'stevess',
        security_groups = ['default'],
        user_data=get_script(),
    )
    instance = i.instances[0]
    info['Instance'] = instance.id

    print "Waiting for", name, instance.id, "to start ..."
    wait_while(instance, 'pending')

    instance.add_tag('Name', name)
    instance.add_tag('Users', users)
    print "Instance", name, instance.id, "is running"
    return info

def fetch_running_instances(name=None):
    conn = boto.ec2.connect_to_region('us-east-1')
    if name is not None:
        filters = {'tag:Name': name, 'instance-state-name': 'running'}
    else:
        filters = {'instance-state-name': 'running'}
    return conn.get_only_instances(filters=filters)

def terminate_instance(name):
    for reservation in fetch_running_instances(name):
        for instance in reservation.instances:
            print 'Terminating instance', instance.id
            instance.terminate()
            wait_while(instance, 'running')

def wait_while(instance, status):
    # Wait while in a status, eg 'running', 'pending'
    instance.update()
    while instance.state == status:
        time.sleep(5)
        instance.update()


if __name__ == '__main__':
    launch()