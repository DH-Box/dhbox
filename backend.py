import os
from flask import Flask, request, redirect, url_for, render_template, flash, make_response, jsonify, send_file
import launch_instance

# create application
app = Flask('dhbox')

"""
URLS/VIEWS
"""

# API
@app.route('/dhbox', methods=['POST'])
def dhbox():
    admin = request.form['admin']
    users = request.form.getlist('users')  # Get every form item with name='users' and create a list
    print admin
    # print request.data
    return str(request.data)
    # output = render_template('knowledge_base.html', entries=entries)
    # return output

if __name__ == '__main__':
    app.debug = True
    # Bind to PORT if defined, otherwise default to 3000.
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
    # app.run()
