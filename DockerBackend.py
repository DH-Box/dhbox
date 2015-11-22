import docker
from docker import Client
from docker.utils import kwargs_from_env
import json
from urllib2 import urlopen
import os, time, subprocess
from threading import Timer
import dhbox
import logging
import ipgetter
import datetime

dhbox_repo = 'thedhbox'
gotten_ip = ipgetter.myip()

logging.basicConfig(filename='dhbox.log',level=logging.DEBUG)

def attach_to_docker_client():
    if os.getenv('DOCKER_HOST') == 'tcp://192.168.59.103:2376':
        c = Client(**kwargs_from_env(assert_hostname=False))
    else:
        c = Client()
    return c


def get_hostname():
    """Determine the IP address of the host server"""
    if os.getenv('DOCKER_HOST') == 'tcp://192.168.59.103:2376':
        hostname = 'dockerhost'
    else:
        if dhbox.app.config['TESTING']:
            hostname = 'localhost'
        else:
            hostname = gotten_ip or dhbox.app.config['DEFAULT_HOSTNAME']
    return hostname


def build_dhbox(username='test'):
    """Builds a new Dh Box seed, renaming the old one if it exists"""
    print "Building Seed"
    images = c.images()
    for image in images:
        if image["RepoTags"] == [dhbox_repo+"/seed:latest"]:
            image_id = image["Id"]
            c.tag(image=image_id, repository=dhbox_repo+'/seed', tag='older', force=True)
    os.chdir('seed/')
    for line in c.build(path='.', rm=True, tag=dhbox_repo+'/seed:latest'):
        print line
    if "errorDetail" in line:
        # There was an error, so kill the container and the image
        pass
    os.chdir('../')


def all_containers():
    info = c.containers(all=True)
    return info


def get_container_info(which_container):
    info = c.inspect_container(which_container)
    return info


def get_container_port(container_name, app_port):
    container = get_container_info(container_name)
    public_port = container['NetworkSettings']['Ports'][app_port + '/tcp'][0]['HostPort']
    return public_port


def get_all_exposed_ports(container_name):
    container = get_container_info(container_name)
    public_ports = container['NetworkSettings']['Ports']
    public_ports_cleaned = {}
    for inside_port, outside_port in public_ports.iteritems():
        inside_port = inside_port[:-4]
        outside_port = outside_port[0]['HostPort']
        public_ports_cleaned[inside_port] = outside_port
    return public_ports_cleaned


def setup_new_dhbox(username, password, email, demo=False):
    """Create a new DH Box container, customize it."""
    try:
       # ports = [(lambda x: app['port'] for app in dhbox.all_apps if app['port'] != None)]
       # print ports
        print "Creating Container"
        container = c.create_container(image=dhbox_repo+'/seed:latest', name=username,
                                       ports=[8080, 8787, 4444, 4200],
                                       tty=True, stdin_open=True)
    except docker.errors.APIError, e:
        raise e
    else:
        print "Starting Container"
        restart_policy = {"MaximumRetryCount": 10, "Name": "always"}
        c.start(container, publish_all_ports=True, restart_policy=restart_policy)
        configure_dhbox(username, password, email, demo=demo)
        info = c.inspect_container(container)
        return info


def execute(container, args):
    """Execute a list of arbitrary Bash commands inside a container"""
    for arg in args:
        print arg
        exec_instance = c.exec_create(container=container,cmd=arg)
        c.exec_start(exec_instance)

def configure_dhbox(user, the_pass, email, demo=False):
    """Use Docker exec to SSH into a new container, customizing it for the user.
    Adds the user to the UNIX instance, and Omeka. """
    container = user
    if demo:
        user = 'demonstration'
    user_add_strings = ['adduser --disabled-password --gecos "" ' + user, 'usermod -a -G sudo ' + user]
    config = execute(container, user_add_strings)
    if os.getenv('DOCKER_HOST') == 'tcp://192.168.59.103:2376':
        subprocess.call('echo ' + user + ':' + the_pass + ' | docker exec -i ' + container + ' chpasswd', shell=True)
    else:
        subprocess.call('echo ' + user + ':' + the_pass + ' | sudo docker exec -i ' + container + ' chpasswd',
                        shell=True)
    omeka_string = 'wget -O /tmp/install.html --post-data "username={0}&password={1}&password_confirm={1}&super_email={2}&administrator_email={2}&site_title=DHBox&description=DHBox&copyright=2014&author=DHBOX&tag_delimiter=,&fullsize_constraint=800&thumbnail_constraint=200&square_thumbnail_constraint=200&per_page_admin=10&per_page_public=10&show_empty_elements=0&path_to_convert=/usr/bin&install_submit=Install" localhost:8080/install/install.php'.format(
        user, the_pass, email)
    time.sleep(5)
    execute(container, [omeka_string])


def demo_dhbox(username):
    """Make a demonstration DH Box with a random name. Expires after an hour."""
    password = 'demonstration'
    email = username + '@demo.com'
    setup_new_dhbox(username, password, email, demo=True)
    t = Timer(600.0, kill_and_remove_user, [username])
    t.start()  # after one hour, demo will be destroyed


def kill_dhbox(ctr_name):
    """Kill a running DH Box container"""
    try:
        print "Killing container."
        c.kill(ctr_name)
        c.remove_container(ctr_name)
    except Exception, e:
        raise e


def kill_and_remove_user(name):
    kill_dhbox(name)
    logging.info("killed user "+name)
    dhbox.delete_user(name)


def how_long_up(container):
    """Find out how long a container has been running, in seconds"""
    detail = c.inspect_container(container)
    time_started = dt.datetime.strptime(detail['Created'][:-4], '%Y-%m-%dT%H:%M:%S.%f')
    time_up = datetime.datetime.now() - time_started
    return time_up.total_seconds()

c = attach_to_docker_client()

if __name__ == '__main__':
    c = DockerBackend.attach_to_docker_client()
# setup_new_dhbox('test', 'password', 'test@gmail.com')
