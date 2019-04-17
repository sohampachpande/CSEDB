from flask import render_template, request, redirect
from flask_paginate import Pagination, get_page_parameter

from app import app

from app import db

fos_list = [['F-0', 'Error Correction and Code-Switching'], ['F-1', 'Word Segmentation'], ['F-2', 'Natural Language Processing'], ['F-3', 'Computational Linguitics on Twitter'], ['F-4', 'Dialogue and Discourse'], ['F-5', 'Sentiment Analysis'], ['F-6', 'Speech Recognition'], ['F-7', 'Information Extraction'], ['F-8', 'Word-Sense Disambiguation'], ['F-9', 'Lexical Acquisition'], ['F-10', 'Machine Translation'], ['F-11', 'Semantic Similarity'], ['F-12', 'Dependency Parsing'], ['F-13', 'Language Annotation'], ['F-14', 'Multilingual NLP']]


def all_paper_pagination(all_data, offset, per_page):
    return all_data[offset:offset+per_page]


@app.route('/fos_all', methods = ['GET'])
def get_fos_authors():
    
    return render_template('fos_all.html', fos_list = fos_list)

@app.route('/fos/<fos_id>', methods = ['GET'])
def get_fos_papers(fos_id):
    cursor = db.cursor()
    # execute SQL query using execute() method.
    # Fetch a single row using fetchone()
    # data = cursor.fetchone()
    cursor.execute('call FOS_paper("{}")'.format(fos_id))
    papers = cursor.fetchall()

    cursor.execute('call FOS_aut("{}")'.format(fos_id))
    authors = cursor.fetchall()

    cursor.execute('call fos_conf("{}")'.format(fos_id))
    conferences = cursor.fetchall()

    total_papers = len(papers)
    total_authors = len(authors)
    # page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    
    pagination_paper = all_paper_pagination(papers, offset=page, per_page=20)
    paginationpaper = Pagination(page=page, total=total_papers, css_framework='bootstrap4',display_msg='''Showing <b>{start} - {end}</b> {record_name} from <b>{total}</b> entries''')

    pagination_author = all_paper_pagination(authors, offset=page, per_page=20)
    paginationauthor = Pagination(page=page, total=total_authors, css_framework='bootstrap4',display_msg='''Showing <b>{start} - {end}</b> {record_name} from <b>{total}</b> entries''')

    return render_template('fos_temp.html', fos_list = fos_list,  papers = papers, authors = authors, conferences = conferences, fos_id = fos_id,page=page, pagination_author=pagination_author,pagination_paper= pagination_paper)