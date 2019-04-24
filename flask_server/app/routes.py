from flask import render_template, request, redirect, session
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
    session.clear()
    # Todo : Make search
    
    return render_template('index.html', title='CSE DB', user=user)


@app.route('/add')
def cite_net():
    user = {'username': 'Soham'}

    fos_list = [['F-0', 'Error Correction and Code-Switching'], ['F-1', 'Word Segmentation'], ['F-2', 'Natural Language Processing'], ['F-3', 'Computational Linguitics on Twitter'], ['F-4', 'Dialogue and Discourse'], ['F-5', 'Sentiment Analysis'], ['F-6', 'Speech Recognition'], ['F-7', 'Information Extraction'], ['F-8', 'Word-Sense Disambiguation'], ['F-9', 'Lexical Acquisition'], ['F-10', 'Machine Translation'], ['F-11', 'Semantic Similarity'], ['F-12', 'Dependency Parsing'], ['F-13', 'Language Annotation'], ['F-14', 'Multilingual NLP']]

    return render_template('mods.html', title='CSE DB', user=user, fos_list = fos_list)


@app.route('/submit', methods = ['POST'])
def submit():

    fos_list = [['F-0', 'Error Correction and Code-Switching'], ['F-1', 'Word Segmentation'], ['F-2', 'Natural Language Processing'], ['F-3', 'Computational Linguitics on Twitter'], ['F-4', 'Dialogue and Discourse'], ['F-5', 'Sentiment Analysis'], ['F-6', 'Speech Recognition'], ['F-7', 'Information Extraction'], ['F-8', 'Word-Sense Disambiguation'], ['F-9', 'Lexical Acquisition'], ['F-10', 'Machine Translation'], ['F-11', 'Semantic Similarity'], ['F-12', 'Dependency Parsing'], ['F-13', 'Language Annotation'], ['F-14', 'Multilingual NLP']]

    paper = request.form.get("paper")
    keywords = request.form.get("keywords")
    authors = request.form.get("authors")
    conference = request.form.get("conferences")
    references = request.form.get("references").split(",")
    affiliations = request.form.get("affiliations").split(",")

    keywords_list = keywords.split(",")
    
    summary = request.form.get("summary")

    fos = list()
    for f in fos_list:
        if request.form.get(f[1]):
            fos.append(1)
        else:
            fos.append(0)

    return "submitted successfully"

@app.route('/search_nlp', methods = ['POST'])
def nlp_query():
    query = request.form.get("nlp")

