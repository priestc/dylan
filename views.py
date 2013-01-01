import json
from giotto.views import BasicView

def album2json(result):
    """
    Convert the album instance into a json object. Include the list of
    songs as well. Songs do not include the ID.
    """
    new_songs = []
    for song in [x.todict() for x in result['album'].songs]:
        del song['id']
        new_songs.append(song)
    album = result['album'].todict()
    album['songs'] = new_songs
    return BasicView().generic_json(album, None)