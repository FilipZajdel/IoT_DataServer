from flask import Flask, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import (login_required, LoginManager, current_user, login_user,
                         logout_user)
import models
from app import app, db
from datetime import datetime

endpoints_args = {
    "api_readings" : {
        "dateFrom" : "required",
        "dateTo"   : "required"
    }
}

@app.route("/api/sensors/<sensor_name>/readings")
@login_required
def api_readings(sensor_name):
    if not api_readings_validate(request):
        return jsonify({}), 404

    dateFrom = datetime.fromisoformat(request.args.get("dateFrom"))
    dateTo = datetime.fromisoformat(request.args.get("dateTo"))

    readings = models.Sensor.find(sensor_name) \
                            .get_readings_by_date(dateFrom, dateTo)
    readings = [reading.dict() for reading in readings]

    return jsonify({"readings":readings}), 200


def api_readings_validate(request):
    if request.args is None or len(request.args) == 0:
        return False
    
    args = endpoints_args["api_readings"]
    for arg, is_required in args.items():
        if arg not in request.args and is_required:
            return False
    
    return True