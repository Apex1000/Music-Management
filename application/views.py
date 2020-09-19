from flask import render_template,request,redirect
from werkzeug.utils import secure_filename
from application import app
import os
import uuid
from .models import db, Songs
SONGS_DIR = 'application/static/songs'
app.config['SONGS_DIR'] = SONGS_DIR

@app.route('/')
def index():
    return render_template('public/main/index.html',
                            title="Flask Application")

@app.route('/playlist')
def playlist():
    return render_template('public/main/playlist.html',
                            title="Flask Application")

@app.route('/',methods=['POST'])
def upload():
    uid = uuid.uuid4().hex
    title = request.form['title']
    artist = request.form['artist']
    album = request.form['album']
    song = request.files['file']

    filename = secure_filename(song.filename)
    safefilename = secure_filename(str(uid)+ '-' + song.filename)
    song.save(os.path.join(SONGS_DIR,safefilename))
    title = title.strip()
    slug = title.replace(" ","-")
    
    new_song = Songs(id=uid,title=title,artist=artist,album=album,filename=safefilename,slug=slug)
    db.session.add(new_song)
    db.session.commit()

    return redirect('playlist')