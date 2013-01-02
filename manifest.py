from giotto import config
from giotto.programs import GiottoProgram, ProgramManifest, management_manifest
from giotto.views import BasicView, jinja_template
from giotto.contrib.static.programs import StaticServe
from giotto.control import Redirection

from models import Album, Song, get_bucket_contents, from_json
from views import album2json

manifest = ProgramManifest({
    '': GiottoProgram(
        view=BasicView(
            html=jinja_template('home.html'),
        ),
    ),
    'albums': GiottoProgram(
        model=[Album.all],
        view=BasicView(
            html=jinja_template('album_list.html'),
        ),
    ),
    'album': GiottoProgram(
        model=[Album.get],
        view=BasicView(
            html=jinja_template('album.html'),
            json=album2json,
        ),
    ),
    'song': GiottoProgram(
        model=[Song.profile],
        view=BasicView(
            html=jinja_template('song.html')
        ),
    ),
    'songs': GiottoProgram(
        model=[Song.all_songs],
        view=BasicView(
            html=jinja_template('all_songs.html'),
        ),
    ),
    'venue': GiottoProgram(
        model=[Album.by_venue],
        view=BasicView(
            html=jinja_template('venue.html'),
        )
    ),
    'venues': GiottoProgram(
        model=[Album.all_venues],
        view=BasicView(
            html=jinja_template('all_venues.html'),
        )
    ),
    'city': GiottoProgram(
        model=[Album.by_city],
        view=BasicView(
            html=jinja_template('city.html'),
        )
    ),
    'cities': GiottoProgram(
        model=[Album.all_cities],
        view=BasicView(
            html=jinja_template('all_cities.html'),
        )
    ),
    'bucket_contents': GiottoProgram(
        model=[get_bucket_contents, ['1.mp3', '2.mp3']],
        view=BasicView(),
    ),
    'newest': GiottoProgram(
        model=[Album.newest],
        view=BasicView(
            html=jinja_template('newest.html'),
        ),
    ),
    'new': [
        GiottoProgram(
            view=BasicView(
                html=jinja_template('album_form.html'),
            ),
        ),
        GiottoProgram(
            controllers=['http-post'],
            model=[Album.create],
            view=BasicView(
                html=lambda m: Redirection('album/%s' % m.id),
            ),
        ),
    ],
    'load_from_json': GiottoProgram(
        controllers=['cmd'],
        model=[from_json],
        view=BasicView(),
    ),
    'static': StaticServe(config.project_path + '/static/'),
    'mgt': management_manifest,
})