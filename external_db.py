import mysql.connector as connector
import json
import os

"""
    This is not a proper solution !!!
    
    Assuming that table looks like:
    ID, DATE, VALUE, UNIT, SENSOR, TYPE
"""


db_name = None
db_host = None
db_user = None
db_password = None

try:
    credentials_filepath = os.environ['CREDENTIALS_PATH']
    with open(credentials_filepath) as creds:
        data = json.load(creds)
        db_name = data.get("db-name")
        db_host = data.get("db-host")
        db_user = data.get("db-user")
        db_password = data.get("db-password")
except (IOError, KeyError):
    print("There is no CREDENTIALS_PATH environment variable set!!\n"
          "Please, set it prior to have support of external DB")

def get_all():

    db = connector.connect(host=db_host, database=db_name, user=db_user, password=db_password)
    cursor = db.cursor()
    cursor.execute("SELECT * FROM data")

    data = cursor.fetchall()
    db.disconnect()

    return data

def get_by_date(begin, end):
    
    db = connector.connect(host=db_host, database=db_name, user=db_user, password=db_password)
    cursor = db.cursor()
    cursor.execute(f"SELECT * FROM data WHERE DATE BETWEEN \'{begin}\' AND \'{end}\'")

    data = cursor.fetchall()
    db.disconnect()
    return data

