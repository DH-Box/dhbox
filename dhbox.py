import os, os.path, sys, random, string, time
from flask import Flask, flash, request, redirect, url_for, render_template, \
    make_response, jsonify, send_file, current_app, g, abort
import ast
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_user, \
    UserMixin, RoleMixin, login_required, roles_required, registerable, current_user, LoginForm
from flask_mail import Mail, Message
from wtforms.validators import DataRequired
from wtforms import TextField, Form
from werkzeug import generate_password_hash, check_password_hash
from werkzeug.contrib.fixers import ProxyFix
import schedule
from threading import Thread
import DockerBackend
from datetime import datetime, timedelta

# create application
app = Flask('dhbox')
app.wsgi_app = ProxyFix(app.wsgi_app)

# install_secret_key(app)
app.config.from_pyfile('config.cfg')
app.template_folder = 'src/templates' if app.config['TESTING'] else 'dist/templates'
app.static_folder = 'src/static' if app.config['TESTING'] else 'dist/static'
# Create database connection object
db = SQLAlchemy(app)

# Set up email
# mail = Mail(app)
# app.config.update(
#     #EMAIL SETTINGS
#     MAIL_DEBUG = True,
#     MAIL_SUPPRESS_SEND = False,
#     TESTING = False,
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT=465,
#     MAIL_USE_SSL=True,
#     MAIL_USERNAME = 'dhboxsignup@google.com',
#     MAIL_PASSWORD = 'dhbox123'
#     )


all_apps = [
    {'name': 'mallet', 'wiki-page': 'MALLET', 'display-name': 'MALLET'},
    {'name': 'ntlk', 'wiki-page': 'NLTK', 'display-name': 'NLTK'},
    {'name': 'bash', 'port': '3000', 'wiki-page': 'Bash-shell', 'display-name': 'Command Line'},
    {'name': 'rstudio', 'port': '8787', 'wiki-page': 'R-Studio', 'display-name': 'R Studio'},
    {'name': 'omeka', 'port': '8080', 'wiki-page': 'Omeka', 'display-name': 'Omeka'},
    {'name': 'brackets', 'port': '4444', 'wiki-page': 'Brackets', 'display-name': 'Brackets'},
    {'name': 'apache', 'port': '80', 'hide': True},
    {'name': 'jupyter', 'port': '8888', 'wiki-page': 'ipython', 'display-name': 'Jupyter Notebooks'},
    {'name': 'wordpress', 'port': '80', 'wiki-page': 'wordpress', 'display-name': 'WordPress'},
]


def get_app(key):
    for app in all_apps:
        if app['name'] == key:
            return app

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
    dhbox_duration = db.Column(db.Integer)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, name, active, roles, email, password, dhbox_duration):
        self.name = name
        self.email = email.lower()
        self.active = active
        self.roles = roles
        self.dhbox_duration = dhbox_duration
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


# Create an admin user to test with
def create_user_and_role():
    first_user = User.query.filter(User.name == str('admin')).first()
    if not first_user:
        user_email = 'test@gmail.com'
        username = 'admin'
        user_pass = app.config['ADMIN_PASS']
        the_user = user_datastore.create_user(email=user_email, name=username, password=user_pass, dhbox_duration=1000000000)
        the_role = user_datastore.create_role(name='admin', description='The administrator')
        user_datastore.add_role_to_user(the_user, the_role)
        db.session.commit()
        try:
            DockerBackend.get_container_info(username)
            print 'already have a container'
        except Exception:
            DockerBackend.setup_new_dhbox(username, user_pass, user_email)


def delete_user(user):
    try:
        user = User.query.filter(User.name == user).first()
        db.session.delete(user)
        db.session.commit()
    except Exception, e:
        print e


"""
URLS/VIEWS
"""


@app.route("/test/<the_user>")
def test(the_user):
    which_user = User.query.filter(User.name == str(the_user)).first()
    if which_user is None:
        return redirect(url_for("index"))
    if current_user.name is not which_user.name:
        return redirect(url_for("index"))
    email_domain = which_user.email.split("@", 1)[1]
    if email_domain == 'demo.com':
        demo = True
    else:
        demo = False
    dhbox_username = which_user.name
    time_left = which_user.dhbox_duration - DockerBackend.how_long_up(which_user.name)
    time_left = DockerBackend.display_time(time_left)
    resp = make_response(render_template('alt_dhbox.html',
                     user=the_user,
                     apps=filter(lambda app: app.get('hide', False) != True, all_apps),
                     demo=demo,
                     time_left=time_left
                     )
                 )
    return resp


@app.route("/")
def index():
    return render_template('index.html', institution=app.config['INSTITUTION'], demo=app.config['DEMO_ENABLED'])


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


@app.route('/demo', methods=["GET"])
def demo():
    username = 'demo' + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    demo_user_object = user_datastore.create_user(email=username + '@demo.com', name=username, password='demo', dhbox_duration=3600)
    db.session.commit()
    login_user(demo_user_object)
    DockerBackend.demo_dhbox(username)
    return redirect('/dhbox/' + username, 301)


@app.route("/login", methods=["GET", "POST"])
def login():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     # login and validate the user...
    #     login_user(user)
    #     flash("Logged in successfully.", 'alert-success')
    #     return redirect(url_for("user_box", the_user=user.name) or url_for("index"))
    return render_template("login.html", form=form)


