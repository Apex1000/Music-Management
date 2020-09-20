from flask import render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
from application import app
import os
import uuid
from .models import db, Songs

SONGS_DIR = 'application/static/songs'
app.config['SONGS_DIR'] = SONGS_DIR

def jsonconvert(songs,album,artist):
    items=[]
    for i in songs:
        item={
            "html_url": "http://0.0.0.0:5000/song/"+i.slug,
            "name":i.title,
            "description":"Album: "+i.album+" | "+"Artist: "+i.artist
        }
        items.append(item)
    for i in album:
        item={
            "html_url": "http://0.0.0.0:5000/song/"+i.slug,
            "name":i.title,
            "description":"Album: "+i.album+" | "+"Artist: "+i.artist
        }
        items.append(item)
    for i in artist:
        item={
            "html_url": "http://0.0.0.0:5000/song/"+i.slug,
            "name":i.title,
            "description":"Album: "+i.album+" | "+"Artist: "+i.artist
        }
        items.append(item)
    datas = {
        "total_count":len(items),
        "items": items
    }
    return datas
@app.route('/')
def index():
    songs = Songs.query.all()
    return render_template('public/main/index.html',
                            songs=reversed(songs))

@app.route('/playlist')
def playlist():
    songs = Songs.query.all()
    return render_template('public/main/playlist.html',
                            songs=reversed(songs))

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
                            songs=reversed( songs))

@app.route('/songs')
def songs():
    songs = Songs.query.all()
    return render_template('public/main/songs.html',
                            songs=reversed(songs))

@app.route('/search')
def search():
    args = request.args['q']
    search = "%{}%".format(args)
    songs = Songs.query.filter(Songs.title.like(search)).all()
    album = Songs.query.filter(Songs.album.like(search)).all()
    artist = Songs.query.filter(Songs.artist.like(search)).all()
    # print(artist)
    data = jsonconvert(songs,album,artist)
    return data,200

@app.route('/find', methods=['POST','GET'])
def find():
    if request.method == 'POST':
        song = request.form['title']
        album = request.form['album']
        artist = request.form['artist']
        if song != "":
            songs = Songs.query.filter(Songs.title.like("%{}%".format(song))).all()
        else:
            songs = []
        if album != "":
            album = Songs.query.filter(Songs.album.like("%{}%".format(album))).all()
        else:
            album = []
        if artist != "":
            artist = Songs.query.filter(Songs.artist.like("%{}%".format(artist))).all()
        else:
            artist =[]

        return render_template('public/main/search.html',
                                songs=songs,
                                album=album,
                                artist=artist)
    else:
        return render_template('public/main/search.html')