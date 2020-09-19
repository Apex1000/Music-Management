from flask import render_template,request,redirect
from application import app

@app.route('/')
def index():
    return render_template('public/main/index.html',
                            title="Flask Application")

@app.route('/playlist')
def playlist():
    return render_template('public/main/playlist.html',
                            title="Flask Application")