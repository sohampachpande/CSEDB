from flask import render_template, request, redirect, url_for
from app import app

from app import db

@app.route('/search', methods = ['GET', 'POST'])
def search():
    cursor = db.cursor()

    q_author = request.form.get("Author")
    q_conference = request.form.get("Conference")
    q_paper = request.form.get("Paper")



    if len(q_author)>0:
        q_author = request.form.get("Author")
        print("hi author", q_author)
        cursor.execute('CALL autname_nlq("{}")'.format(q_author))
        return_list = cursor.fetchall()
        return render_template('result_author.html')

    elif len(q_conference)>0:
        q_conference = request.form.get("Conference")
        print("hi conf", q_conference)
        cursor.execute('CALL conferencename_nlq("{}")'.format(q_conference))
        return_list = cursor.fetchall()
        return render_template('result_conference.html')

    elif len(q_paper)>0:
        q_paper = request.form.get("Paper")
        print("hi paper", q_paper)
        cursor.execute('CALL papername_nlq("{}")'.format(q_paper))
        return_list = cursor.fetchall()
        return render_template('result_paper.html')

    else:
        return redirect(url_for('index'))


    cursor.close()
    # print("\n\n\n",return_list,"\n\n\n")
    return "Hi"
