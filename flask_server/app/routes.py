from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Soham'}
    return render_template('index.html', title='CSE DB', user=user)
