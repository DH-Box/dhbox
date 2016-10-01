import docker
from docker import Client
from docker.utils import kwargs_from_env
import json
from urllib2 import urlopen
import os, time, subprocess
from threading import Timer
import logging
import ipgetter
import datetime as dt
import dhbox


dhbox_repo = 'thedhbox'
gotten_ip = ipgetter.myip()

# logging.basicConfig(filename='dhbox.log',level=logging.ERROR)


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
        if dhbox.app.config['LOCALHOST']:
            hostname = 'localhost'
        else:
            hostname = gotten_ip or dhbox.app.config['DEFAULT_HOSTNAME']
    return hostname


def download_dhbox(username='test'):
    """Downloads a DH Box seed, renaming the old one if it exists"""
    print "Downloading Seed"
    images = c.images()
    for image in images:
        if image["RepoTags"] == [dhbox_repo+"/seed:latest"]:
            image_id = image["Id"]
            c.tag(image=image_id, repository=dhbox_repo+'/seed', tag='older', force=True)
    for line in c.pull(dhbox_repo+'/seed:latest', stream=True):
        print(json.dumps(json.loads(line), indent=4))
    for line in c.pull(dhbox_repo+'/twordpress:latest', stream=True):
        print(json.dumps(json.loads(line), indent=4))


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
    environment = {"PASS": password, "EMAIL": email, "THEUSER": username, "DEMO": demo}
    if demo:
        environment = {"PASS": 'demonstration', "EMAIL": email, "THEUSER": 'demonstration', "DEMO": demo}        
    try:
       # ports = [(lambda x: app['port'] for app in dhbox.all_apps if app['port'] != None)]
       # print ports
        print "Creating Containers"
        wp_container = c.create_container(image=dhbox_repo+"/twordpress:latest",
                                          name=username+'_wp',
                                          ports=[80],)
        container = c.create_container(image=dhbox_repo+'/seed:latest', name=username,
                                       ports=[8080, 8081, 8787, 4444, 4200, 3000, 8888],
                                       tty=True, stdin_open=True, 
                                       environment=environment)
    except docker.errors.APIError, e:
        print e
        raise e
    else:
        print "Starting Containers"
        restart_policy = {"MaximumRetryCount": 10, "Name": "always"}
        c.start(wp_container,
                publish_all_ports=True, restart_policy=restart_policy)
        c.start(container, publish_all_ports=True, volumes_from=username+'_wp', restart_policy=restart_policy)
        configure_dhbox(username, password, email, demo=demo)
        info = c.inspect_container(container)
        return info


def execute(container, args):
    """Execute a list of arbitrary Bash commands inside a container"""
    for arg in args:
        # print arg
        exec_instance = c.exec_create(container=container, cmd=arg)
        return c.exec_start(exec_instance)


def configure_dhbox(user, the_pass, email, demo=False):
    """Use Docker exec to SSH into a new container, customizing it for the user.
    Adds the user to Omeka. """
    container = user
    if demo:
        user = 'demonstration'
    omeka_string = 'wget -O /tmp/install.html --post-data "username={0}&password={1}&password_confirm={1}&super_email={2}&administrator_email={2}&site_title=DHBox&description=DHBox&copyright=2014&author=DHBOX&tag_delimiter=,&fullsize_constraint=800&thumbnail_constraint=200&square_thumbnail_constraint=200&per_page_admin=10&per_page_public=10&show_empty_elements=0&path_to_convert=/usr/bin&install_submit=Install" localhost:8080/install/install.php'.format(
        user, the_pass, email)
    time.sleep(5)
    execute(container, [omeka_string])


def demo_dhbox(username):
    """Make a demonstration DH Box with a random name. Expires in an hour."""
    password = 'demonstration'
    email = username + '@demo.com'
    setup_new_dhbox(username, password, email, demo=True)


def add_user(container, username, password):
    """Add a user to a running DH Box"""
    execute(container, ["useradd " + username])
    execute(container, ["echo " + username + ":" + password + " | chpasswd"])


def kill_and_remove_user(name, user=True):
    """Kill a running DH Box container and remove the user if there is one"""
    try:
        print "Killing container."
        c.kill(name)
        c.kill(name+'_wp')
        c.remove_container(name)
        c.remove_container(name+'_wp')
        if user:
            dhbox.delete_user(name)
    except (docker.errors.NotFound, docker.errors.APIError) as e:
        print "Could not kill container ", name
        if user:
            dhbox.delete_user(name)
        return e


def delete_untagged():
    """Find the untagged images and remove them"""
    images = c.images()
    found = False
    for image in images:
        if image["RepoTags"] == ["<none>:<none>"]:
            found = True
            image_id = image["Id"]
            print "Deleting untagged image\nhash=", image_id
            try:
                c.remove_image(image["Id"])
            except docker.errors.APIError as error:
                print "Failed to delete image\nhash={}\terror={}", image_id, error

    if not found:
        print "Didn't find any untagged images to delete!"


def how_long_up(container):
    """Find out how long a container has been running, in seconds"""
    try:
        detail = c.inspect_container(container)
        time_started = dt.datetime.strptime(detail['Created'][:-4], '%Y-%m-%dT%H:%M:%S.%f')
        time_up = dt.datetime.utcnow() - time_started   
        return time_up.total_seconds()
    except docker.errors.NotFound, e:
        return e


def check_if_over_time(user):
    try:
        duration = user.dhbox_duration - how_long_up(user.name)
        return duration
    except docker.errors.NotFound, e:
        return e


def check_and_kill(user):
    """Checks a container's uptime and kills it and the user if time is up"""
    try:
        get_container_info(user.name)
        time_left = user.dhbox_duration - how_long_up(user.name)
        # print user.name, " time left: ", time_left, " seconds"
        if time_left <= 0:
            kill_and_remove_user(user.name)
    except docker.errors.NotFound:
        dhbox.delete_user(user.name)


def replace_admin_dhbox_image():
    """Updates admin's DH Box to the new seed image."""
    kill_and_remove_user('admin', user=False)
    dhbox.create_user_and_role()
    # setup_new_dhbox('admin', dhbox.app.config['ADMIN_PASS'], dhbox.app.config['ADMIN_EMAIL'], demo=False)


def display_time(seconds, granularity=2):
    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])


c = attach_to_docker_client()


if __name__ == '__main__':
    c = attach_to_docker_client()
