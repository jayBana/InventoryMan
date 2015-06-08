from functools import wraps
from flask import Flask, flash, session, redirect, url_for, request, render_template
from get_results import get_predictions_all, get_predictions_subset

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
        print(url)
        return url

def format_url(url):
    return '//localhost:{}'.format(app.config['PORT']) + url

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
    print('hello')
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
            get_predictions_all()
            return redirect(my_url_for('orders'))
    return render_template('login.html')


@app.route('/orders/', methods=['GET', 'POST'])
@login_required
def orders():
    if request.method == 'POST':
        start_date = request.form['start']
        end_date = request.form['end']
        results, summed = get_predictions_subset(start_date, end_date)
    else:
        results, summed, start_date, end_date = get_predictions_subset()

    order_list = [dict(date=entry[0], name=entry[1], predicted=entry[2]) for entry in results]
    summed = [dict(name=k, total=v) for k, v in summed.items()]
    one_day = True if (end_date == start_date) else False

    return render_template(
        'orders.html',
        one_day=one_day,
        start_date=start_date,
        end_date=end_date,
        order_list=order_list,
        summed=summed
    )