@app.route('/admin')
@login_required
@roles_required('admin')
def admin():
    containers = User.query.all()
    containers_list = []
    for container in containers:
        uptime = DockerBackend.how_long_up(container.name)
        time_left = DockerBackend.check_if_over_time(container)
        time_left = DockerBackend.display_time(time_left)
        info = DockerBackend.get_container_info(container.name)
        containers_list.append({'name':container.name, 'uptime':uptime, 'time_left':time_left})
    return render_template('admin.html', containers=containers_list)


@app.route("/dhbox/<the_user>")
@login_required
def user_box(the_user):
    which_user = User.query.filter(User.name == str(the_user)).first()
    if which_user is None:
        return redirect(url_for("index"))
    if current_user.name is not which_user.name:
        return redirect(url_for("index"))
    email_domain = which_user.email.split("@", 1)[1]
    if email_domain == 'demo.com':
        demo = True
    else:
        demo = False
    dhbox_username = which_user.name
    time_left = which_user.dhbox_duration - DockerBackend.how_long_up(which_user.name)
    time_left = DockerBackend.display_time(time_left)
    resp = make_response(render_template('my_dhbox.html',
                                         user=the_user,
                                         apps=filter(lambda app: app.get('hide', False) != True, all_apps),
                                         demo=demo,
                                         time_left=time_left
                                         )
                         )
    return resp


@app.route("/dhbox/<the_user>/<app_name>")
@login_required
def app_box(the_user, app_name):
    which_user = User.query.filter(User.name == str(the_user)).first()
    dhbox_username = which_user.name
    if app_name == 'wordpress':
        app_port = get_app(app_name)['port']
        port_info = DockerBackend.get_container_port(dhbox_username+'_wp', app_port)
    else:
        app_port = get_app(app_name)['port']
        port_info = DockerBackend.get_container_port(dhbox_username, app_port)
    hostname = DockerBackend.get_hostname()
    location = hostname + ":" + port_info
    if app_name == 'omeka':
        return redirect('http://' + location+'/admin')
    else:
        return redirect('http://' + location)


@app.route('/new_dhbox', methods=['POST'])
def new_dhbox():
    data = {key: request.form.getlist(key)[0] for key in request.form.keys()}
    for key in data:
        users_dict = key
    users_dict = ast.literal_eval(users_dict)
    users = users_dict['users']
    for user in users:
        if 'name' in user:
            if 'email' in user:  # Then is DH Box admin
                name_check = User.query.filter(User.name == user['name']).first()
                email_check = User.query.filter(User.name == user['email']).first()
                if name_check or email_check:
                    print "Username taken. Already has a DH Box."
                    return str('failure')
                admin_user = user['name']
                admin_email = user['email']
                admin_pass = user['pass']
                if user['duration'] == 'day':
                    duration = 86400
                elif user['duration'] == 'week':
                    duration = 604800
                else:
<<<<<<< HEAD
                    duration = 13148730
=======
                    duration = 2592000
                # if user['duration'] == 'week':
                #     duration = 604800
                # elif user['duration'] == 'month':
                #     duration = 2592000
                # else:
                #     duration = 13148730 
>>>>>>> master
                admin_user_object = user_datastore.create_user(email=user['email'], name=user['name'], password=user['pass'], dhbox_duration=duration)
                db.session.commit()
                login_user(admin_user_object)
                the_new_dhbox = DockerBackend.setup_new_dhbox(admin_user, admin_pass, admin_email)
    return str('Successfully created a new DH Box.')


@app.route('/kill_dhbox', methods=['POST'])
@login_required
def kill_dhbox():
    the_next = request.form.get('next')
    user = request.form.get('user')
    print(user)
    if current_user.has_role("admin"):
        pass
    elif user != current_user.name:
        # If they're not an admin and they're trying to delete a user that isn't them,
        # return a Forbidden error.
        return abort(403)
    DockerBackend.kill_and_remove_user(user)
    flash(message='DH Box and username deleted.', category='alert-success')
    return redirect(url_for(the_next) or url_for("index"))


def police():
<<<<<<< HEAD
    if os.path.isfile('dhbox-docker.db'):
        users = User.query.all()
        for user in users:
            DockerBackend.check_and_kill(user)
        all_containers = DockerBackend.all_containers()
        for container in all_containers:
            time_up = DockerBackend.how_long_up(container)
            info = DockerBackend.get_container_info(container)
            name = info['Name'][1:]
            # print name, "time up:", time_up
            if name.startswith('demo') and time_up > 60:
                DockerBackend.kill_and_remove_user(name)

=======
    users = User.query.all()
    for user in users:
        DockerBackend.check_and_kill(user)
    all_containers = DockerBackend.all_containers()
    for container in all_containers:
        time_up = DockerBackend.how_long_up(container)
        info = DockerBackend.get_container_info(container)
        name = info['Name'][1:]
        if name.startswith('demo') and time_up > 3600:
            DockerBackend.kill_and_remove_user(name, user=False)
>>>>>>> master

def run_schedule():
    while 1:
        schedule.run_pending()
        time.sleep(1)


schedule.every(1).minutes.do(police)
t = Thread(target=run_schedule)
t.daemon = True
t.start()

if __name__ == '__main__':
    app.debug = app.config['TESTING'] or app.config['SERVER_TESTING']
    # Make database if it doesn't exist
    if not os.path.exists('dhbox-docker.db'):
        db.create_all()
        create_user_and_role()
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, threaded=True)
