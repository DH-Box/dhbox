import os
import os.path
from flask import Flask, request, redirect, url_for, render_template, make_response, jsonify, send_file, current_app
import ast
from flask.ext.sqlalchemy import SQLAlchemy
from database.database import db_session, init_db
from database.models import User
import DockerBackend

# Make database if it doesn't exist
if not os.path.exists('dhbox-docker.db'):
    init_db()

# create application
app = Flask('dhbox')


"""
URLS/VIEWS
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dhbox-docker.db'

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route("/test")
def login():
    return render_template('test.html')

@app.route("/dhbox/<the_user>")
def user_box(the_user):
    which_user = User.query.filter(User.name == str(the_user)).first()
    dhbox_username = which_user.name
    port_info = DockerBackend.get_all_exposed_ports(dhbox_username)
    hostname = DockerBackend.get_hostname()
    return str(port_info)

@app.route("/dhbox/<the_user>/rstudio")
def rstudio_box(the_user):
    which_user = User.query.filter(User.name == str(the_user)).first()
    dhbox_username = which_user.name
    port_info = DockerBackend.get_container_port(dhbox_username, '8787')
    hostname = DockerBackend.get_hostname()
    location = hostname+":"+port_info
    return redirect(location)



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
            if 'email' in user: # Then is DH Box admin
                already_has_dhbox_check = User.query.filter(User.name == user['name']).first()
                if already_has_dhbox_check:
                    print already_has_dhbox_check
                    print "Username taken. Already has a DH Box."
                    return str(form)
                else:
                    admin_user = user['name']
                    admin_email = user['email']
                    admin_pass = user['pass']
                    new_user = User(admin_user, admin_email)
                    db_session.add(new_user)
                    db_session.commit()
            else:
                pass
            the_new_dhbox = DockerBackend.setup_new_dhbox(admin_user, admin_pass, admin_email)
    return str(form)

if __name__ == '__main__':
	app.debug = True
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
	# app.run()