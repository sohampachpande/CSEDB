from flask import render_template, request, redirect, session
from flask_paginate import Pagination, get_page_parameter
import networkx as nx
import plotly
import plotly.graph_objs as go
import json


from app import app
from app import db

fos_list = [['All', 'All'],['F-0', 'Error Correction and Code-Switching'], ['F-1', 'Word Segmentation'], ['F-2', 'Natural Language Processing'], ['F-3', 'Computational Linguitics on Twitter'], ['F-4', 'Dialogue and Discourse'], ['F-5', 'Sentiment Analysis'], ['F-6', 'Speech Recognition'], ['F-7', 'Information Extraction'], ['F-8', 'Word-Sense Disambiguation'], ['F-9', 'Lexical Acquisition'], ['F-10', 'Machine Translation'], ['F-11', 'Semantic Similarity'], ['F-12', 'Dependency Parsing'], ['F-13', 'Language Annotation'], ['F-14', 'Multilingual NLP']]
fos_dict = {'All': 'All', 'Error Correction and Code-Switching': 'F-0', 'Word Segmentation': 'F-1', 'Natural Language Processing': 'F-2', 'Computational Linguitics on Twitter': 'F-3', 'Dialogue and Discourse': 'F-4', 'Sentiment Analysis': 'F-5', 'Speech Recognition': 'F-6', 'Information Extraction': 'F-7', 'Word-Sense Disambiguation': 'F-8', 'Lexical Acquisition': 'F-9', 'Machine Translation': 'F-10', 'Semantic Similarity': 'F-11', 'Dependency Parsing': 'F-12', 'Language Annotation': 'F-13', 'Multilingual NLP': 'F-14'}

def citation_graph(papers, references, cited_by):
    G = nx.DiGraph()
    # print("Inside graph func \n\n\n\n\n papers",papers,"\n references:", references,"\nCitations:", cited_by,"\n\n\n\n\n")
    for i in references:
        G.add_edge(i[1], papers[0][1])

    for i in cited_by:
        G.add_edge(papers[0][1], i[1])

    pos=nx.spring_layout(G,dim=2,k=None)

    for i in pos:
        pos[i] = pos[i].tolist()

    dmin=1
    ncenter=0
    for n in pos:
        x,y=pos[n]
        d=(x-0.5)**2+(y-0.5)**2
        if d<dmin:
            ncenter=n
            dmin=d

    edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5,color='#888'),
    hoverinfo='none',
    mode='lines')

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            # showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))

    for node in G.nodes():
        x, y = pos[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color']+=tuple([len(adjacencies[1])])
        node_info = str(adjacencies[0])
        node_trace['text']+=tuple([node_info])

    data=[edge_trace, node_trace]

    # fig = go.Figure(data=[edge_trace, node_trace],
    #          layout=go.Layout(
    #             title='<br>Network graph made with Python',
    #             titlefont=dict(size=16),
    #             showlegend=False,
    #             hovermode='closest',
    #             margin=dict(b=20,l=5,r=5,t=40),
    #             annotations=[ dict(
    #                 text="Python code: <a href='https://plot.ly/ipython-notebooks/network-graphs/'> https://plot.ly/ipython-notebooks/network-graphs/</a>",
    #                 showarrow=False,
    #                 xref="paper", yref="paper",
    #                 x=0.005, y=-0.002 ) ],
    #             xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    #             yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

    return json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

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

    if selectFOS == 'All':
        if sort_convention == 'Citation Count':
            cursor.execute('CALL sort_papers_by_citations()')
            all_paper = cursor.fetchall()
        else:
            # execute SQL query using execute() method.
            cursor.execute('SELECT * FROM PaperTable ')
            all_paper = cursor.fetchall()
    else:
        if sort_convention == 'Citation Count':
            cursor.execute('CALL FOS_Paper_sorted_by_citations("{}")'.format(fos_dict[selectFOS]))
            all_paper = cursor.fetchall()
        else:
            cursor.execute('CALL FOS_paper("{}")'.format(fos_dict[selectFOS]))
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
                           fos_list = fos_list,
                           fos_id = fos_dict[selectFOS],
                           sort_id = sort_convention
                           )

# Individual paper page
@app.route('/paper/<paper_id>', methods = ['GET'])
def individual_paper_page(paper_id):
    #must return author individual page
    cursor = db.cursor()
    # execute SQL query using execute() method.
    cursor.execute('SELECT * FROM PaperTable WHERE  PaperID = "{}"'.format(paper_id))
    papers = cursor.fetchall()


    cursor.execute('call  con_paper("{}")'.format(paper_id))
    confs = cursor.fetchall()
    # print(confs)

    cursor.execute('call author_paper("{}")'.format(paper_id))
    authors = cursor.fetchall()
   
    cursor.execute('call references_of_this_paper("{}")'.format(paper_id))
    references = cursor.fetchall()

    cursor.execute('call this_paper_cited_by("{}")'.format(paper_id))
    papers_cite_this = cursor.fetchall()

    cursor.execute('CALL paper_citations_notCumul_yearwise("{}")'.format(paper_id))
    year_paper  = cursor.fetchall()

    cursor.execute('CALL summary_of_paper("{}")'.format(paper_id))
    summary  = cursor.fetchall()

    cursor.execute('CALL paper_keywords("{}")'.format(paper_id))
    keywords = cursor.fetchall()

    cursor.execute('CALL paper_fos("{}")'.format(paper_id))
    foss = cursor.fetchall()

    cursor.execute('CALL total_citation_count_paper("{}")'.format(paper_id))
    citation = cursor.fetchall()


    y = []
    x =  []
    for year,c in year_paper:
        x.append(year)
        y.append(c)
    # print(x,y)

    graph_json = citation_graph(papers, references, papers_cite_this)

    return render_template(
    'paper_temp.html',
    paper=papers[0],
    conferences=confs,
    authors=authors,
    references=references,
    papers_cite_this=papers_cite_this,
    x=x,
    y=y,
    summary=summary,
    keywords=keywords,
    foss=foss,
    citation_count=citation[0][0],
    graph=graph_json)
