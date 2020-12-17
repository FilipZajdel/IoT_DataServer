from external_db import get_all
from models import Sensor, Reading, User, save_external_db_record


# Copy database to local database
readings = get_all()
for reading in readings:
    save_external_db_record(reading)

# Grant sudo user all sensors
sensors = Sensor.get()
sudo = User.find("sudo")

for sensor in sensors:
    sudo.grant_sensor_access(sensor)

