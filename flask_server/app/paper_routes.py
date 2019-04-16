from flask import render_template, request, redirect
from app import app

from app import db


# All Papers page
@app.route('/papers_all', methods = ['GET'])
def get_all_papers():
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('SELECT * FROM PaperTable ')
    l = cursor.fetchall()

    print("\n\nNo of Papers\n\n",len(l))
    # for a in l:
    #     a[1] = FirstNameLastName(a[1])

    return render_template('papersAll.html', pages = l)


# Individual paper page
@app.route('/paper/<paper_id>', methods = ['GET'])
def individual_paper_page(paper_id):
	#must return author individual page
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('SELECT * FROM PaperTable WHERE  PaperID = "{}"'.format(paper_id))
    l = cursor.fetchall()


    cursor.execute('call  con_paper("{}")'.format(paper_id))
    confs = cursor.fetchall()
    # print(confs)

    cursor.execute('call author_paper("{}")'.format(paper_id))
    authors = cursor.fetchall()
   
    cursor.execute('call citation("{}")'.format(paper_id))
    references = cursor.fetchall()

    cursor.execute('call refers("{}")'.format(paper_id))
    papers_cite_this = cursor.fetchall()

    print(papers_cite_this)


    papers = l
    # x =  ['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
    y = [ 1, 3, 6,8 , 9, 0]
    x =  [1 , 2 , 3.5 , 4 , 5 , 6]
    # print(l)
    return render_template('paper_temp.html', paper=l[0], conferences = confs, authors = authors, references = references, papers_cite_this = papers_cite_this)

@app.route('/author/<author_id>/papers', methods = ['GET'])
def get_author_papers_page(author_id):
    #must return author individual page
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('select AuthorWritesPaper.PaperID from AuthorWritesPaper where AuthorWritesPaper.AuthorID = "{}"'.format(author_id))
    l = cursor.fetchall()
    # Fetch a single row using fetchone()
    # data = cursor.fetchone()
    papers = l
    confs = [['conf1', 'confid'], ['conf2', 'confid2']]
    # x =  ['2013-10-04 22:23:00', '2013-11-04 22:23:00', '2013-12-04 22:23:00'],
    y = [ 1, 3, 6,8 , 9, 0]
    x =  [1 , 2 , 3.5 , 4 , 5 , 6]
    print(l)
    return render_template('author_temp.html', author=l[0], papers=papers, confs=confs, x=x, y=y)
