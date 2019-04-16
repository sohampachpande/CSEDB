from flask import render_template, request, redirect
from app import app

from app import db

@app.route('/conferences_all', methods = ['GET'])
def get_all_confs():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM ConferenceTable')
    l = cursor.fetchall()
    return render_template('confsAll.html', pages = l)


@app.route('/conference/<conf_id>', methods = ['GET'])
def get_conf_individual(conf_id):
    cursor = db.cursor()
    return 'Page Incomplete'

