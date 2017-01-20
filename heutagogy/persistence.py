from heutagogy import app
from flask_sqlalchemy import SQLAlchemy
import datetime
import pytz

db = SQLAlchemy(app)


# SQLite doesn't store timezones, so we convert all timestamps to UTC
# to not save incorrect info.
def to_utc(t):
    """Convert datetime to UTC."""
    if t is None:
        return t

    if t.tzinfo is None or t.tzinfo.utcoffset(t) is None:
        # t is naive datetime (not aware of timezone)
        return t.replace(tzinfo=pytz.utc)

    return t.astimezone(pytz.utc)


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    url = db.Column(db.String)
    title = db.Column(db.String)
    read = db.Column(db.DateTime)

    def __init__(self, user, url, title=None, timestamp=None, read=None):
        if timestamp is None:
            timestamp = datetime.datetime.utcnow()
        if title is None:
            title = url

        self.user = user
        self.url = url
        self.title = title
        self.timestamp = to_utc(timestamp)
        self.read = to_utc(read)

    def __repr__(self):
        return '<Bookmark %r of %r>' % self.url % self.user

    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'timestamp': self.timestamp.isoformat(),
            'read': self.read.isoformat() if self.read else None,
        }


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    db.create_all()
