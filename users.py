#!/usr/bin/python
import os
import ast

def adduser(user, password):
    os.system("useradd -m "+user)
    os.system("echo -e '"+password+"\n"+password+"\n' | passwd "+ user)


def set_users():
    user_list = ast.literal_eval(os.environ.get('users'))
    for user in user_list:
        adduser(user['name'], user['pass'])
    del os.environ['users']