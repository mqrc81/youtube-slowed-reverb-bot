import io
import os
from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

_CREDENTIALS_FILE = 'token_youtube_v3.json'


def _load_credentials():
    if not os.path.exists(_CREDENTIALS_FILE):
        return None
    return Credentials.from_authorized_user_file(_CREDENTIALS_FILE)


def _save_credentials(credentials):
    with io.open(_CREDENTIALS_FILE, 'w', encoding='UTF-8') as json_file:
        json_file.write(credentials.to_json())


def _create_service(client_secret_file, scopes):
    credentials = _load_credentials()

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            credentials = flow.run_console()

    _save_credentials(credentials)

    try:
        service = build('youtube', 'v3', credentials=credentials)
        return service
    except Exception as e:
        print('service creation failed:', e)
        return None


def upload_video(artist_name, track_name, genres, spotify_url, soundcloud_url, minutes_offset=0):
    youtube = _create_service('client_secret_key.json', ['https://www.googleapis.com/auth/youtube.force-ssl'])
    if not youtube:
        return

    publish_at = datetime.now().astimezone() + timedelta(minutes=minutes_offset)
    request = youtube.videos().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': f'{artist_name.lower()} - {track_name.lower()} (slowed + reverb)',
                'description': f'''
                {artist_name} - {track_name} slowed to perfection with reverb.
                
                Original version on Spotify: {spotify_url}.
                Slowed + Reverb version on SoundCloud: {soundcloud_url}.
                
                TODO copyright disclaimer.
                ''',
                'tags': [artist_name, track_name, *genres, 'slowed', 'reverb', 'slowedandreverb'],
                'categoryId': '10',
            },
            'status': {
                'publishAt': publish_at.replace(microsecond=0).isoformat()
            },
        }
    )
    response = request.execute()

    print(response)
