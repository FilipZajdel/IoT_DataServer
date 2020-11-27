from flask import Flask, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import (login_required, LoginManager, current_user, login_user,
                         logout_user)
import models
from app import app, db



@app.route("/api/sensors/<sensor_name>/readings")
@login_required
def api_readings(sensor_name):
    readings = models.Sensor.find(sensor_name).readings()

    readings = [reading.dict() for reading in readings]

    return jsonify({"readings":readings}), 200