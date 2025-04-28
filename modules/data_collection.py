import pandas as pd
import requests
from typing import Optional, Dict, List
from datetime import datetime
import time
import os
from dotenv import load_dotenv
from modules.lyric_fetcher import GeniusLyricFetcher

# data_collection.py
class AcousticBrainzCollector:
    def __init__(self):
        load_dotenv()
        self.base_url = "https://acousticbrainz.org/api/v1"
        self.lyric_fetcher = GeniusLyricFetcher()
    
    def get_audio_features(self, mbid: str) -> Optional[Dict]:
        """Get audio features for a MusicBrainz recording ID"""
        try:
            response = requests.get(f"{self.base_url}/{mbid}/high-level")
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching AcousticBrainz data: {e}")
            return None
        
    def search_mbid(self, track_name: str, artist: str) -> Optional[str]:
        """Search MusicBrainz for a recording MBID"""
        params = {
            "query": f"recording:{track_name} AND artist:{artist}",
            "fmt": "json"
        }
        try:
            response = requests.get(
                "https://musicbrainz.org/ws/2/recording/",
                params=params,
                headers={"User-Agent": "NLP_Project/1.0 (neranti.gary@bison.howard.edu)"}
            )
            if response.status_code == 200 and response.json().get("recordings"):
                return response.json()["recordings"][0]["id"]
            return None
        except Exception as e:
            print(f"MusicBrainz search error: {e}")
            return None

    def get_top_tracks_by_genre(self, genre, limit=50):
         # Note: AcousticBrainz doesn't have direct genre search, 
        # so we'll use MusicBrainz for initial track listing
        params = {
            "query": f'tag:"{genre}"',
            "fmt": "json",
            "limit": limit
        }
        
        try:
            recordings = []
            response = requests.get(
                "https://musicbrainz.org/ws/2/recording/",
                params=params,
                headers={"User-Agent": "YourApp/1.0 (contact@example.com)"}
            )
            
            if response.status_code == 200:
                for recording in response.json().get("recordings", [])[:limit]:
                    mbid = recording["id"]
                    features = self.get_audio_features(mbid)
                    
                    if features:
                        recordings.append({
                            "mbid": mbid,
                            "title": recording.get("title", ""),
                            "artist": recording["artist-credit"][0]["name"] if recording.get("artist-credit") else "",
                            **self._map_features(features),
                            "lyrics": None  # Will be fetched later
                        })
                    time.sleep(1)  # Rate limiting
            
            return pd.DataFrame(recordings)
            
        except Exception as e:
            print(f"Error fetching genre tracks: {e}")
            return pd.DataFrame()

    def _find_top_playlist(self, genre, market):
        """Find official 'Top [Genre]' playlist"""
        query = f"Top {genre} - {datetime.now().year}"
        results = self.sp.search(q=query, type='playlist', limit=1)
        return results['playlists']['items'][0]['id'] if results['playlists']['items'] else None  
    
    def _map_features(self, data: Dict) -> Dict:
        """Map AcousticBrainz features to our schema"""
        return {
            "danceability": data.get("highlevel", {}).get("danceability", {}).get("value", 0),
            "energy": data.get("highlevel", {}).get("energy", {}).get("value", 0),
            "key": data.get("tonal", {}).get("key_key", "Unknown"),
            "tempo": data.get("rhythm", {}).get("bpm", 0),
            "valence": data.get("highlevel", {}).get("mood_acoustic", {}).get("value", 0),
            "instrumentalness": data.get("highlevel", {}).get("instrumental", {}).get("value", 0)
        }

    def add_lyrics_to_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add lyrics to dataframe with rate limiting"""
        if df.empty:
            return df
            
        for idx, row in df.iterrows():
            if pd.isna(row.get('lyrics')):
                df.at[idx, 'lyrics'] = self.lyric_fetcher.get_lyrics(
                    row['title'],
                    row['artist']
                )
                time.sleep(1)  # Respect rate limits
        return df



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