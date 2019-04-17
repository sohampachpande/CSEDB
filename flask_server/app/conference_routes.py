from flask import render_template, request, redirect
from app import app

from app import db

@app.route('/conferences_all', methods = ['GET'])
def get_all_confs():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM ConferenceTable')
    l = cursor.fetchall()

    confs = list()
    d = dict()
    for i in l:
        try:
            d[i[1]].append((int(i[2]), i[0]))
        except:
            d[i[1]] = [(int(i[2]), i[0])]
    for i in list(d.keys()):
        confs.append((i, sorted(d[i], key=lambda x: x[0])))
    print(confs[0])
    return render_template('confsAll.html', pages = confs)


@app.route('/conference/<conf_id>', methods = ['GET'])
def get_conf_individual(conf_id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM ConferenceTable WHERE ConferenceID="{}"'.format(conf_id))
    conf_details = cursor.fetchall()
    print(conf_details)
    return render_template('conf_temp.html', conf = conf_details[0])
