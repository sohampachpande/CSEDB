from flask import render_template, request, redirect, url_for, session
from flask_paginate import Pagination, get_page_parameter
from app import app

from app import db


def all_paper_pagination(all_paper, offset, per_page):
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



@app.route('/search', methods = ['GET', 'POST'])
def search():
    cursor = db.cursor()

    q_author = request.form.get("Author")
    q_paper = request.form.get("Paper")
    q_conference = request.form.get("Conference")

    if q_author:
        session["AuthorName"] = q_author
        print("Inside Author", session["AuthorName"])
    else: 
        try:
            if session["AuthorName"]:
                print("inside try of Author", session["AuthorName"], type(session["AuthorName"]))
                q_author = session["AuthorName"]
        except KeyError:
            pass


    if q_paper:
        session["PaperName"] = q_paper
        print("Inside Paper", session["PaperName"])
    else: 
        try:
            if session["PaperName"]:
                print("inside try of paper", session["PaperName"], type(session["PaperName"]))
                q_paper = session["PaperName"]
                print("2 inside try of paper 2", q_paper, type(q_paper))
        except KeyError:
            pass


    if q_conference:
        session["ConferenceName"] = q_conference
    else: 
        try:
            if session["ConferenceName"]:
                q_conference = session["ConferenceName"]
        except KeyError:
            pass    

    if q_author:
        print("hi author", q_author)
        cursor.execute('CALL autname_nlq("{}")'.format(q_author))
        all_authors = cursor.fetchall()


        # selectFOS = 'All'
        # sort_convention = 'random'

        # if 'selectFOS' in request.args:
        #     selectFOS = request.args.get("selectFOS", type=str, default="All")
        #     session['selectFOS'] = selectFOS

        # else:
        #     if 'selectFOS' in session:
        #         selectFOS = session['selectFOS']
        #     else:
        #         session['selectFOS'] = selectFOS
            
        # if 'sort' in request.args:
        #     sort_convention = request.args.get("sort", type=str, default="random")
        #     session['sort_convention'] = sort_convention
            
        # else:
        #     if 'sort_convention' in session:
        #         sort_convention = session['sort_convention'] 
        #     else:
        #         session['sort_convention'] = sort_convention

        # print("\n\n", selectFOS=='All', sort_convention,"\n\n")
        # if selectFOS == 'All':
        #     if sort_convention == 'Citation Count':
        #         cursor.execute('CALL sort_authors_by_citations()')
        #         all_authors = cursor.fetchall()
        #     elif sort_convention == 'A-Z':
        #         cursor.execute('CALL sort_authors_alphabetically()')
        #         all_authors = cursor.fetchall()
        #     elif sort_convention == 'Paper Count':
        #         cursor.execute('CALL sort_authors_by_paper_count()')
        #         all_authors = cursor.fetchall()
        #     else:
        #         cursor.execute('SELECT * FROM AuthorTable')
        #         all_authors = cursor.fetchall()
        # else:
        #     if sort_convention == 'Citation Count':
        #         cursor.execute('CALL FOS_Author_sorted_by_citations("{}")'.format(fos_dict[selectFOS]))
        #         all_authors = cursor.fetchall()
        #     elif sort_convention == 'A-Z':
        #         cursor.execute('CALL FOS_Author_sorted_alphabetically("{}")'.format(fos_dict[selectFOS]))
        #         all_authors = cursor.fetchall()
        #     elif sort_convention == 'Paper Count':
        #         cursor.execute('CALL FOS_Author_sorted_by_paper_count("{}")'.format(fos_dict[selectFOS]))
        #         all_authors = cursor.fetchall()
        #     else:
        #         cursor.execute('CALL FOS_Author_sorted_alphabetically("{}")'.format(fos_dict[selectFOS]))
        #         all_authors = cursor.fetchall()
        
        cursor.close()

        total = len(all_authors)
        # page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
        page = request.args.get(get_page_parameter(), type=int, default=1)
        
        pagination_data = all_author_pagination(all_authors, offset=page, per_page=20)
        pagination = Pagination(page=page, total=total, css_framework='bootstrap4',display_msg='''Showing <b>{start} - {end}</b> {record_name} from <b>{total}</b> entries''')

        return render_template('result_author.html', data_authors=pagination_data,
                               page=page,
                               pagination=pagination,
                               query = q_author
                               )
        
    elif q_paper:
        print("hi paper", q_paper)
        cursor.execute('CALL papername_nlq("{}")'.format(q_paper))
        all_paper = cursor.fetchall()
        
        # sort_convention = request.args.get("sort", type=str, default="random")

        # if sort_convention == 'Citation Count':
        #     cursor.execute('CALL sort_papers_by_citations()')
        #     all_paper = cursor.fetchall()
        # else:
        #     # execute SQL query using execute() method.
        #     cursor.execute('SELECT * FROM PaperTable ')
        #     all_paper = cursor.fetchall()

        # cursor.close()

        total = len(all_paper)
        # page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
        page = request.args.get(get_page_parameter(), type=int, default=1)
        
        pagination_data = all_paper_pagination(all_paper, offset=page, per_page=20)
        pagination = Pagination(page=page, total=total, css_framework='bootstrap4',display_msg='''Showing <b>{start} - {end}</b> {record_name} from <b>{total}</b> entries''')

        return render_template('result_paper.html', data_papers=pagination_data,
                               page=page,
                               pagination=pagination,
                               query = q_paper
                               )

    elif len(q_conference)>0:
        print("hi conf", q_conference)
        cursor.execute('CALL conferencename_nlq("{}")'.format(q_conference))
        conf_list = cursor.fetchall()

        confs = list()
        d = dict()
        for i in conf_list:
            try:
                d[i[1]].append((int(i[2]), i[0]))
            except:
                d[i[1]] = [(int(i[2]), i[0])]
        for i in list(d.keys()):
            confs.append((i, sorted(d[i], key=lambda x: x[0])))

        return render_template('result_conference.html', 
                                pages = confs,
                                query = q_conference)

    else:
        return redirect(url_for('index'))


    cursor.close()
    # print("\n\n\n",return_list,"\n\n\n")
    return "Hi"
