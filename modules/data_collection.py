import pandas as pd
import requests
import lyricsgenius
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import os

# data_collection.py
class SpotifyDataCollector:
    def __init__(self):
        client_id = os.getenv('f6a5a0fa696441128c0e5bd3d7667c67')
        client_secret = os.getenv('e23e2595e1a1423d86809db56c95dc5c')
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
    
    def get_top_tracks_by_genre(self, genre, limit=50):
        """Fetch top tracks for a given genre"""
        results = self.sp.search(q=f'genre:{genre}', type='track', limit=limit)
        track_ids = [track['id'] for track in results['tracks']['items']]
        
        # Get audio features and track details
        audio_features = self.sp.audio_features(track_ids)
        track_details = [self.sp.track(track_id) for track_id in track_ids]
        
        return self._process_track_data(track_details, audio_features)
    
    def _process_track_data(self, track_details, audio_features):
        """Process raw data into structured format"""
        processed_data = []
        for detail, features in zip(track_details, audio_features):
            if features:  # Some tracks might not have features
                entry = {
                    'id': detail['id'],
                    'title': detail['name'],
                    'artist': ', '.join([artist['name'] for artist in detail['artists']]),
                    'popularity': detail['popularity'],
                    'duration_ms': detail['duration_ms'],
                    'danceability': features['danceability'],
                    'energy': features['energy'],
                    'key': features['key'],
                    'tempo': features['tempo'],
                    'valence': features['valence'],
                    'lyrics': None  # Will be fetched separately
                }
                processed_data.append(entry)
        return pd.DataFrame(processed_data)



# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# import lyricsgenius
# import pandas as pd

# # Initialize APIs
# sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='f6a5a0fa696441128c0e5bd3d7667c67', client_secret='e23e2595e1a1423d86809db56c95dc5c'))
# genius = lyricsgenius.Genius('D-SguwQ702lRELAEP9_dgflQ4f5MAamy1K9iemirO4tfwGy6HzuM5t7YZIb1jTku_5FO0dlBjHvOLne5UHpPNA')

# def get_track_data(artist_name, track_name):
#     # Get Spotify data
#     results = sp.search(q=f'artist:{artist_name} track:{track_name}', type='track')
#     if not results['tracks']['items']:
#         return None
    
#     track = results['tracks']['items'][0]
#     features = sp.audio_features(track['id'])[0]
    
#     # Get lyrics
#     try:
#         song = genius.search_song(track_name, artist_name)
#         lyrics = song.lyrics if song else None
#     except:
#         lyrics = None
    
#     return {
#         'id': track['id'],
#         'name': track['name'],
#         'artist': track['artists'][0]['name'],
#         'album': track['album']['name'],
#         'release_date': track['album']['release_date'],
#         'duration_ms': track['duration_ms'],
#         'popularity': track['popularity'],
#         **features,
#         'lyrics': lyrics
#     }

# # Example usage
# track_data = get_track_data("Taylor Swift", "Anti-Hero")