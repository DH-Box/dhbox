import os
import crypt

def make_user_pass(user, password='test'):
    encPass = crypt.crypt(password,"22")
    return {'name': user, 'password': encPass}


def user_set_passes(user_list):
    finished_user_list = []
    # expects a list like: [{'name': 'jimmy', 'password': 'test'}, {'name': 'timmy', 'password': 'fest'}]
    for user in user_list:
        user = make_user_pass(str(user['name']), str(user['password']))
        finished_user_list.append(user)
    return finished_user_list


def create_whole_dhbox(users, admin, email, verbose=False):
    # expects a list just like user_set_passes(), but with hashed passwords
    users = str(users)
    admin = str(admin)
    if verbose is True:
        bashCommand = "ansible-playbook -i ansible/hosts ansible/start.yml -vvvv --private-key=~/.ssh/stevess.pem --extra-vars '{\"users\":"+users+", \"admin\":"+admin+"}'"
    else:
        bashCommand = "ansible-playbook -i ansible/hosts ansible/start.yml --private-key=~/.ssh/stevess.pem --extra-vars '{\"users\":"+users+", \"admin\":"+admin+", \"email\":"+email+"}'"
    print bashCommand
    os.system(bashCommand)

def seed_new(verbose=False):
    if verbose is True:
        bashCommand = "ansible-playbook -i ansible/hosts premake/start.yml -vvvv --private-key=~/.ssh/stevess.pem"
    else:
        bashCommand = "ansible-playbook -i ansible/hosts premake/start.yml --private-key=~/.ssh/stevess.pem"
    print bashCommand
    os.system(bashCommand)

def create_dhbox_from_seed(users, admin, email, verbose=False):
    # expects a list just like user_set_passes(), but with hashed passwords
    users = str(users)
    admin = str(admin)
    if verbose is True:
        bashCommand = "ansible-playbook -i ansible/hosts after/start.yml -vvvv --private-key=~/.ssh/stevess.pem --extra-vars '{\"users\":"+users+", \"admin\":"+admin+"}'"
    else:
        bashCommand = "ansible-playbook -i ansible/hosts after/start.yml --private-key=~/.ssh/stevess.pem --extra-vars '{\"users\":"+users+", \"admin\":"+admin+", \"email\":"+email+"}'"
    print bashCommand
    os.system(bashCommand)


if __name__ == '__main__':
    test_users = user_set_passes([{'name': 'jimmy', 'password': 'test123'}, {'name': 'timmy', 'password': 'fest123'}])
    test_admin = user_set_passes([{'name': 'steve', 'password':'test123'}])
    create_dhbox_from_seed(test_users, test_admin[0], 'oneperstephen@gmail.com', verbose=False)