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
@app.route('/home')
def index():
    user = {'username': 'Soham'}

    # Todo : Make search
    
    return render_template('index.html', title='CSE DB', user=user)