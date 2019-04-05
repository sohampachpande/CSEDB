from flask import render_template, request, redirect
from app import app

import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='user',
                             password='passwd',
                             db='test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Soham'}
    return render_template('index.html', title='CSE DB', user=user)


@app.route('/form/', methods = ['POST'])
def form():
    name = request.form['Author']
    year = request.form['Year']
    s = "The name is: " + name + "\nYear is " + year
    return s