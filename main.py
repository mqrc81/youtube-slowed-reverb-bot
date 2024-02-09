import json

import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_USA_VIRAl_50_PLAYLIST_ID = '37i9dQZEVXbKuaTI1Z1Afx'
# SPOTIFY_USA_VIRAl_50_PLAYLIST_ID = '4wVt939CImGINCU4LYyZTN'  # my own top 250 playlist for test

mock_db = {
    'genres': {
        'hip hop': 2,
        'rap': 2,
        'atl hip hop': 2,
        'r&b': 2,
        'cloud rap': 2,
        'aesthetic rap': 2,
        'trap': 2,
        'viral rap': 2,
        'southern hip hop': 2,
        'alt z': 2,
        'emo rap': 2,
        'ottawa rap': 2,
        'alternative r&b': 2,
        'chicago rap': 2,
        'uk drill': 2,
        'glitchcore': 2,
        'new orleans rap': 2,
        'kentucky hip hop': 2,
        'uk hip hop': 2,
        'viral trap': 2,
        'cali rap': 2,
        'new york drill': 2,
        'pittsburgh rap': 2,
        'rap francais': 2,
        'philly rap': 2,
        'zxc': 2,
        'trap soul': 2,
        'melodic drill': 2,
        'french hip hop': 2,
        'german cloud rap': 2,
        'nyc rap': 2,
        'tennessee hip hop': 2,
        'pop rap': 2,
        'deep underground hip hop': 2,
        'scream rap': 2,
        'canadian trap': 2,
        'london rap': 2,
        'manchester hip hop': 2,
        'cloud rap francais': 2,
        'underground hip hop': 2,
        'canadian hip hop': 2,
        'miami hip hop': 2,
        'new jersey rap': 2,
        'german trap': 2,
        'melodic rap': 2,
        'chill drill': 2,
        'rap latina': 2,
        'belgian hip hop': 2,
        'german hip hop': 2,
        'bedroom r&b': 2,
        'florida rap': 2,
        'pop urbaine': 2,
        'drift phonk': 2,
        'rage rap': 2,
        'dark trap': 2,
        'j-pop': 1,
        'new wave': 1,
        'dirty south rap': 1,
        'old school atlanta hip hop': 1,
        'alternative hip hop': 1,
        'j-rock': 1,
        'neo soul': 1,
        'memphis hip hop': 1,
        'sacramento hip hop': 1,
        'r&drill': 1,
        'rap lyonnais': 1,
        'brooklyn drill': 1,
        'drill francais': 1,
        'ohio hip hop': 1,
        'german drill': 1,
        'rap belge': 1,
        'dutch drill': 1,
        'indie hip hop': 1,
        'aussie drill': 1,
        'philly drill': 1,
        'trap queen': 1,
        'drill': 1,
        'political hip hop': 0,
        'country': 0,
        'classic oklahoma country': 0,
        'pixel': 0,
        'contemporary country': 0,
        'show tunes': 0,
        'otacore': 0,
        'country road': 0,
        'broadway': 0,
        'sierreno': 0,
        'dc indie': 0,
        'singer-songwriter pop': 0,
        'lds youth': 0,
        'new romantic': 0,
        'dance pop': 0,
        'singer-songwriter': 0,
        'country rock': 0,
        'outlaw country': 0,
        'corridos tumbados': 0,
        'album rock': 0,
        'rock': 0,
        'hollywood': 0,
        'nashville sound': 0,
        'movie tunes': 0,
        'classic country pop': 0,
        'conscious hip hop': 0,
        'sad sierreno': 0,
        'dance rock': 0,
        'classic texas country': 0,
        'europop': 0,
        'colombian pop': 0,
        'synthpop': 0,
        'indie r&b': 0,
        'new wave pop': 0,
        'corrido': 0,
        'soft rock': 0,
        'soul flow': 0,
        'lgbtq+ hip hop': 0,
        'edm': 0,
        'electro house': 0,
        'hyperpop': 0,
        'german hyperpop': 0,
        'electronic trap': 0,
        'proto-hyperpop': 0,
        'meme rap': 0,
        'meme': 0,
    },
    # 'tracks': {'0BhdrTIB5flACZyaLjdzp4', '7E2DqvnVtbIrFrL5X6YH9Q', '4iEoDBAgMJIzest7VsDgmT', '3QQAeMQbbjZXVFbF8DgFWT',
    #            '0M7mWKqwTIaVjYyxfZmtTa', '6NMqeF0Ssmi7d3dSUqnOFf', '7G6l2FtQyRhQgYgut2I6i8', '6UTPUfrTvKzD7GhLAhi1x7',
    #            '6ZXL1A1BVshe1JZ1IY734k', '0WIv5qV41y6YjjB9V1biuC', '4YKAOXyqkKZ5gOZR0AmVMN', '4pxE9huyROQ61TlyS0Mhhi',
    #            '32jHB7W9b08OTorAqR0cJo', '4DLSN6f2Cp5eWIa5Vfn9kj', '54L7uacUGRkvoLokUlNWfH', '4tKGFmENO69tZR9ahgZu48',
    #            '6dpLxbF7lfCAnC9QRTjNLK', '69phA1R4gmQsBFRQ3INW8C', '2ddFi6kHdtkFtO5Z8gNILu', '0R6NfOiLzLj4O5VbYSJAjf',
    #            '5v3MSh7CD3VNyCwAoSha5p', '7rDcULv8vV16vetBjPJhuE', '6XaJfhwof7qIgbbXO5tIQI', '4HMop4Re0iucehmF7mgV27',
    #            '17phhZDn6oGtzMe56NuWvj', '6uTPdRrEDeH8Fyg5L5qmeU', '4PmQAzVNQBw7n1OpmPvovb', '1UsPflAuWTNteFUPJAJe8E',
    #            '6tNQ70jh4OwmPGpYy6R2o9', '5WFDseVq6n2LnKQMByCYnj', '5crY7axm3GejOxy5PsnnPk', '3VHevS1BocAcrihLnl11DG',
    #            '3Pbp7cUCx4d3OAkZSCoNvn', '1HbzxLqpNVPdiBXvpC7Ovb', '5taqvRgn1DdZ117p2DhPXQ', '1BEioZa6o8AVDmOh5Sc86j',
    #            '7sRz3vO2bEMhZGEkjnfMxb', '0kdqcbwei4MDWFEX5f33yG', '792RoRzlyIP29zz03556Ja', '3h5TiWTqGxjSjFrbruPFH9',
    #            '1v4m9GLt7lpFM5iOvwQZrU', '2Evk4YMwD4zjjha2k3dbV7', '42zkB4Eh0PAxwnTaXP6HxU', '4TJUS843fKiqqIzycM74Oy',
    #            '51EpFns3CG9taCMQz6XDom', '45FCt12lQyBdxUrLtM4Uor'}
    'tracks': {'b', 'a'},
}


def partition(lst, size):
    return [lst[i:i + size] for i in range(0, len(lst), size)]


if __name__ == '__main__':
    load_dotenv()

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    playlist = sp.playlist(SPOTIFY_USA_VIRAl_50_PLAYLIST_ID, market='US',
                           fields='tracks.items.track(id,name,artists(id,name))')
    print(len(playlist['tracks']['items']))

    new_tracks = []
    for item in playlist['tracks']['items']:
        if item['track']['id'] not in mock_db['tracks']:
            new_tracks.append(item['track'])
            mock_db['tracks'].add(item['track']['id'])

    artist_ids_partitioned = partition([artist['id']
                                        for track in new_tracks
                                        for artist in track['artists']
                                        if artist['id'] is not None], 50)
    print(artist_ids_partitioned)
    artists = [artist
               for artist_ids in artist_ids_partitioned
               for artist in sp.artists(artist_ids)['artists']]
    print(json.dumps(artists))

    genres = {genre for artist in artists for genre in artist['genres']}
    print(len(genres))
    # print(genres.difference(set(mock_db['genres'].keys())))

    # mock_db['tracks'].update(new_tracks)
