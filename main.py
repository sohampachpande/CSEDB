#!/usr/bin/python3

import pymysql as PyMySQL

# Open database connection
db = PyMySQL.connect("localhost","root","@Cooker123","test" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
cursor.execute("SELECT VERSION()")

# Fetch a single row using fetchone()
data = cursor.fetchone()
print ("Database version : %s " % data)

# disconnect from server
db.close()