import os
import psycopg2
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import lyricsgenius
from dotenv import load_dotenv
import time
import random
from tqdm import tqdm

# Load environment variables
load_dotenv()

# Connect to database
def connect_to_db():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'hits_scan')
    )
    return conn, conn.cursor()

# Initialize APIs
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
    )
)

genius = lyricsgenius.Genius(os.getenv('GENIUS_ACCESS_TOKEN'))
genius.verbose = False  # Turn off status messages
genius.remove_section_headers = True  # Remove section headers from lyrics

def get_playlist_tracks(playlist_ids):
    """Get tracks from playlists"""
    all_tracks = []
    for playlist_id in playlist_ids:
        offset = 0
        while True:
            response = spotify.playlist_items(
                playlist_id,
                offset=offset,
                fields='items.track.id,items.track.name,items.track.artists,total',
                limit=100
            )
            
            if len(response['items']) == 0:
                break
                
            for item in response['items']:
                if item['track'] and item['track']['id']:
                    all_tracks.append(item['track'])
            
            offset += len(response['items'])
            if offset >= response['total']:
                break
                
            # Respect API rate limits
            time.sleep(0.5)
    
    return all_tracks

def get_track_details(track_id):
    """Get detailed track information including audio features"""
    track = spotify.track(track_id)
    audio_features = spotify.audio_features(track_id)[0]
    return track, audio_features

def get_artist_details(artist_id):
    """Get detailed artist information"""
    return spotify.artist(artist_id)

def get_lyrics(song_title, artist_name):
    """Get lyrics from Genius"""
    try:
        song = genius.search_song(song_title, artist_name)
        if song:
            return song.lyrics
    except Exception as e:
        print(f"Error getting lyrics for {song_title}: {e}")
    
    return None

def insert_genre(cursor, name, description, bpm_range):
    """Insert a genre and return its ID"""
    query = "INSERT INTO genres (name, description, typical_bpm_range) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, description, bpm_range))
    return cursor.lastrowid

def insert_artist(cursor, artist_data):
    """Insert an artist and return its ID"""
    # Check if artist already exists
    query = "SELECT artist_id FROM artists WHERE spotify_id = %s"
    cursor.execute(query, (artist_data['spotify_id'],))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    # Insert new artist
    query = """
    INSERT INTO artists (name, spotify_id, popularity, followers, image_url)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING artist_id
    """
    cursor.execute(query, (
        artist_data['name'],
        artist_data['spotify_id'],
        artist_data['popularity'],
        artist_data['followers'],
        artist_data['image_url']
    ))
    return cursor.fetchone()[0]

def insert_artist_genre(cursor, artist_id, genre_id):
    """Link artist with genre"""
    query = """
    INSERT INTO artist_genres (artist_id, genre_id) 
    VALUES (%s, %s)
    ON CONFLICT (artist_id, genre_id) DO NOTHING
    """
    cursor.execute(query, (artist_id, genre_id))

def insert_song(cursor, song_data):
    """Insert a song and return its ID"""
    # Check if song already exists
    query = "SELECT song_id FROM songs WHERE spotify_id = %s"
    cursor.execute(query, (song_data['spotify_id'],))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    # Insert new song
    query = """
    INSERT INTO songs (
        title, artist_id, primary_genre_id, spotify_id, 
        release_date, duration_ms, popularity, explicit, lyrics
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING song_id
    """
    cursor.execute(query, (
        song_data['title'],
        song_data['artist_id'],
        song_data['genre_id'],
        song_data['spotify_id'],
        song_data['release_date'],
        song_data['duration_ms'],
        song_data['popularity'],
        song_data['explicit'],
        song_data['lyrics']
    ))
    return cursor.fetchone()[0]

