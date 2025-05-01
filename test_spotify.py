from spotify_auth import get_spotify_client
import os
from dotenv import load_dotenv
import sys

def verify_credentials():
    """Verify that required environment variables are set"""
    load_dotenv()
    missing = []
    
    required = {
        'SPOTIFY_CLIENT_ID': 'Spotify Client ID',
        'SPOTIFY_CLIENT_SECRET': 'Spotify Client Secret',
        'POP_PLAYLISTS': 'Pop Playlists'
    }
    
    for var, name in required.items():
        if not os.getenv(var):
            missing.append(name)
    
    if missing:
        raise Exception(f"Missing required environment variables: {', '.join(missing)}")

def verify_playlist_exists(spotify, playlist_id):
    """Verify that a playlist ID exists and is accessible"""
    try:
        # First try a basic search
        results = spotify.search(
            q=f"playlist:{playlist_id}",
            type='playlist',
            limit=1
        )
        
        if not results['playlists']['items']:
            raise Exception(f"Playlist {playlist_id} not found")
            
        # Then try to access the playlist directly
        playlist = spotify.playlist(
            playlist_id,
            fields='name,tracks.total',
            market='US'
        )
        return playlist
        
    except Exception as e:
        raise Exception(f"Failed to verify playlist {playlist_id}: {str(e)}")

def test_spotify_connection():
    """Test Spotify API connection and playlist access"""
    try:
        # Verify credentials first
        verify_credentials()
        
        # Initialize Spotify client
        print("Initializing Spotify client...")
        spotify = get_spotify_client()
        
        # Get and verify playlist ID
        playlists = os.getenv('POP_PLAYLISTS', '').split(',')
        if not playlists or not playlists[0]:
            raise Exception("No playlist IDs configured")
            
        test_playlist_id = playlists[0].strip()
        print(f"\nTesting playlist access for ID: {test_playlist_id}")
        
        # Verify playlist exists
        playlist = verify_playlist_exists(spotify, test_playlist_id)
        
        print(f"Successfully accessed playlist: {playlist['name']}")
        print(f"Total tracks: {playlist['tracks']['total']}")
        return True
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_spotify_connection()
    sys.exit(0 if success else 1)