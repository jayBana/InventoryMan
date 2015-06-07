from functools import wraps
from flask import Flask, flash, session, redirect, url_for, request, render_template

# config
app = Flask(__name__)
app.config.from_object('_config')

# helper functions

# source: https://github.com/mitsuhiko/flask/issues/824 by Chris Newhouse (newhouse)
def my_url_for(*args, **kwargs):
    with app.test_request_context():
        kwargs['_external'] = True  # Add the _external=True keyword argument to whatever else was passed
        url = url_for(*args, **kwargs)  # Get the URL
        if app.config['PORT'] is not None:  # If we have a port, we should do something
            url = url.replace('://localhost/',
                              '://localhost:%d/' % (app.config['PORT']))  # Oh yeah, add the port to the URL
        return url


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
@app.route('/logout/')
def lougout():
    session.pop('logged_in', None)
    print(session)
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
            return redirect(my_url_for('orders'))
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
