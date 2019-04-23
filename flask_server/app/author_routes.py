from flask import render_template, request, redirect, session
from flask_paginate import Pagination, get_page_parameter
from app import app

from app import db

# session['selectFOS'] = 'All'
# session['sort_convention'] = 'random' 

fos_list = [['All', 'All'],['F-0', 'Error Correction and Code-Switching'], ['F-1', 'Word Segmentation'], ['F-2', 'Natural Language Processing'], ['F-3', 'Computational Linguitics on Twitter'], ['F-4', 'Dialogue and Discourse'], ['F-5', 'Sentiment Analysis'], ['F-6', 'Speech Recognition'], ['F-7', 'Information Extraction'], ['F-8', 'Word-Sense Disambiguation'], ['F-9', 'Lexical Acquisition'], ['F-10', 'Machine Translation'], ['F-11', 'Semantic Similarity'], ['F-12', 'Dependency Parsing'], ['F-13', 'Language Annotation'], ['F-14', 'Multilingual NLP']]
fos_dict = {'All': 'All', 'Error Correction and Code-Switching': 'F-0', 'Word Segmentation': 'F-1', 'Natural Language Processing': 'F-2', 'Computational Linguitics on Twitter': 'F-3', 'Dialogue and Discourse': 'F-4', 'Sentiment Analysis': 'F-5', 'Speech Recognition': 'F-6', 'Information Extraction': 'F-7', 'Word-Sense Disambiguation': 'F-8', 'Lexical Acquisition': 'F-9', 'Machine Translation': 'F-10', 'Semantic Similarity': 'F-11', 'Dependency Parsing': 'F-12', 'Language Annotation': 'F-13', 'Multilingual NLP': 'F-14'}


def all_author_pagination(all_authors,offset, per_page):
    auth_subset = all_authors[offset: offset + per_page]
    cursor = db.cursor()
    return_list = []
    for a in auth_subset:
        cursor.execute('CALL FOS("{}")'.format(a[0]))
        fos = cursor.fetchall()
        cursor.execute('CALL Number_of_papers_of_author("{}")'.format(a[0]))
        no_papers = cursor.fetchall()
        cursor.execute('CALL Number_of_citations_of_author("{}")'.format(a[0]))
        citations = cursor.fetchall()
        cursor.execute('CALL author_affiliation("{}")'.format(a[0]))
        affiliation = cursor.fetchall()
        if a[1][0]==',':
            pass
            # return_list.append([a[0], a[1][1:], fos, no_papers[0][0], citations[0][0], affiliation])
        else:
            return_list.append([a[0], a[1], fos, no_papers[0][0], citations[0][0], affiliation])
    return return_list


def get_paper_all_info(papers_list):
    cursor = db.cursor()
    return_list = []
    for a in papers_list:
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


