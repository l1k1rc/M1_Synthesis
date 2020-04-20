#!/usr/bin/python3

import pymysql

# Open database connection
db = pymysql.connect("localhost","l1k1","raccoon","projetM1" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT COUNT() FROM csv_data; ")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print ("Database version : %s " % data)

# disconnect from server
db.close()