import docker

c = docker.Client()

def create_container(name, seed_container='steve/seed'):
	container = c.create_container(seed_container, name=name, ports=[(80, 'tcp'), (4200, 'tcp'), (8080, 'tcp'), (8787, 'tcp')])
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

def setup_new_dhbox():
	pass