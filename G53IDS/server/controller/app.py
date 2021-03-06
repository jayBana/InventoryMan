# needed import for flask-triangle to work
import os
import builtins
from functools import wraps
from datetime import date

builtins.unicode = str
from server.ml_helpers.ml_studio_request import main as ml_std_req
from flask import Flask, jsonify, render_template, url_for, request, session, flash, redirect
from flask.ext.triangle import Triangle

# create a Flask app that plays nice with AngularJS
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates')
app = Flask(__name__, template_folder=tmpl_dir)
app.config.from_object('_config')
Triangle(app)

# globals
global results_info
global weather_info
global events_info

### helper functions ###
# source: https://github.com/mitsuhiko/flask/issues/824 by Chris Newhouse (newhouse)
def my_url_for(*args, **kwargs):
    with app.test_request_context():
        kwargs['_external'] = True  # Add the _external=True keyword argument to whatever else was passed
        url = url_for(*args, **kwargs)  # Get the URL
        if app.config['PORT'] is not None:  # If we have a port, we should do something
            url = url.replace('://localhost/',
                              '://%s:%d/' % (app.config['IP'], app.config['PORT']))  # Oh yeah, add the port to the URL
        else:
            url = url.replace('://localhost/',
                              '://%s/' % (app.config['IP']))
        return url

# custom url formater function used in html templates
def format_url(url):
    if app.config['PORT'] is not None:
        return '//{}:{}/'.format(app.config['IP'], app.config['PORT']) + url + '/'
    else:
        return '//{}/'.format(app.config['IP']) + url + '/'

# add helper functions to jinja2 templating engine
app.jinja_env.globals.update(my_url_for=my_url_for)
app.jinja_env.globals.update(format_url=format_url)

# function for getting results
def get_results():
    global results_info
    global weather_info
    global events_info
    results_info, events_info, weather_info = ml_std_req()


# wrapped login function
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


# landing (login) page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # check credentials against the ones stored in the config file
        if request.form['username'] != app.config['USERNAME'] or request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid login. Try again!'
            return render_template('login.html', error=error)
        else:
            # successful login
            session['logged_in'] = True
            flash('Welcome')
            # get the predictions upon login
            get_results()
            return redirect(my_url_for('index'))
    # pop session logged_in prevents user being able to press go back and still login
    session.pop('logged_in', None)
    return render_template('login.html')


# index page, showing today's date
@app.route('/index/', methods=['GET'])
def index():
    today = date.today().strftime("%Y-%m-%d")
    return render_template('index.html', today=today)


# return prediction results as json
@app.route('/data', methods=['GET'])
def results():
    return jsonify(orders=results_info)


# return events info as json
@app.route('/events', methods=['GET'])
def events():
    return jsonify(events=events_info)


# return weather info as json
@app.route('/weather', methods=['GET'])
def weather():
    return jsonify(weather=weather_info)
