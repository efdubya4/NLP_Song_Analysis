import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

def test_spotify():
    auth = SpotifyClientCredentials(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
    )
    sp = spotipy.Spotify(auth_manager=auth)
    try:
        results = sp.search(q='genre:pop', type='track', limit=1)
        print("Spotify connection successful!")
        return True
    except Exception as e:
        print(f"Spotify error: {e}")
        return False



if __name__ == "__main__":
    test_spotify()