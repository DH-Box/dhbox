from subprocess import Popen, PIPE
import os

def kill_and_remove(ctr_name):
    for action in ('kill', 'rm'):
        p = Popen('docker %s %s' % (action, ctr_name), shell=True,
                  stdout=PIPE, stderr=PIPE)
        if p.wait() != 0:
            raise RuntimeError(p.stderr.read())


def build_dhbox(seed=True):
	if seed:
		p = Popen('docker %s' % ('build -t dhbox/seed seed/'), shell=True,
                  stdout=PIPE, stderr=PIPE)
	else:
		p = Popen('docker %s' % ('build -t dhbox/seed dhbox/'), shell=True,
                  stdout=PIPE, stderr=PIPE)
	return p

def run_container(name, user_container='dhbox/user'):
	container = Popen('docker %s' % ('run --rm -p 80 -p 4200 -p 8787 -p 8080 -t -i dhbox/user /sbin/my_init'), shell=True,
                  stdout=PIPE, stderr=PIPE)
	# info = get_container_info(container)
	# return info

# def get_container_info(which_container):
# 	containers = c.containers()
# 	for container_info in containers:
# 		if which_container in container_info['Names'][0]:
# 			return container_info

# def get_container_port(container_name, app_port):
# 	container = get_container_info(container_name)
# 	public_port = [item for item in container['Ports'] if item['PrivatePort'] == app_port][0]['PublicPort']
# 	return public_port

def build_startup_file(user, the_pass, email):
	temp_filename = 'dhbox/tmp/startup.sh'
	temp = open(temp_filename, 'w+b')
	special_string = '  wget -O /tmp/install.html --post-data "username={0}&password={1}&password_confirm={1}&super_email={2}&administrator_email={2}&site_title=DHBox&description=DHBox&copyright=2014&author=DHBOX&tag_delimiter=,&fullsize_constraint=800&thumbnail_constraint=200&square_thumbnail_constraint=200&per_page_admin=10&per_page_public=10&show_empty_elements=0&path_to_convert=/usr/bin&install_submit=Install" localhost:8080/install/install.php'.format(user, the_pass, email)
	try:
		temp.write(
"""
#!/bin/bash

set -e

if [ -f /etc/configured ]; then
  echo 'already configured'
else
  #code that needs to run only once
  #needed to fix problems with ubuntu and cron
  update-locale
  date > /etc/configured
  # start apache and give Omeka our user's info
  sudo service apache2 restart
""")	
		temp.writelines([special_string+'\n', '  sudo service apache2 stop\n', 'fi'])
		temp.seek(0)
	finally:
		return temp
		##make sure to close and remove the file!!

def setup_new_dhbox(user, password, email):
	startup_file = build_startup_file(user, password, email)
	build_dhbox(seed=False)
	print startup_file
	info = run_container('test')
	startup_file.close()
    # Clean up the temporary file
	os.remove(startup_file.name)
	return info

if __name__ == '__main__':
	setup_new_dhbox('steve', 'password', 'oneperstephen@gmail.com')