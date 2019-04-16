from flask import Flask

import pymysql as PyMySQL
import pymysql.cursors

app = Flask(__name__)

# Connect to the database
db = PyMySQL.connect("10.0.25.35","sohamp","s27498","CSResearchPapers" )

from app import routes, author_routes, paper_routes