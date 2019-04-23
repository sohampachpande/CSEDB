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


@app.route('/add')
def cite_net():
    user = {'username': 'Soham'}
    return render_template('mods.html', title='CSE DB', user=user)


@app.route('/submit', methods = ['POST'])
def submit():
    paper = request.form.get("paper")
    keywords = request.form.get("keywords")
    authors = request.form.get("authors")
    conferences = request.form.get("conferences")
    fos = request.form.get("fos")

    keywords_list = keywords.split(",")
    conferences_list = conferences.split(",")
    return "submitted successfully"