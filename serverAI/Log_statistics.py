from datetime import datetime, date
from time import strftime

import pymysql

def nextDay(day):


def countDayRows(day):
    # Open database connection
    db = pymysql.connect("localhost", "admin", "admin", "smartwifi")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM csv_data WHERE time REGEXP \'" + str(day) + " *\'")
    rows = [day, cursor.fetchone()[0]]
    db.close()

    return rows

#def countDaysRows(dayMin, dayMax):



print(countDayRows(date(2018, 3, 7)))
print(date(2018, 3, 7))