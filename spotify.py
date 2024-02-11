import logging

import spotipy
from spotipy import SpotifyClientCredentials

import postgres
from postgres import GenrePriority

_PLAYLISTS_IDS = [
    '37i9dQZEVXbKuaTI1Z1Afx',  # Top 50 Viral USA
    # TODO add more
]
_PLAYLIST_FIELDS = 'tracks.items.track(id,name,artists(id,name))'
_DAILY_VIDEO_LIMIT = 5


def collect_new_tracks():
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    new_tracks = [track
                  for playlist_id in _PLAYLISTS_IDS
                  for track in sp.playlist(playlist_id, market='US', fields=_PLAYLIST_FIELDS)['tracks']['items']
                  if track['id'] not in postgres.MOCK_DB['tracks']]

    artist_ids_partitioned = _partition([artist['id']
                                         for track in new_tracks
                                         for artist in track['artists']
                                         if artist['id'] is not None], 50)

    artists = {artist['id']: {'name': artist['name'], 'genres': artist['genres']}
               for artist_ids in artist_ids_partitioned
               for artist in sp.artists(artist_ids)['artists']}

    handled_tracks = set()
    priority_tracks = []
    backup_tracks = []
    for track in new_tracks:
        if track['id'] in handled_tracks:
            continue  # skip duplicate tracks
        handled_tracks.add(track['id'])
        max_genre_priority = _collect_genre_priority(track, artists)
        _handle_genre_priority(max_genre_priority, track, priority_tracks, backup_tracks)
    priority_tracks.extend(backup_tracks)

    minutes_offset = 0
    for i in range(0, min(len(priority_tracks), _DAILY_VIDEO_LIMIT)):
        track = priority_tracks[i]


def _collect_genre_priority(track, artists):
    max_genre_priority = -1
    for artist in track['artists']:
        for genre in artists[artist['id']]['genres']:
            genre_priority = postgres.MOCK_DB['genres'][genre]
            if genre_priority is None:
                logging.warning('Unknown genre {} for \'{} - {}\''.format(genre, artist['name'], track['name']))
            else:
                max_genre_priority = max(max_genre_priority, genre_priority)
            if max_genre_priority is GenrePriority.ALWAYS.value:
                return genre_priority  # short-circuit
    return max_genre_priority


def _handle_genre_priority(max_genre_priority, track, priority_tracks, backup_tracks):
    if max_genre_priority is GenrePriority.ALWAYS.value:
        priority_tracks.append(track)
    elif max_genre_priority is GenrePriority.MAYBE.value:
        backup_tracks.append(track)
    elif max_genre_priority is GenrePriority.NEVER.value:
        postgres.MOCK_DB['tracks'].add(track['id'])


def _partition(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]
