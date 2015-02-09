import os
import sys
import os.path
from flask import Flask, flash, request, redirect, url_for, render_template, \
    make_response, jsonify, send_file, current_app, g, abort
import ast
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_user, \
    UserMixin, RoleMixin, login_required, roles_required, registerable, current_user, LoginForm
from wtforms.validators import DataRequired
from wtforms import TextField, Form
from werkzeug import generate_password_hash, check_password_hash
from werkzeug.contrib.fixers import ProxyFix
import DockerBackend

# create application
app = Flask('dhbox')
app.wsgi_app = ProxyFix(app.wsgi_app)

# def install_secret_key(app, filename='secret_key'):
#     """Configure the SECRET_KEY from a file
#     in the instance directory.

#     If the file does not exist, print instructions
#     to create it from a shell with a random key,
#     then exit.

#     """
#     filename = os.path.join(app.instance_path, filename)
#     try:
#         app.config['SECRET_KEY'] = open(filename, 'rb').read()
#     except IOError:
#         print 'Error: No secret key. Create it with:'
#         if not os.path.isdir(os.path.dirname(filename)):
#             print 'mkdir -p', os.path.dirname(filename)
#         print 'head -c 24 /dev/urandom >', filename
#         sys.exit(1)

# install_secret_key(app)
app.config.from_pyfile('config.cfg')

# Create database connection object
db = SQLAlchemy(app)

all_apps = {'rstudio': '8787', 'bash': '4200', 'omeka': '8080', 'apache': '80'}

"""
MODELS
"""
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    name = db.Column(db.String(255), unique=True)
    pwdhash = db.Column(db.String(160))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    
    def __init__(self, name, active, roles, email, password):
        self.name = name
        self.email = email.lower()
        self.active = active
        self.roles = roles
        self.set_password(password)
    
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

class ExtendedLoginForm(LoginForm):
    name = TextField('Name', [DataRequired()])
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(
            name=self.name.data).first()
        if user is None:
            self.name.errors.append('Unknown username')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=ExtendedLoginForm)


# Create a user to test with
def create_user_and_role():
    first_user = User.query.filter(User.name == str('steve')).first()
    if not first_user:
        user_email = 'oneperstephen@gmail.com'
        username = 'steve'
        user_pass = 'password'
        the_user = user_datastore.create_user(email=user_email, name=username, password=user_pass)
        the_role = user_datastore.create_role(name='admin', description='The administrator')
        user_datastore.add_role_to_user(the_user, the_role)
        db.session.commit()
        try:
            is_container = DockerBackend.get_container_info(username)
        except Exception, e:
            the_new_dhbox = DockerBackend.setup_new_dhbox(username, user_pass, user_email)

# Make database if it doesn't exist
if not os.path.exists('dhbox-docker.db'):
    db.create_all()
    create_user_and_role()

"""
URLS/VIEWS
"""

@app.route('/test')
def test():
    from time import sleep
    return render_template('test.html')
            
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/our_team')
def our_team():
    return render_template('our_team.html')

@app.route('/get_started')
def get_started():
    return render_template('get_started.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     print 'asdasd'
    #     # login and validate the user...
    #     login_user(user)
    #     flash("Logged in successfully.", 'alert-success')
    #     return redirect(url_for("user_box", the_user=user.name) or url_for("index"))
    return render_template("login.html", form=form)


@app.route('/admin')
@login_required
@roles_required('admin')
def admin():
    containers = DockerBackend.all_containers()
    return render_template('admin.html', containers=containers)

@app.route("/dhbox/<the_user>")
@login_required
def user_box(the_user):
    which_user = User.query.filter(User.name == str(the_user)).first()
    if which_user is None:
        return redirect(url_for("index"))
    if current_user.name is not which_user.name:
        return redirect(url_for("index"))
    dhbox_username = which_user.name
    port_info = DockerBackend.get_all_exposed_ports(dhbox_username)
    hostname = DockerBackend.get_hostname()
    resp = make_response(render_template('my_dhbox.html', user=the_user, apps=all_apps))
    return resp

@app.route("/dhbox/<the_user>/<app_name>")
@login_required
def app_box(the_user, app_name):
    which_user = User.query.filter(User.name == str(the_user)).first()
    dhbox_username = which_user.name
    which_app = all_apps[app_name]
    port_info = DockerBackend.get_container_port(dhbox_username, which_app)
    hostname = DockerBackend.get_hostname()
    location = hostname+":"+port_info
    return redirect('http://'+location)

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
                    print "Username taken. Already has a DH Box."
                    return str('failure')
                admin_user = user['name']
                admin_email = user['email']
                admin_pass = user['pass']
                admin_user_object = user_datastore.create_user(email=admin_email, name=admin_user, password=admin_pass)
                db.session.commit()
                login_user(admin_user_object)
                the_new_dhbox = DockerBackend.setup_new_dhbox(admin_user, admin_pass, admin_email)
    return str('Successfully created a new DH Box.')

@app.route('/kill_dhbox', methods=['POST'])
def kill_dhbox():
    next = request.form['next'] 
    user = request.form['user']
    user = User.query.filter(User.name == user).first()
    DockerBackend.kill_dhbox(user.name, delete_image=True)
    db.session.delete(user)
    db.session.commit()
    flash(message='DH Box and username deleted.', category='alert-success')
    return redirect(url_for(next) or url_for("index"))

if __name__ == '__main__':
	app.debug = True
	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port, threaded=True)
	# app.run()