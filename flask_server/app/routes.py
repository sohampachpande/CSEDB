from flask import render_template, request, redirect, session, flash
from app import app
import re
from app import db

def FirstNameLastName(name):
    l_n = name.split(",")
    return l_n[-1]+', '+ l_n[0]

# # Connect to the database
# db = PyMySQL.connect("10.0.25.35","sohamp","s27498","CSResearchPapers" )

@app.route('/index')
@app.route('/home')
def index():
    user = {'username': 'Soham'}
    session.clear()
    # Todo : Make search
    
    return render_template('index.html', title='CSE DB', user=user)


@app.route('/add')
def cite_net():
    user = {'username': 'Soham'}

    fos_list = [['F-0', 'Error Correction and Code-Switching'], ['F-1', 'Word Segmentation'], ['F-2', 'Natural Language Processing'], ['F-3', 'Computational Linguitics on Twitter'], ['F-4', 'Dialogue and Discourse'], ['F-5', 'Sentiment Analysis'], ['F-6', 'Speech Recognition'], ['F-7', 'Information Extraction'], ['F-8', 'Word-Sense Disambiguation'], ['F-9', 'Lexical Acquisition'], ['F-10', 'Machine Translation'], ['F-11', 'Semantic Similarity'], ['F-12', 'Dependency Parsing'], ['F-13', 'Language Annotation'], ['F-14', 'Multilingual NLP']]

    return render_template('mods.html', title='CSE DB', user=user, fos_list = fos_list)


@app.route('/submit', methods = ['POST'])
def submit():
    cursor = db.cursor()
    fos_list = [['F-0', 'Error Correction and Code-Switching'], ['F-1', 'Word Segmentation'], ['F-2', 'Natural Language Processing'], ['F-3', 'Computational Linguitics on Twitter'], ['F-4', 'Dialogue and Discourse'], ['F-5', 'Sentiment Analysis'], ['F-6', 'Speech Recognition'], ['F-7', 'Information Extraction'], ['F-8', 'Word-Sense Disambiguation'], ['F-9', 'Lexical Acquisition'], ['F-10', 'Machine Translation'], ['F-11', 'Semantic Similarity'], ['F-12', 'Dependency Parsing'], ['F-13', 'Language Annotation'], ['F-14', 'Multilingual NLP']]

    paper = request.form.get("paper")
    keywords = request.form.get("keywords")
    authors = request.form.get("authors").split(",")
    conference = request.form.get("conferences").split(",")
    references = request.form.get("references").split(",")
    affiliations = request.form.get("affiliations").split(",")
    places = request.form.get("places").split(",")
    keywords_list = keywords.split(",")
    year = request.form.get("year").split(",")
    summary = request.form.get("summary")

    fos = list()
    for f in fos_list:
        if request.form.get(f[1]):
            fos.append(f[1])
    


    author = authors
    for i,w in enumerate(author):
        author[i] = w.strip().split(' ')[1:]+[w.strip().split(' ')[0]]
        author[i] = ', '.join(author[i])
    
    # fos - [,]
    # fos = fos.split(',')
    # fos = [i.split() for i in fos]
    
    # title - 
    title = paper
    
    # conf [[conf, year]]
    new_conf = [[conf.strip(), year[i].strip()] for i,conf in enumerate(conference)]
    
    # aff - [[author,aff]]
    aff = affiliations
    place = places
    
    new = []
    for i,w in enumerate(aff):
        new.append([author[i], w.strip(), place[i].strip()])
        
    # ref - []
    ref = references
    ref = [i.split() for i in ref]
    
    
    
    ###############################
    cursor.execute('call check_paper_exists_and_add("{}")'.format(title))
    check_paper = cursor.fetchall()
    
    
    try:
        cursor.execute('call check_paper_exists_and_add("{}")'.format(title))
        check_paper = cursor.fetchall()
        
        if check_paper[0][0][0] =='Z':
            for i in new:
                cursor.execute('call addAuthor_Affiliation("{}","{}","{}","{}")'.format(check_paper[0][0], i[0], i[1], i[2]))
                
            for i in new_conf:
                cursor.execute('call addConference("{}","{}","{}")'.format(check_paper[0][0], i[0], int(i[1])))
                
            for i in fos:
                cursor.execute('call addFieldOfStudy("{}","{}")'.format(check_paper[0][0], i))
            
            for i in ref:
                cursor.execute('call addReferences("{}","{}")'.format(check_paper[0][0], i))
                
            for i in keywords_list:
                print(i, )
                cursor.execute('call addKeywords("{}","{}")'.format(check_paper[0][0], i))
            
            cursor.execute('call addSummary("{}","{}")'.format(check_paper[0][0], summary))
            db.commit()
            cursor.close()
            return("Submitted Successfully")
    except:
        cursor.close()
        return("Failed")
    




