import os
from flask import Flask, request, redirect, url_for, render_template, flash, make_response, jsonify, send_file, current_app
import ansible_call
from datetime import timedelta
from functools import update_wrapper


# create application
app = Flask('dhbox')

"""
URLS/VIEWS
"""
# decorator
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


# API
@app.route('/dhbox', methods=['POST'])
@crossdomain(origin='*')
def dhbox():
    all_users = []
    admins = []
    admin = request.form['admin']
    users = request.form.getlist('users')  # Get every form item with name='users' and create a list
    admins.append(admin)
    for user in users:
        all_users.append(user)

    users_and_passes = []
    admins_and_passes = []
    for user in all_users:
        users_and_passes.append({'name': user, 'password': 'test'})
    for admin in admins:
        admins_and_passes.append({'name': admin, 'password': 'test'})
    print users_and_passes
    print admins_and_passes
    users_hashed_passes = ansible_call.user_set_passes(users_and_passes)
    admins_hashed_passes = ansible_call.user_set_passes(admins_and_passes)
    ansible_call.call_ansible(users_hashed_passes, admins_hashed_passes)
    return str(request.data)

if __name__ == '__main__':
    app.debug = True
    # Bind to PORT if defined, otherwise default to 3000.
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    # app.run()
