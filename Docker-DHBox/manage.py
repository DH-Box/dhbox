from manager import Manager
from docker import Client
from docker.utils import kwargs_from_env
import DockerBackend

manager = Manager()



@manager.command
def new_seed():
    """Build new seed DH Box"""
    c = Client(**kwargs_from_env(assert_hostname=False))
    response = DockerBackend.build_dhbox(seed=True)
    return response

@manager.command
def test():
    """Build new USER DH Box"""
    c = Client(**kwargs_from_env(assert_hostname=False))
    response = DockerBackend.setup_new_dhbox('steve', 'password', 'oneperstephen@gmail.com')
    return response


@manager.command
def start_over():
    """delete and make a new DH Box test"""
    c = Client(**kwargs_from_env(assert_hostname=False))
    response = DockerBackend.kill_delete_dhbox('test', 'dhbox/user')
    DockerBackend.setup_new_dhbox('steve', 'password', 'oneperstephen@gmail.com')
    return response

if __name__ == '__main__':
    manager.main()