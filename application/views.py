from flask import render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
from application import app
import os
import uuid
from .models import db, Songs

SONGS_DIR = 'application/static/songs'
app.config['SONGS_DIR'] = SONGS_DIR

@app.route('/')
def index():
    songs = Songs.query.all()
    return render_template('public/main/index.html',
                            songs=songs)

@app.route('/playlist')
def playlist():
    songs = Songs.query.all()
    return render_template('public/main/playlist.html',
                            songs=songs)

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

@app.route('/delete/<id>')
def delete(id):
    Songs.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('playlist'))

@app.route('/song/<id>')
def song(id):
    songs = Songs.query.all()
    song=Songs.query.filter_by(slug=id).first()
    print(song.filename)
    return render_template('public/main/play.html',
                            song=song,
                            songs=songs)