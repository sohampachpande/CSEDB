from flask import Flask, session
import os

import pymysql as PyMySQL
import pymysql.cursors

app = Flask(__name__)

app.config['SECRET_KEY'] = "96e16ccf34694cc691a8c284919ab2e7d3daafbdb9407c90"

# Connect to the database
db = PyMySQL.connect("10.0.25.35","sohamp","s27498","CSResearchPapers" )

from app import routes, author_routes, paper_routes, conference_routes, fos_routes