import os
import crypt

def make_user_pass(user, password='test'):
    encPass = crypt.crypt(password,"22")
    return {'name': user, 'password': encPass}


def user_set_passes(user_list, finished_user_list = []):
    # expects a list like: [{'name': 'jimmy', 'password': 'test'}, {'name': 'timmy', 'password': 'fest'}]
    for user in user_list:
        user = make_user_pass(str(user['name']), str(user['password']))
        finished_user_list.append(user)
    return finished_user_list


def call_ansible(users):
    # expects a list just like user_set_passes(), but with hashed passwords
    users = str(users)
    bashCommand = "ansible-playbook -i ansible/hosts ansible/start.yml --private-key=~/.ssh/stevess.pem --extra-vars '{\"users\":"+users+"}'"
    print bashCommand
    os.system(bashCommand)

if __name__ == '__main__':
    pass