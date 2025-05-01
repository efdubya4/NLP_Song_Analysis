import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from dotenv import load_dotenv
from modules.data_collection import AcousticBrainzCollector

load_dotenv()

class SpotifyCollector:
    def __init__(self):
        """Initialize Spotify API client with credentials"""
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        if not client_id or not client_secret:
            raise ValueError("Spotify credentials not found in environment variables")
            
        auth_manager = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def get_tracks(self, genre, limit=10, market='US'):
        """
        Get top tracks by genre from Spotify
        Args:
            genre: Music genre to search for
            limit: Number of tracks to return (max 50)
            market: Country code (e.g., 'US', 'GB')
        Returns:
            List of track dictionaries with metadata
        """
        collector = AcousticBrainzCollector()
        try:
            # Search for playlists tagged with this genre
            playlists = self.sp.search(
                q=f'genre:"{genre}"',
                type='playlist',
                limit=1,
                market=market
            )['playlists']['items']
            
            if not playlists:
                print(f"No playlists found for genre: {genre}")
                return pd.DataFrame()
                
            # Get tracks from the first relevant playlist
            playlist_id = playlists[0]['id']
            results = self.sp.playlist_tracks(
                playlist_id,
                market=market,
                limit=min(limit, 50)  # Spotify's max limit per request
            )
            
            tracks = []
            for item in results['items']:
                track = item['track']
                if not track:
                    continue
                    
                # Get audio features for each track
                ab_features = collector.get_audio_features(track['id'])

                tracks.append({
                    # AcousticBrainz features (if available)
                    'ab_mood': ab_features.get('mood', {}).get('value') if ab_features else None,
                    'ab_genre': ab_features.get('genre', {}).get('value') if ab_features else None,
                    'genre': genre
                })
            
            return pd.DataFrame(tracks)
            
        except Exception as e:
            print(f"Error fetching tracks: {str(e)}")
            return pd.DataFrame()