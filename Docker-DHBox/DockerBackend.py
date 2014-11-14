from docker import Client
from docker.utils import kwargs_from_env
import os

# c = Client()
c = Client(**kwargs_from_env(assert_hostname=False))

def attach_to_docker_client(development=False):
	if development:
		c = Client(**kwargs_from_env(assert_hostname=False))
	else:
		c = Client()
	return c

def build_dhbox(seed=True):
	if seed:
		response = [line for line in c.build(path='seed/', rm=True, tag='dhbox/seed')]
	else:
		response = [line for line in c.build(path='dhbox/', rm=True, tag='dhbox/user')]
	return response

def create_new_container(name, user_container='dhbox/user'):
	container = c.create_container(image=user_container, name=name,
		ports=[(80, 'tcp'), (4200, 'tcp'), (8080, 'tcp'), (8787, 'tcp')], tty=True, stdin_open=True)
	c.start(container, publish_all_ports=True)
	info = c.inspect_container(container)
	return info

def get_container_info(which_container):
	containers = c.containers()
	for container_info in containers:
		if which_container in container_info['Names'][0]:
			return container_info

def get_container_port(container_name, app_port):
	container = get_container_info(container_name)
	public_port = [item for item in container['Ports'] if item['PrivatePort'] == app_port][0]['PublicPort']
	return public_port

def build_startup_file(user, the_pass, email):
	temp_filename = 'dhbox/tmp/startup.sh'
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
  # start apache and give Omeka our user's info
  sudo service mysql start
  sudo service apache2 restart
""")	
		temp.writelines([special_string+'\n', '  sudo service apache2 stop\n', 'sudo service mysql stop\n','fi'])
		temp.seek(0)
	finally:
		return temp
		##make sure to close and remove the file!!

def setup_new_dhbox(user, password, email):
	startup_file = build_startup_file(user, password, email)
	build_dhbox(seed=False)
	info = create_new_container('test')
	startup_file.close()
    # Clean up the temporary file
	os.remove(startup_file.name)
	return info

def kill_delete_dhbox(ctr_name, username):
	try:
		c.kill(ctr_name)
		c.remove_container(ctr_name)
		c.remove_image(username)
	except Exception, e:
		print e
	
if __name__ == '__main__':
	c = Client(**kwargs_from_env(assert_hostname=False))
	setup_new_dhbox('steve', 'password', 'oneperstephen@gmail.com')