from flask import render_template, request, redirect
from app import app

from app import db

def FirstNameLastName(name):
    l_n = name.split(",")
    return l_n[-1]+', '+ l_n[0]

# # Connect to the database
# db = PyMySQL.connect("10.0.25.35","sohamp","s27498","CSResearchPapers" )

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Soham'}

    # Todo : Make search
    
    return render_template('index.html', title='CSE DB', user=user)


@app.route('/conferences_all', methods = ['GET'])
def get_all_confs():
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('SELECT * FROM test_table ')
    l = cursor.fetchall()
    # Fetch a single row using fetchone()
    # data = cursor.fetchone()
    print(l)
    return render_template('confsAll.html', pages = l)


@app.route('/search', methods = ['POST'])
def search():
    # name = request.form['Author']
    # conference = request.form['Conference']
    # year = request.form['Year']
    # s = "The name is: " + name + "\nYear is " + year + conference
    # prepare a cursor object using cursor() method
    # cursor = db.cursor()
    # execute SQL query using execute() method.
    # cursor.execute('SELECT * FROM test_table ')
    # l = cursor.fetchall()

    # Fetch a single row using fetchone()
    # data = cursor.fetchone()
    # print(l)
    # print(s)
    # disconnect from server
    return s