import datetime
import re

from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError
from giotto import config
from giotto.primitives import ALL_DATA
from giotto.exceptions import DataNotFound, InvalidInput
from giotto.utils import slugify

from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import relationship

class Album(config.Base):
    id = Column(Integer, primary_key=True)
    title = Column(String)
    date = Column(Date)
    date_added = Column(DateTime)
    venue = Column(String)
    venue_slug = Column(String)
    city = Column(String)
    city_slug = Column(String)
    source = Column(String)
    bucket = Column(String)
    folder = Column(String)
    encoding = Column(String)
    songs = relationship('Song', backref="album")

    def __repr__(self):
        return "<Album: %s - %s>" % (self.title, self.date)

    def __init__(self, *a, **k):
        super(Album, self).__init__(*a, **k)
        self.city_slug = slugify(self.city)
        self.venue_slug = slugify(self.venue)
        if not self.date_added:
            self.date_added = datetime.datetime.now()

    @classmethod
    def by_city(cls, city_slug):
        albums = config.session.query(cls).filter_by(city_slug=city_slug).all()
        if not albums:
            raise DataNotFound
        city = albums[0].city
        return {'albums': albums, 'length': len(albums), 'city': city}

    @classmethod
    def by_venue(cls, venue_slug):
        albums = config.session.query(cls).filter_by(venue_slug=venue_slug).all()
        if not albums:
            raise DataNotFound
        venue = albums[0].venue
        return {'albums': albums, 'length': len(albums), 'venue': venue}

    @classmethod
    def newest(cls):
        albums = config.session.query(cls).order_by(cls.date_added)
        return {'albums': albums[:10]}

    @classmethod
    def all_cities(cls):
        cities = config.session.query(func.max(cls.city), cls.city_slug, func.count(cls.title)).group_by(cls.city_slug).all()
        return {'cities': cities, 'length': len(cities)}

    @classmethod
    def all_venues(cls):
        venues = config.session.query(func.max(cls.venue), cls.venue_slug, func.count(cls.title)).group_by(cls.venue_slug).all()
        return {'venues': venues, 'length': len(venues)}

    @classmethod
    def all(cls):
        return {'albums': config.session.query(cls).all()}

    @classmethod
    def get(cls, id):
        album = config.session.query(cls).filter_by(id=id).first()
        if not album:
            raise DataNotFound()
        return {'album': album}

    @classmethod
    def create(cls, data=ALL_DATA):
        try:
            if '-' in data['date']:
                y, m, d = data['date'].split('-')
            else:
                y = data['date']
                m, d = 1, 1
        except:
            raise InvalidInput("invalid date")

        a = cls(
            title=data['title'],
            date=datetime.date(year=int(y), month=int(m), day=int(d)),
            venue=data['venue'],
            bucket=data['bucket'],
            folder=data['folder'],
            city=data['city'],    
        )
        config.session.add(a)
        for i in xrange(int(data['num_of_tracks']) + 1):
            title = data['title_%s' % i]
            track = data['track_%s' % i]
            s3_name = data['s3_%s' % i]
            dur = data['duration_%s' % i]
            s = Song(title=title, track=track, s3_name=s3_name, album=a, duration=dur)
            config.session.add(s)

        config.session.commit()
        return a

    def playlist_urls_js(self):
        ret = [str(x.url()) for x in self.songs]
        return [''] + ret
    def run_time_in_seconds(self):
        return sum(x.duration_in_seconds() for x in self.songs)

    def duration(self):
        dur = self.run_time_in_seconds()
        m = dur / 60
        s = dur % 60
        return "%d:%2d" % (m, s)

class Song(config.Base):
    id = Column(Integer, primary_key=True)
    title = Column(String)
    slug = Column(String)
    track = Column(Integer)
    duration = Column(String)
    album_id = Column(Integer, ForeignKey('giotto_album.id'))
    s3_name = Column(String)

    @classmethod
    def all_songs(cls):
        songs = config.session.query(
            func.max(cls.title), cls.slug, func.count(cls.title)
            ).group_by(cls.slug).order_by(cls.slug).all()
        return {'songs': songs, 'length': len(songs)}

    @classmethod
    def profile(cls, slug):
        songs = config.session.query(cls).join(Album).filter(cls.slug==slug).order_by(Album.date).all()
        if not songs:
            raise DataNotFound
        title = songs[0].title
        return {'songs': songs, 'title': title, 'length': len(songs)}

    def __init__(self, *a, **k):
        super(Song, self).__init__(*a, **k)
        self.slug = slugify(self.title)
        if not re.match(r'^\d+:\d{2}$', self.duration):
            raise InvalidInput("invalid duration")
        if type(self.track) != int and not self.track.isdigit():
            raise InvalidInput("invalid track")

    def duration_in_seconds(self):
        m, s = self.duration.split(':')
        return (int(m) * 60) + int(s)

    def __repr__(self):
        return "<Song: %02d - %s>" %(self.track, self.title)

    def url(self):
        return "https://s3.amazonaws.com/%s/%s/%s" % (self.album.bucket, self.album.folder, self.s3_name) 


def get_bucket_contents(bucket, folder):
    conn = S3Connection(config.aws_access_key, config.aws_secret_access_key)
    try:
        bucket = conn.get_bucket(bucket)
    except S3ResponseError:
        raise DataNotFound("Can't open S3 bucket")

    length = len(folder)
    # skip the first result (which is just the folder name, and remove the
    # folder name from each result
    ret = [x.name[length+1:] for x in bucket.list(folder)]
    if len(ret) == 0:
        raise DataNotFound("Empty Bucket or folder")
    return ret


def from_json(file):
    import json
    import dateutil.parser
    j = open(file).read()
    obj = json.loads(j)
    songs = obj['songs']
    del obj['songs']
    obj['date_added'] = dateutil.parser.parse(obj['date_added'])
    obj['date'] = dateutil.parser.parse(obj['date'])
    a = Album(**obj)
    config.session.add(a)

    for song_data in songs:
        s = Song(**song_data)
        config.session.add(s)
    
    config.session.commit()