# needed import for flask-triangle to work
import os
import builtins

builtins.unicode = str

from flask import Flask, jsonify, render_template, url_for, request, session, flash, redirect
from flask.ext.triangle import Triangle

# create a Flask app that plays nice with AngularJS
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.config.from_object('_config')
Triangle(app)

### helper functions ###

# source: https://github.com/mitsuhiko/flask/issues/824 by Chris Newhouse (newhouse)
def my_url_for(*args, **kwargs):
    with app.test_request_context():
        kwargs['_external'] = True  # Add the _external=True keyword argument to whatever else was passed
        url = url_for(*args, **kwargs)  # Get the URL
        if app.config['PORT'] is not None:  # If we have a port, we should do something
            url = url.replace('://localhost/',
                              '://localhost:%d/' % (app.config['PORT']))  # Oh yeah, add the port to the URL
        return url

def format_url(url):
    return '//localhost:{}/'.format(app.config['PORT']) + url + '/'

# add helper functions to jinja2 templating engine
app.jinja_env.globals.update(my_url_for=my_url_for)
app.jinja_env.globals.update(format_url=format_url)

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(my_url_for('login'))

    return wrap

# route handlers
@app.route('/logout/', methods=['GET'])
def lougout():
    session.pop('logged_in', None)
    flash('Goodbye!')
    return redirect(my_url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid login. Try again!'
            return render_template('login.html', error=error)
        else:
            session['logged_in'] = True
            flash('Welcome')
            # get the predictions upon login
            return redirect(my_url_for('orders'))
    return render_template('login.html')


@app.route('/orders')
def orders():
    data = {
        "2015-06-01": {
            "dough": 16,
            "cheese": 15,
            "pepperoni": 17
        },
        "2015-06-02": {
            "dough": 21,
            "cheese": 22,
            "pepperoni": 23
        }
    }
    return jsonify(data)
