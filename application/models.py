from . import db

class Songs(db.Model):
    __tablename__ = 'todos'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    title = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    artist = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    album = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    slug = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    slug = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    
    def __repr__(self):
        return '<Todo {}>'.format(self.todo)