from flask import render_template, request, redirect
from app import app
import pymysql as PyMySQL

import pymysql.cursors

# Connect to the database

db = PyMySQL.connect("localhost","root","@Cooker123","test" )

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Soham'}

    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute('SELECT * FROM test_table ')
    l = cursor.fetchall()

    # Fetch a single row using fetchone()
    # data = cursor.fetchone()
    print(l)

    return render_template('index.html', title='CSE DB', user=user)




@app.route('/form/', methods = ['POST'])
def form():
    name = request.form['Author']
    year = request.form['Year']
    s = "The name is: " + name + "\nYear is " + year


    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # execute SQL query using execute() method.
    cursor.execute('SELECT * FROM test_table ')
    l = cursor.fetchall()

    # Fetch a single row using fetchone()
    # data = cursor.fetchone()
    print(l)

    # disconnect from server

    return s
