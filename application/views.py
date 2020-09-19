from flask import render_template,request,redirect
from application import app

@app.route('/')
def index():
    print(app.config)
    return render_template('public/main/index.html',
                            title="Flask Application")