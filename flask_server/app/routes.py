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


@app.route('/author_all', methods = ['GET'])
def get_all_authors():
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('SELECT * FROM authors ')
    l = cursor.fetchall()
    # Fetch a single row using fetchone()
    # data = cursor.fetchone()
    print(l)
    return render_template('authorsAll.html', authors = l)


@app.route('/papers_all', methods = ['GET'])
def get_all_papers():
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('SELECT * FROM test_table ')
    l = cursor.fetchall()
    # Fetch a single row using fetchone()
    # data = cursor.fetchone()
    print(l)
    return render_template('papersAll.html', pages = l)


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


@app.route('/author/<int:author_id>', methods = ['GET'])
def get_author_page(author_id):
    #must return author individual page
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('SELECT * FROM authors WHERE  aid = "{}"'.format(author_id))
    l = cursor.fetchall()
    # Fetch a single row using fetchone()
    # data = cursor.fetchone()
    print(l)
    return render_template('author_temp.html', author=l[0])



@app.route('/search', methods = ['POST'])
def search():
    name = request.form['Author']
    conference = request.form['Conference']
    year = request.form['Year']
    s = "The name is: " + name + "\nYear is " + year + conference
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('SELECT * FROM test_table ')
    l = cursor.fetchall()

    # Fetch a single row using fetchone()
    # data = cursor.fetchone()
    print(l)
    print(s)
    # disconnect from server
    return s