def insert_audio_features(cursor, song_id, features):
    """Insert audio features for a song"""
    query = """
    INSERT INTO audio_features (
        song_id, danceability, energy, key_value, loudness, mode,
        speechiness, acousticness, instrumentalness, liveness,
        valence, tempo, time_signature
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO UPDATE SET
        danceability = EXCLUDED.danceability,
        energy = EXCLUDED.energy,
        key_value = EXCLUDED.key_value,
        loudness = EXCLUDED.loudness,
        mode = EXCLUDED.mode,
        speechiness = EXCLUDED.speechiness,
        acousticness = EXCLUDED.acousticness,
        instrumentalness = EXCLUDED.instrumentalness,
        liveness = EXCLUDED.liveness,
        valence = EXCLUDED.valence,
        tempo = EXCLUDED.tempo,
        time_signature = EXCLUDED.time_signature
    """
    cursor.execute(query, (
        song_id,
        features['danceability'],
        features['energy'],
        features['key'],
        features['loudness'],
        features['mode'],
        features['speechiness'],
        features['acousticness'],
        features['instrumentalness'],
        features['liveness'],
        features['valence'],
        features['tempo'],
        features['time_signature']
    ))

def populate_database():
    """Main function to populate the database with songs"""
    conn, cursor = connect_to_db()
    
    # Get genre IDs
    cursor.execute("SELECT genre_id, name FROM genres")
    genres = {name: id for id, name in cursor.fetchall()}
    
    # Genre-specific playlists
    genre_playlists = {
        'Pop': [
            '37i9dQZF1DXcBWIGoYBM5M',  # Today's Top Hits
            '37i9dQZF1DX1ngEVM0lKrb'   # Nobody's Listening
        ],
        'Hip Hop': [
            '37i9dQZF1DX0XUsuxWHRQd',  # RapCaviar
            '37i9dQZF1DX2RxBh64BHjQ'   # Most Necessary
        ],
        'Rock': [
            '37i9dQZF1DWXRqgorJj26U',  # Rock Classics
            '37i9dQZF1DX1rVvRgjX59F'   # Rock This
        ],
        'Electronic': [
            '37i9dQZF1DX4dyzvuaRJ0n',  # mint
            '37i9dQZF1DX6J5NfMJS675'   # Dance Party
        ],
        'R&B': [
            '37i9dQZF1DX4SBhb3fqCJd',  # Are & Be
            '37i9dQZF1DX9XIFQuFvzM4'   # Soul Coffee
        ]
    }
    
    # Process each genre
    for genre_name, playlist_ids in genre_playlists.items():
        print(f"Processing {genre_name} playlists...")
        genre_id = genres[genre_name]
        
        # Get tracks from playlists
        tracks = get_playlist_tracks(playlist_ids)
        random.shuffle(tracks)
        
        # Limit to 100 songs per genre
        tracks = tracks[:100]
        
        # Process each track
        for track in tqdm(tracks, desc=f"Adding {genre_name} songs"):
            try:
                # Get track details
                track_detail, audio_features = get_track_details(track['id'])
                
                # Get main artist details
                artist_id = track['artists'][0]['id']
                artist_detail = get_artist_details(artist_id)
                
                # Get lyrics (with rate limiting)
                lyrics = get_lyrics(track['name'], artist_detail['name'])
                time.sleep(1)  # Genius API rate limiting
                
                # Insert artist
                artist_data = {
                    'name': artist_detail['name'],
                    'spotify_id': artist_detail['id'],
                    'popularity': artist_detail['popularity'],
                    'followers': artist_detail['followers']['total'],
                    'image_url': artist_detail['images'][0]['url'] if artist_detail['images'] else None
                }
                db_artist_id = insert_artist(cursor, artist_data)
                
                # Link artist to genre
                insert_artist_genre(cursor, db_artist_id, genre_id)
                
                # Insert song
                song_data = {
                    'title': track_detail['name'],
                    'artist_id': db_artist_id,
                    'genre_id': genre_id,
                    'spotify_id': track_detail['id'],
                    'release_date': track_detail['album']['release_date'],
    conn.close()
    print("Database population complete!")

if __name__ == "__main__":
    populate_database()