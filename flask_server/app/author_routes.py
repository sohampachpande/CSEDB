from flask import render_template, request, redirect
from app import app

from app import db

@app.route('/author_all', methods = ['GET'])
def get_all_authors():
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('SELECT * FROM AuthorTable ')
    l = cursor.fetchall()


    return render_template('authorsAll.html', authors = l)


# @app.route('/author_all/<a_letter>', methods = ['GET'])
# def get_author_by_startingLetter(a_letter):
#     cursor = db.cursor()
#     # execute SQL query using execute() method.
#     cursor.execute('SELECT * FROM authors ')
#     l = cursor.fetchall()
#     # Fetch a single row using fetchone()
#     # data = cursor.fetchone()
#     print(l)
#     return render_template('authorsAll.html', authors = l)



@app.route('/author/<author_id>', methods = ['GET'])
def get_author_page(author_id):
    #must return author individual page
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('SELECT * FROM AuthorTable WHERE  AuthorID = "{}"'.format(author_id))
    l = cursor.fetchall()

    cursor.execute('call FOS("{}")'.format(author_id))
    a_field = cursor.fetchall()

    cursor.execute('call aut_conf("{}")'.format(author_id))
    a_conf = cursor.fetchall()

    cursor.execute('call aut_paper("{}")'.format(author_id))
    a_papers = cursor.fetchall()

    cursor.execute('call coauthor("{}")'.format(author_id))
    a_coauth = cursor.fetchall()
    # x =  ['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
    y = [ 1, 3, 6,8 , 9, 0]
    x =  [1 , 2 , 3.5 , 4 , 5 , 6]
    print(l)
    return render_template('author_temp.html', author=l[0], auth_field=a_field, auth_conference=a_conf, auth_papers=a_papers, auth_coauth = a_coauth, x=x, y=y)


# @app.route('/author/<author_id>/papers', methods = ['GET'])
# def get_author_page(author_id):
#     #must return author individual page
#     cursor = db.cursor()
#     # execute SQL query using execute() method.

#     cursor.execute('call aut_conf("{}")'.format(author_id))
#     a_conf = cursor.fetchall()
#     print("a_conf", a_conf)

#     papers = l
#     confs = [['conf1', 'confid'], ['conf2', 'confid2']]
#     # x =  ['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
#     y = [ 1, 3, 6,8 , 9, 0]
#     x =  [1 , 2 , 3.5 , 4 , 5 , 6]
#     print(l)
#     return render_template('author_temp.html', author=l[0], auth_field=a_field, auth_conference=a_conf, x=x, y=y)
