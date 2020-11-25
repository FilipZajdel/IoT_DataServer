from models import User, Sensor, Reading

sensors = {"Termometer":"Celsius", "MoistureMeter":"%", "Manometer":"bar"}
users = ["John", "Alex", "Rob", "Matt"]

for sensor_name in sensors.keys():
    Sensor.create(sensor_name)

for sensor_name, unit in sensors.items():
    for i in range(120, 180, 1):
        Reading.create(str(i), unit, Sensor.find(sensor_name).id)

for user in users:
    User.create(name=user, email=f"{user}@domain.com", password="1234",
                priviledged=False)

User.find("Alex").grant_sensor_access(Sensor.find("Termometer"))
User.find("Alex").grant_sensor_access(Sensor.find("Manometer"))
User.find("Rob").grant_sensor_access(Sensor.find("MoistureMeter"))
User.find("Matt").grant_sensor_access(Sensor.find("Manometer"))
User.find("John").grant_sensor_access(Sensor.find("MoistureMeter"))
User.find("John").grant_sensor_access(Sensor.find("Manometer"))

# create super user
User.create(name="sudo", email="admin@domain.com", password="agh3nv-4dmin",
            priviledged=True)
