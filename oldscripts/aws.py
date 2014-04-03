from boto.ec2 import connect_to_region
from ConfigParser import SafeConfigParser
from properties import loadcredentials
import sys, os, time

USERNAME = 'admin'
AMI_ID = 'ami-032b416a'
INSTANCE_TYPE = 'm1.small'

EC2_REGION = 'us-east-1'
EC2_SSH_KEY_NAME = 'stevess'
EC2_SSH_KEY_PATH = os.path.join(os.path.dirname(__file__), 'venv', 'stevess.pem')

class Node:
    def __init__(self, instance):
        self.hostname = instance.public_dns_name
        self.ssh_key_file = EC2_SSH_KEY_PATH
        self.ssh_user = USERNAME

def provision_with_boto(name):
    conn = connect()

    for reservation in fetch_running_reservations(conn, name):
        for instance in reservation.instances:
            return Node(instance)

    res = conn.run_instances(AMI_ID, key_name=EC2_SSH_KEY_NAME, instance_type=INSTANCE_TYPE)
    instance = res.instances[0]

    print "Waiting for", name, instance.id, "to start ..."
    wait_while(instance, 'pending')

    conn.create_tags([instance.id], {'Name': name})

    print "Instance", name, instance.id, "is running"
    return Node(instance)

def get_node(name):
    conn = connect()
    for reservation in fetch_running_reservations(conn, name):
        for instance in reservation.instances:
            return Node(instance)

def connect():
    credentials = loadcredentials()
    access_key = credentials.access_key_id
    secret_key = credentials.secret_access_key
    return connect_to_region(EC2_REGION, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

def fetch_running_reservations(conn, name):
    filters = {'tag:Name': name, 'instance-state-name': 'running'}
    return conn.get_all_instances(filters=filters)

def terminate_instance(name):
    conn = connect()
    for reservation in fetch_running_reservations(conn, name):
        for instance in reservation.instances:
            print 'Terminating instance', instance.id
            instance.terminate()
            wait_while(instance, 'running')

def terminate_all_instances():
    conn = connect()
    for reservation in conn.get_all_instances():
        for instance in reservation.instances:
            print 'Terminating instance', instance.id
            instance.terminate()
            wait_while(instance, 'running')

def wait_while(instance, status):
    instance.update()
    while instance.state == status:
        time.sleep(5)
        instance.update()