def nlq(query):
    re1 = re.compile('is (.*) accpeting papers from (\w+)')
    re2 = re.compile('has (.*) published any papers')
    re3 = re.compile('does (.*) published papers on (.*)')
    re4 = re.compile('has (.*) and (.*) published together')
    re5 = re.compile('how many papers are published by (.*)')
    re6 = re.compile('how many citations does (.*) have')
    
    if re1.findall(query) != []:
        flg = 1
        return re1.findall(query), flg
    
    elif re2.findall(query) != []:
        flg = 2
        return re2.findall(query), flg
    
    elif re3.findall(query) != []:
        flg = 3
        return re3.findall(query), flg
    
    elif re4.findall(query) != []:
        flg = 4
        return re4.findall(query), flg
    
    elif re5.findall(query) != []:
        flg = 5
        return re5.findall(query), flg
    
    elif re6.findall(query) != []:
        flg = 6
        return re6.findall(query), flg
    else:
        flg = 0
        return None, flg

def nlq_answer(query):
    result, flg = nlq(query)

    cursor = db.cursor()
    
    if flg == 1:
        cursor.execute('CALL conferencename_nlq("{}")'.format(result[0]))
        conf_id = cursor.fetchall()
        
        if conf_id == []:
            pass
        
        else:
            for i,w in enumerate(conf_id):
                cursor.execute('CALL conference_FieldOfStudy("{}")'.format(w[0]))
                fos = cursor.fetchall()

                for i in fos:
                    if i[1].lower() == result[1]:
                        return 'Yes'
        return 'No'

    elif flg == 2:
        cursor.execute('CALL autname_nlq("{}")'.format(result[0]))
        try:
            auth_id = cursor.fetchall()[0][0]
            
            cursor.execute('CALL Number_of_papers_of_author("{}")'.format(auth_id))
            answer = cursor.fetchall()
            try:
                if str(answer[0][0]) > 'a':
                    pass
                return 'Yes'

            except:
                pass
            
            return 'No'
        except:
            return 'No'    
        
    elif flg == 3:
        cursor.execute('CALL autname_nlq("{}")'.format(result[0]))
        try:
            auth_id = cursor.fetchall()[0][0]
            
            cursor.execute('CALL FOS("{}")'.format(auth_id[0][0]))
            field = cursor.fetchall()
            
            if field == []:
                pass
            elif field[0][0] == result[1]:
                return 'Yes'
            
            return 'No'
        except:
            return 'No'

    elif flg == 4:
        cursor.execute('CALL autname_nlq("{}")'.format(result[0]))
        try:
            auth_id = cursor.fetchall()[0][0]
            
            cursor.execute('CALL coauthor("{}")'.format(auth_id))
            answer = cursor.fetchall()
            
            try:
                if answer[0][0] > 'a':
                    pass
                return 'Yes'
            except:
                pass
            
            return 'No'
        except:
            return 'No'

    elif flg == 5:
        cursor.execute('CALL autname_nlq("{}")'.format(result[0]))
        try:
            auth_id = cursor.fetchall()[0][0]
            
            cursor.execute('CALL Number_of_papers_of_author("{}")'.format(auth_id))
            answer = cursor.fetchall()
            return answer[0][0]
        except:
            return 'No such author'

    elif flg == 6:
        try:
            cursor.execute('CALL autname_nlq("{}")'.format(result[0]))
            auth_id = cursor.fetchall()[0][0]
            
            cursor.execute('CALL Number_of_citations_of_author("{}")'.format(auth_id))
            answer = cursor.fetchall()
            return answer[0][0]
        except:
            return 'No such author'
        
    else:
        return "Query Not Understood"


@app.route('/search_nlp', methods = ['POST'])
def nlp_query():
    query = request.form.get("nlp").lower()

    s = nlq_answer(query)
    return str(s)

