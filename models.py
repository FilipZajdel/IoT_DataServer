from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
import logging
from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

engine = create_engine('sqlite:///database.db', echo=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

association_table = db.Table("association", Base.metadata,
    db.Column("Users_id", db.Integer, db.ForeignKey("Users.id")),
    db.Column("Sensors_id", db.Integer, db.ForeignKey("Sensors.id"))
)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# Set your classes here.

class User(UserMixin, Base):
    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    priviledged = db.Column(db.Boolean)
    acc_sensors = db.relationship("Sensor", secondary=association_table,
                                  back_populates="users")

    # It shouldn't be stored in here
    password = db.Column(db.String(30))

    def __init__(self, name, password, email, priviledged=False):
        self.name = name
        self.password = password
        self.email = email
        self.priviledged = priviledged

    def __repr__(self):
        return f"<User {self.id}>, name: {self.name}, email: {self.email}"

    def remove(self):
        db_session.delete(self)
        db_session.commit()

    def create(name, email, password, priviledged=False):

        if (User._exist(name)):
            logging.debug(f"User couldn't be created: {name} {email} {password}")
            return False
        
        new_user = User(name=name, email=email, password=password,
                        priviledged=priviledged)

        db_session.add(new_user)
        db_session.commit()

        if priviledged:
            for sensor in Sensor.get():
                new_user.grant_sensor_access(sensor)

        logging.debug(f"Created user: {name} {email} {password}")

    def grant_sensor_access(self, sensor):
        if sensor not in self.acc_sensors:
            self.acc_sensors.append(sensor)
            db_session.add(self)
            db_session.commit()

    def del_sensor_access(self, sensor):
        if sensor in self.acc_sensors:
            self.acc_sensors.remove(sensor)

    def find(name):
        return User.query.filter_by(name=name).first()

    def _exist(name) -> bool:
        return User.query.filter_by(name=name).first() is not None

    def check_creds(name, password) -> bool:
        user = User.find(name)
        if user is not None:
            return user.password == password
        
        return False

    def get_sensors(self):
        return self.acc_sensors

    def get_all():
        return User.query.all()


class Sensor(Base):
    __tablename__ = 'Sensors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    measured_quantity = db.Column(db.String(30))
    users = db.relationship("User", secondary=association_table,
                            back_populates="acc_sensors")

    def __init__(self, name, measured_quantity):
        self.name = name
        self.measured_quantity = measured_quantity

    def __repr__(self):
        return f"<{self.name}> <users granted: {self.users}>"

    def create(name, measured_quantity):
        db_session.add(Sensor(name=name, measured_quantity=measured_quantity))
        db_session.commit()

    def find(name):
        return Sensor.query.filter_by(name=name).first()
    
    def readings(self):
        return Reading.query.filter_by(sensor_id=self.id).all()

    def get(name=None):
        if name is None:
            return Sensor.query.all()
        else:
            return Sensor.find(name)

class Reading(Base):
    __tablename__ = 'Readings'

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(30))
    unit = db.Column(db.String(5))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    sensor_id = db.Column(db.Integer, db.ForeignKey("Sensors.id"))

    def __init__(self, value, unit, timestamp, sensor_id):
        self.value = value
        self.unit = unit
        self.timestamp = timestamp
        self.sensor_id = sensor_id

    def __repr__(self):
        return f"<{self.value} {self.unit} {self.timestamp}>"

    def create(value, unit, sensor_id, timestamp=datetime.utcnow()):
        db_session.add(Reading(value=value, unit=unit, sensor_id=sensor_id,
                        timestamp=timestamp))
        db_session.commit()

    def dict(self):
        return {
            "value" : self.value,
            "unit" : self.unit,
            "timestamp" : self.timestamp
        }

# Create tables.
Base.metadata.create_all(bind=engine)
