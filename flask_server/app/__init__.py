from flask import Flask, session
import os

import pymysql as PyMySQL
import pymysql.cursors

from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = "96e16ccf34694cc691a8c284919ab2e7d3daafbdb9407c90"

# Connect to the database
# Enter Username and Password to database here 
db = PyMySQL.connect("localhost","sohamp","<password>","CSResearchPapers" )

# login module
login = LoginManager(app)

from app import routes, author_routes, paper_routes, conference_routes, fos_routes, search

