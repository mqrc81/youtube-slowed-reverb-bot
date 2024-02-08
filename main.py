import json

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_USA_VIRAl_50_PLAYLIST_ID = '37i9dQZEVXbKuaTI1Z1Afx'

if __name__ == '__main__':
    load_dotenv()

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    playlist = sp.playlist(SPOTIFY_USA_VIRAl_50_PLAYLIST_ID,
                           market='US', fields='tracks.items.track(id,name,artists(id,name))')
    print(json.dumps(playlist))
