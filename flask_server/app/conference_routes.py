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

    return render_template('confsAll.html', pages = confs)


@app.route('/conference/<conf_id>', methods = ['GET'])
def get_conf_individual(conf_id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM ConferenceTable WHERE ConferenceID="{}"'.format(conf_id))
    conf_details = cursor.fetchall()

    cursor.execute('CALL conference_FieldOfStudy("{}")'.format(conf_id))
    fos = cursor.fetchall()

    cursor.execute('CALL conference_PaperNames("{}")'.format(conf_id))
    papers = cursor.fetchall()

    cursor.execute('CALL conference_AuthorNames("{}")'.format(conf_id))
    authors = cursor.fetchall()

    cursor.execute(' CALL ConferenceName_PaperDistribution("{}")'.format(conf_details[0][1]))
    conf_paper_count = cursor.fetchall()

    conf_paper_count_years = list()
    conf_paper_count_c = list()
    for i in conf_paper_count:
        conf_paper_count_c.append(i[1])
        conf_paper_count_years.append(i[0])

    cursor.execute(' CALL ConferenceName_CitationDistribution("{}")'.format(conf_details[0][1]))
    conf_cite_count = cursor.fetchall()

    conf_cite_count_years = list()
    conf_cite_count_c = list()

    for i in conf_cite_count:
        conf_cite_count_c.append(i[1])
        conf_cite_count_years.append(i[0])

    cursor.execute(' CALL conferenceName_PaperCount("{}")'.format(conf_details[0][1]))
    main_paper_count = cursor.fetchall()

    cursor.execute(' CALL conferenceName_AuthorCount("{}")'.format(conf_details[0][1]))
    main_author_count = cursor.fetchall()

    # print(main_paper_count)

    cursor.close()
    return render_template(
        'conf_temp.html',
        conf = conf_details[0],
        fos=fos,
        papers=papers,
        authors=authors,
        no_authors = len(authors),
        no_papers=len(papers),
        conf_paper_count_c = conf_paper_count_c,
        conf_paper_count_years = conf_paper_count_years,
        conf_cite_count_c = list(map(int, conf_cite_count_c)),
        conf_cite_count_years = conf_cite_count_years,
        conf_cite_count= conf_cite_count,
        main_paper_count= main_paper_count[0][0],
        main_author_count= main_author_count[0][0])
