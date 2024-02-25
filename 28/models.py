"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Playlist(db.Model):
    """Playlist."""
    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.Text, nullable=False)
    description=db.Column(db.Text, nullable=False)
    songs = relationship('Song', secondary='playlists_songs', backref='playlists')


class Song(db.Model):
    """Song."""

    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    title =db.Column(db.Text, nullable=False)
    artist=db.Column(db.Text, nullable=False)


class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""

    __tablename__ = "playlists_songs"

    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'), primary_key=True)


# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


