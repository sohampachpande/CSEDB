from flask import render_template, request, redirect
from flask_paginate import Pagination, get_page_parameter
from app import app

from app import db


def all_paper_pagination(all_paper,offset, per_page):
    paper_subset = all_paper[offset: offset + per_page]
    cursor = db.cursor()
    return_list = []
    for a in paper_subset:
        cursor.execute('CALL author_paper("{}")'.format(a[0]))
        authors = cursor.fetchall()

        cursor.execute('CALL con_paper("{}")'.format(a[0]))
        conf = cursor.fetchall()

        cursor.execute('CALL paper_fos("{}")'.format(a[0]))
        fos = cursor.fetchall()

        cursor.execute('CALL total_citation_count_paper("{}")'.format(a[0]))
        citation = cursor.fetchall()
        
        return_list.append([a[0], a[1], authors, conf, fos, citation[0][0]])
    return return_list



# All Papers page
@app.route('/papers_all', methods = ['GET'])
def get_all_papers():

    sort_convention = request.args.get("sort", type=str, default="random")

    cursor = db.cursor()

    if sort_convention == 'Citation Count':
        cursor.execute('CALL sort_papers_by_citations()')
        all_paper = cursor.fetchall()
    else:
        # execute SQL query using execute() method.
        cursor.execute('SELECT * FROM PaperTable ')
        all_paper = cursor.fetchall()

    cursor.close()

    total = len(all_paper)
    # page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    
    pagination_data = all_paper_pagination(all_paper, offset=page, per_page=20)
    pagination = Pagination(page=page, total=total, css_framework='bootstrap4',display_msg='''Showing <b>{start} - {end}</b> {record_name} from <b>{total}</b> entries''')

    return render_template('papersAll.html', data_papers=pagination_data,
                           page=page,
                           pagination=pagination,
                           )

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
   
    cursor.execute('call references_of_this_paper("{}")'.format(paper_id))
    references = cursor.fetchall()

    cursor.execute('call this_paper_cited_by("{}")'.format(paper_id))
    papers_cite_this = cursor.fetchall()

    print(papers_cite_this)
    print(authors)


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
