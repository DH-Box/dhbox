from manager import Manager
from docker import Client
from docker.utils import kwargs_from_env
import DockerBackend
import os

manager = Manager()



@manager.command
def new_seed():
    """Build new seed DH Box"""
    response = DockerBackend.build_dhbox(seed=True)
    return response

@manager.command
def test():
    """Build new test DH Box"""
    response = DockerBackend.setup_new_dhbox('test', 'password', 'oneperstephen@gmail.com')
    return response


@manager.command
def start_over():
    """delete and make a new test DH Box"""
    cleanup()
    response = DockerBackend.kill_dhbox('test', delete_image=True)
    DockerBackend.setup_new_dhbox('test', 'password', 'oneperstephen@gmail.com')
    return response

@manager.command
def killctr(ctr_name):
    """delete a container"""
    print "killing container " + ctr_name
    response = DockerBackend.kill_dhbox(ctr_name)
    return response

@manager.command
def cleanup():
    """delete unnamed images"""
    print "Deleting Images"
    DockerBackend.delete_untagged()

if __name__ == '__main__':
    c = DockerBackend.attach_to_docker_client()
    manager.main()