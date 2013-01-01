import json
from giotto.views import BasicView

def album2json(result):
    songs = [x.todict() for x in result['album'].songs]
    album = result['album'].todict()
    album['songs'] = songs
    return BasicView().generic_json(album, None)