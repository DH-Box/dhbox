import os
from flask import Flask, request, redirect, url_for, render_template, make_response, jsonify, send_file, current_app
import ast

# create application
app = Flask('dhbox')


"""
URLS/VIEWS
"""


@app.route("/test")
def login():
    return render_template('test.html')

@app.route('/new_dhbox', methods=['POST'])
def new_dhbox():
    users_and_passes = []
    admins_and_passes = []
    form  = request.form
    data = {key: request.form.getlist(key)[0] for key in request.form.keys()}
    for key in data:
        users_dict = key
    users_dict = ast.literal_eval(users_dict)
    users = users_dict['users']
    for user in users:
        if 'name' in user:
            if 'email' in user: # Checks if Admin
                # already_has_dhbox_check = User.query.filter(User.email == user['email']).first()
                # if already_has_dhbox_check:
                #     print previous_user_check
                #     return str(form)
                # else:
                admins_and_passes.append({'name': user['name'], 'password': user['pass']})
                adminEmail = user['email']
                adminPass = user['pass']
            else:
                users_and_passes.append({'name': user['name'], 'password': user['pass']})
    # users_hashed_passes = ansible_call.user_set_passes(users_and_passes)
    # admins_hashed_passes = ansible_call.user_set_passes(admins_and_passes)
    # print users_hashed_passes, admins_hashed_passes[0], adminEmail, adminPass
    # ansible_call.create_dhbox_from_seed(users_hashed_passes, admins_hashed_passes[0], adminEmail, adminPass)
    print str(form)
    return str(form)

if __name__ == '__main__':
	app.debug = True
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
	# app.run()