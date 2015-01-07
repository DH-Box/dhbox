import docker
from docker import Client
from docker.utils import kwargs_from_env
import json
from urllib2 import urlopen
import os

def attach_to_docker_client():
	if os.getenv('DOCKER_HOST') == 'tcp://192.168.59.103:2376':
		c = Client(**kwargs_from_env(assert_hostname=False))
	else:
		c = Client()
	return c

def build_dhbox(seed=True, username='test'):
	if seed:
		print "Building Seed"
		os.chdir('seed/')
		response = [line for line in c.build(path='.', rm=True, tag='dhbox/seed')]
		os.chdir('../')
	else:
		print "Building User DH Box"
		os.chdir('dhbox/')
		response = [line for line in c.build(path='.', rm=True, tag='dhbox/'+username)]
		os.chdir('../')
	return response

def all_containers():
	info = c.containers()
	return info

def get_container_info(which_container):
	info = c.inspect_container(which_container)
	return info

def get_container_port(container_name, app_port):
	container = get_container_info(container_name)
	public_port = container['NetworkSettings']['Ports'][app_port+'/tcp'][0]['HostPort']
	return public_port

def get_all_exposed_ports(container_name):
	container = get_container_info(container_name)
	public_ports = container['NetworkSettings']['Ports']
	public_ports_cleaned = {}
	for inside_port, outside_port in public_ports.iteritems():
		inside_port = inside_port [:-4]
		outside_port = outside_port[0]['HostPort']
		public_ports_cleaned[inside_port] = outside_port
	return public_ports_cleaned

def get_hostname():
	if os.getenv('DOCKER_HOST') == 'tcp://192.168.59.103:2376':
		hostname = 'dockerhost'
	else:
		hostname = json.load(urlopen('http://httpbin.org/ip'))['origin']
	return hostname

def build_startup_file(user, the_pass, email):
	"""Create a startup file with a user's custom info"""
	temp_filename = 'dhbox/tmp/startup.sh'
	try:
		os.remove(temp_filename)
	except OSError:
		pass
	temp = open(temp_filename, 'w+b')
	special_string = '  wget -O /tmp/install.html --post-data "username={0}&password={1}&password_confirm={1}&super_email={2}&administrator_email={2}&site_title=DHBox&description=DHBox&copyright=2014&author=DHBOX&tag_delimiter=,&fullsize_constraint=800&thumbnail_constraint=200&square_thumbnail_constraint=200&per_page_admin=10&per_page_public=10&show_empty_elements=0&path_to_convert=/usr/bin&install_submit=Install" localhost:8080/install/install.php'.format(user, the_pass, email)
	try:
		temp.write(
"""#!/bin/bash

set -e

if [ -f /etc/configured ]; then
  echo 'already configured'
else
  #code that needs to run only once
  #needed to fix problems with ubuntu and cron
  update-locale
  date > /etc/configured
  # start Apache and give Omeka our user's info
  sudo service mysql start
  sudo service apache2 restart
""")	
		temp.writelines(['adduser --disabled-password --gecos "" '+user+'\n', 'echo '+user+':'+the_pass+' | chpasswd\n', 'usermod -a -G sudo '+user+'\n'])
		temp.writelines([special_string+'\n', '  sudo service apache2 stop\n', 'sudo service mysql stop\n','fi'])
		temp.seek(0)
	finally:
		return temp
		##make sure to close and remove the file!!

def setup_new_dhbox(username, password, email):
	"""Create a new DH Box with a startup file. Make a new container and start it."""
	startup_file = build_startup_file(username, password, email)
	build_dhbox(seed=False, username=username)
	try:
		print "Creating Container"
		container = c.create_container(image='dhbox/'+username, name=username,
			ports=[(80, 'tcp'), (4200, 'tcp'), (8080, 'tcp'), (8787, 'tcp')], tty=True, stdin_open=True)
	except docker.errors.APIError, e:
		raise e
	else:
		print "Starting Container"
		c.start(container, publish_all_ports=True)
		info = c.inspect_container(container)
    ## Clean up the temporary file
	startup_file.close()
	os.remove(startup_file.name)
	return info

def kill_dhbox(ctr_name, delete_image=False):
	"""Kill a running DH Box container, and optionally remove it"""
	try:
		print "Killing container."
		c.kill(ctr_name)
		c.remove_container(ctr_name)
	except Exception, e:
		if delete_image:
			print "No container to delete. Removing image."
			c.remove_image('dhbox/'+ctr_name)
		raise e
	else:
		if delete_image:
			print "Removing image."
			c.remove_image('dhbox/'+ctr_name)


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
            except docker.errors.DockerAPIError as error:
                print "Failed to delete image\nhash={}\terror={}", image_id, error

    if not found:
        print "Didn't find any untagged images to delete!"

c = attach_to_docker_client()

if __name__ == '__main__':
	c = DockerBackend.attach_to_docker_client()
	# setup_new_dhbox('steve', 'password', 'oneperstephen@gmail.com')