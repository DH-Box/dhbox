#!/usr/bin/python
import os
import ast
import crypt

def adduser(user, password):
    encPass = crypt.crypt(password,"22")
    os.system("useradd -m -p "+ encPass +" "+ user)


def set_users():
    user_list = ast.literal_eval(str(os.environ.get('users')))
    for user in user_list:
        adduser(user['name'], user['pass'])
    del os.environ['users']

if __name__ == '__main__':
    set_users()