#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from flask import Flask, render_template, request, url_for, redirect, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import (login_required, LoginManager, current_user, login_user,
                         logout_user)
import logging
from logging import Formatter, FileHandler
from forms import *
from functools import wraps
from datetime import datetime, timedelta
import os

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)

# Automatically tear down SQLAlchemy.
@app.teardown_request
def shutdown_session(exception=None):
    # TODO: Properly shutdown session
    db.session.remove()


# Login required decorator.

# def login_required(test):
#     @wraps(test)
#     def wrap(*args, **kwargs):
#         if 'logged_in' in session:
#             return test(*args, **kwargs)
#         else:
#             flash('You need to login first.')
#             return redirect(url_for('login'))
#     return wrap
@login_manager.unauthorized_handler
def unauthorized_cb():
    return redirect(url_for('login'))

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#
import models

@app.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@app.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        if not models.User.check_creds(form.name.data, form.password.data):
            return render_template('forms/login.html', form=form)
        
        print(models.User.find(form.name.data))
        login_user(models.User.find(form.name.data))
        return redirect(url_for('home'))

    return render_template('forms/login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


@app.route('/sensors/<sensor_name>/readings')
@login_required
def readings(sensor_name):
    sensor = models.Sensor.find(sensor_name)
    period_end = datetime.utcnow()
    period_begin = period_end - timedelta(days=2)

    if sensor is None:
        return abort(404)

    readings = sensor.readings()
    return render_template('pages/placeholder.readings.html', readings=readings,
                            sensor=sensor, period_end=period_end.isoformat(),
                            period_begin=period_begin.isoformat())

@app.route('/sensors')
@login_required
def sensors():
    sensors_list = current_user.get_sensors()
    return render_template('pages/placeholder.sensors.html', sensors=sensors_list)

@app.route('/users')
@login_required
def users():
    if not current_user.priviledged:
        return abort(403)

    return render_template('pages/placeholder.users.html', 
                           users=models.User.get_all())

@app.route('/user/<user_name>')
def user_profile(user_name):
    # TODO: Implement that for admin
    pass


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    #db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def access_denied_error(error):
    return "You don't have access to see this content."

if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

import api
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
