import datetime
from models import Song, Album

def mock_album():
    songs = [
        Song(title="You Ain't Goin' Nowhere", track=1, album_id=1, s3_name="Los Angeles 2012-10-26-00.ogg", duration="5:20"),
        Song(title="To Ramona", track=2, album_id=1, s3_name="Los Angeles 2012-10-26-02.ogg", duration="5:01"),
        Song(title="Things Have Changed", track=3, album_id=1, s3_name="Los Angeles 2012-10-26-02.ogg", duration="5:20"),
        Song(title="Tangled Up In Blue", track=4, album_id=1, s3_name="Los Angeles 2012-10-26-03.ogg", duration="6:26"),
        Song(title="The Levee's Gonna Break", track=5, album_id=1, s3_name="Los Angeles 2012-10-26-04.ogg", duration="7:14"),
        Song(title="Make You Feel My Love", track=6, album_id=1, s3_name="Los Angeles 2012-10-26-05.ogg", duration="5:00"),
        Song(title="Cry A While", track=7, album_id=1, s3_name="Los Angeles 2012-10-26-06.ogg", duration="5:42"),
        Song(title="Desolation Row", track=8, album_id=1, s3_name="Los Angeles 2012-10-26-07.ogg", duration="9:08"),
        Song(title="Highway 61 Revisitied", track=9, album_id=1, s3_name="Los Angeles 2012-10-26-08.ogg", duration="7:00"),
        Song(title="Love Sick", track=10, album_id=1, s3_name="Los Angeles 2012-10-26-09.ogg", duration="5:32"),
        Song(title="Thunder on the Mountain", track=11, album_id=1, s3_name="Los Angeles 2012-10-26-10.ogg", duration="7:51"),
        Song(title="Ballad of A Thin Man", track=12, album_id=1, s3_name="Los Angeles 2012-10-26-11.ogg", duration="6:17"),
        Song(title="Like A Rolling Stone", track=13, album_id=1, s3_name="Los Angeles 2012-10-26-12.ogg", duration="6:32"),
        Song(title="All Along the Watchtower", track=14, album_id=1, s3_name="Los Angeles 2012-10-26-13.ogg", duration="6:18"),
        Song(title="Blowin' In the Wind", track=15, album_id=1, s3_name="Los Angeles 2012-10-26-14.ogg", duration="9:02"),
    ]
    album = Album(
        title="Hollywood Bowl 2012",
        date=datetime.date(year=2012, day=26, month=10),
        venue="Hollywood Bowl",
        city="Los Angeles",
        bucket="priestc-dylan",
        folder="hollywood_bowl_2012",
        encoding="ogg q5",
        source="Core Sound micros DPA 4060 with Sony PCM - M10>Hard Drive>Flac"
    )
    album.songs = songs
    return album

def mock_songs():
    return {
        'length': 4,
        'songs': [
            [ "Ain't Talkin", "ain-t-talkin", 1],
            ["Alabama Getaway", "alabama-getaway", 1],
            ["All Along the Watchtower", "all-along-the-watchtower", 4],
            ["Am I Your Stepchild?","am-i-your-stepchild", 1],
        ]
    }

def mock_venues():
    return {
        "length": 5,
        "venues": [
            ["Earl's Court", "earl-s-court", 1],
            ["Mock Bowl", "hollywood-bowl", 2],
            ["Lakeland Center", "lakeland-center", 1],
            ["Stabler Arena (Lehigh University)", "stabler-arena-lehigh-university", 1],
            ["Wang Theatre", "wang-theatre", 1]
        ]
    }

def mock_venue():
    return {
        'venue': "Hollywood Bowl",
        'length': 1,
        'albums': [mock_album()]
    }

def mock_song():
    return {
        "length": 1,
        "title": "It's All Over Now Baby Blue",
        "songs": [
            {
                "album_id": 2,
                "track": 4,
                "title": "It's All Over Now Baby Blue",
                "id": 19,
                "duration": "4:53",
                "album": mock_album(),
                "slug": "it-s-all-over-now-baby-blue",
                "s3_name": "a04dylan090365.ogg"
            }
        ]
     }