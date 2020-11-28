from models import User, Sensor, Reading
from time import sleep
from datetime import datetime
import random

tests_to_execute = []

# models.Sensor test
def get_readings_by_date_test():
    termometer = Sensor.find("Termometer")
    expected_readings_len = 24 - 12 + 1

    begin = datetime(2020, 11, 26, 17, 12)
    end = datetime(2020, 11, 26, 17, 24)

    readings = termometer.get_readings_by_date(begin, end)
    if len(readings) != expected_readings_len:
        print("get_readings_by_date_test: FAILED")
        print(f"Expected outcome {expected_readings_len}, " 
              f"Actual outcome {len(readings)}")
    else:
        print("get_readings_by_date_test: PASSED")

tests_to_execute.append(get_readings_by_date_test)
    
for test in tests_to_execute:
    test()