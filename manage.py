from manager import Manager
from docker import Client
from docker.utils import kwargs_from_env
import DockerBackend
import os
from subprocess import call

manager = Manager()


@manager.command
def new_seed():
    """Build new seed for DH Box"""
    response = DockerBackend.build_dhbox()
    return response


@manager.command
def test():
    """Build new test DH Box"""
    response = DockerBackend.setup_new_dhbox('test', 'password', 'test@gmail.com')
    return response


@manager.command
def start_over():
    """Delete and make a new test DH Box"""
    cleanup()
    response = DockerBackend.kill_dhbox('test', delete_image=False)
    DockerBackend.setup_new_dhbox('test', 'password', 'test@gmail.com')
    return response


@manager.command
def clean_slate():
    """Delete all DH Boxes"""
    cleanup()
    response = DockerBackend.kill_dhbox('test', delete_image=False)
    DockerBackend.setup_new_dhbox('test', 'password', 'test@gmail.com')
    return response


@manager.command
def killctr(ctr_name):
    """Delete a container"""
    print "killing container " + ctr_name
    response = DockerBackend.kill_dhbox(ctr_name)
    return response


@manager.command
def cleanup():
    """Delete ALL stopped containers, unnamed images"""
    print "Deleting stopped containers"
    call("docker ps -a | grep Exit | awk '{print $1}' |  xargs docker rm", shell=True)
    print "Deleting images"
    DockerBackend.delete_untagged()


if __name__ == '__main__':
    c = DockerBackend.attach_to_docker_client()
    manager.main()