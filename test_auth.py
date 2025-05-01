from spotify_auth import get_spotify_client
import os
from dotenv import load_dotenv

def test_auth():
    try:
        # Initialize Spotify client
        spotify = get_spotify_client()
        
        # Test authentication with a simple API call
        results = spotify.current_user()
        print("Authentication successful!")
        print(f"Connected as: {results['display_name']}")
        
        # Test playlist access
        load_dotenv()
        test_playlist = os.getenv('POP_PLAYLISTS').split(',')[0]
        playlist = spotify.playlist(test_playlist, fields='name')
        print(f"Successfully accessed playlist: {playlist['name']}")
        
        return True
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_auth()