@app.route('/author_all', methods = ['GET'])
def get_all_authors():

    # session.clear()
    cursor = db.cursor()

    selectFOS = 'All'
    sort_convention = 'random'

    if 'selectFOS' in request.args:
        selectFOS = request.args.get("selectFOS", type=str, default="All")
        session['selectFOS'] = selectFOS

    else:
        if 'selectFOS' in session:
            selectFOS = session['selectFOS']
        else:
            session['selectFOS'] = selectFOS
        
    if 'sort' in request.args:
        sort_convention = request.args.get("sort", type=str, default="random")
        session['sort_convention'] = sort_convention
        
    else:
        if 'sort_convention' in session:
            sort_convention = session['sort_convention'] 
        else:
            session['sort_convention'] = sort_convention

    print("\n\n", selectFOS=='All', sort_convention,"\n\n")
    if selectFOS == 'All':
        if sort_convention == 'Citation Count':
            cursor.execute('CALL sort_authors_by_citations()')
            all_authors = cursor.fetchall()
        elif sort_convention == 'A-Z':
            cursor.execute('CALL sort_authors_alphabetically()')
            all_authors = cursor.fetchall()
        elif sort_convention == 'Paper Count':
            cursor.execute('CALL sort_authors_by_paper_count()')
            all_authors = cursor.fetchall()
        else:
            cursor.execute('SELECT * FROM AuthorTable')
            all_authors = cursor.fetchall()
    else:
        if sort_convention == 'Citation Count':
            cursor.execute('CALL FOS_Author_sorted_by_citations("{}")'.format(fos_dict[selectFOS]))
            all_authors = cursor.fetchall()
        elif sort_convention == 'A-Z':
            cursor.execute('CALL FOS_Author_sorted_alphabetically("{}")'.format(fos_dict[selectFOS]))
            all_authors = cursor.fetchall()
        elif sort_convention == 'Paper Count':
            cursor.execute('CALL FOS_Author_sorted_by_paper_count("{}")'.format(fos_dict[selectFOS]))
            all_authors = cursor.fetchall()
        else:
            cursor.execute('CALL FOS_Author_sorted_alphabetically("{}")'.format(fos_dict[selectFOS]))
            all_authors = cursor.fetchall()
    
    cursor.close()

    total = len(all_authors)
    # page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
    page = request.args.get(get_page_parameter(), type=int, default=1)
    
    pagination_data = all_author_pagination(all_authors, offset=page, per_page=20)
    pagination = Pagination(page=page, total=total, css_framework='bootstrap4',display_msg='''Showing <b>{start} - {end}</b> {record_name} from <b>{total}</b> entries''')

    return render_template('authorsAll.html', data_authors=pagination_data,
                           page=page,
                           pagination=pagination,
                           fos_list = fos_list,
                           fos_id = fos_dict[selectFOS],
                           sort_id = sort_convention
                           )


@app.route('/author/<author_id>', methods = ['GET'])
def get_author_page(author_id):
    #must return author individual page
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('SELECT * FROM AuthorTable WHERE  AuthorID = "{}"'.format(author_id))
    l = cursor.fetchall()

    cursor.execute('call Number_of_citations_of_author("{}")'.format(author_id))
    a_count_citations = cursor.fetchall()

    cursor.execute('call FOS("{}")'.format(author_id))
    a_field = cursor.fetchall()

    cursor.execute('call aut_conf("{}")'.format(author_id))
    a_conf = cursor.fetchall()

    cursor.execute('call aut_paper("{}")'.format(author_id))
    papers_list = cursor.fetchall()

    a_papers = get_paper_all_info(papers_list)

    cursor.execute('call coauthor("{}")'.format(author_id))
    a_coauth = cursor.fetchall()


    cursor.execute(' CALL  Author_PaperDistribution("{}")'.format(author_id))
    author_paper_count = cursor.fetchall()

    author_paper_count_years = list()
    author_paper_count_c = list()
    for i in author_paper_count:
        author_paper_count_c.append(i[1])
        author_paper_count_years.append(i[0])


    cursor.execute(' CALL Author_CitationDistribution("{}")'.format(author_id))
    author_cite_count = cursor.fetchall()


    author_cite_count_years = list()
    author_cite_count_c = list()

    for i in author_cite_count:
        author_cite_count_c.append(i[1])
        author_cite_count_years.append(i[0])

    confs = list()
    d = dict()
    for i in a_conf:
        try:
            d[i[1]].append((int(i[2]), i[0]))
        except:
            d[i[1]] = [(int(i[2]), i[0])]
    for i in list(d.keys()):
        confs.append((i, sorted(d[i], key=lambda x: x[0])))


    cursor.close()
    return render_template('author_temp.html',
        author=l[0],
        auth_field=a_field,
        auth_conference=confs,
        auth_papers=a_papers,
        auth_coauth = a_coauth,
        author_paper_count_c = author_paper_count_c,
        author_paper_count_years = author_paper_count_years,
        author_cite_count_c = author_cite_count_c,
        author_cite_count_years = author_cite_count_years,
        author_total_citations = a_count_citations)


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
