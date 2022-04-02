from models import User, Sensor, Reading
from time import sleep
from datetime import datetime, timedelta
import random

sensors = {"Termometer (mock)":("Celsius", "Temperature"), 
           "Hygrometer (mock)":("%", "Humidity"),
           "Manometer (mock)":("bar", "Pressure")}
users = ["John", "Alex", "Rob", "Matt"]

for sensor_name, (unit, quantity) in sensors.items():
    Sensor.create(sensor_name, quantity)

# For the sake of tests
for sensor_name, (unit, quantity) in sensors.items():
    for i in range(120, 180, 1):
        t = datetime(2022, 3, 31, 17, i%60, 0)
        Reading.create(str(random.randint(20, 27)), unit, Sensor.find(sensor_name).id,
                       timestamp=t)

# Let's have 4 readings per hour
start_date = datetime.utcnow() - timedelta(days=4)
now = datetime.utcnow()
sampling_interval = timedelta(minutes=15)

for sensor_name, (unit, quantity) in sensors.items():
    sample_date = start_date
    while sample_date < now:
        Reading.create(str(random.randint(20, 27)), unit, Sensor.find(sensor_name).id,
                       timestamp=sample_date)
        sample_date = sample_date + sampling_interval

for user in users:
    User.create(name=user, email=f"{user}@domain.com", password="1234",
                priviledged=False)

User.find("Alex").grant_sensor_access(Sensor.find("Termometer (mock)"))
User.find("Alex").grant_sensor_access(Sensor.find("Manometer (mock)"))
User.find("Rob").grant_sensor_access(Sensor.find("Hygrometer (mock)"))
User.find("Matt").grant_sensor_access(Sensor.find("Manometer (mock)"))
User.find("John").grant_sensor_access(Sensor.find("Hygrometer (mock)"))
User.find("John").grant_sensor_access(Sensor.find("Manometer (mock)"))

# create super user
User.create(name="sudo", email="admin@domain.com", password="agh3nv-4dmin",
            priviledged=True)
