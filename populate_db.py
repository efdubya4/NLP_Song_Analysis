import os
import sys
import psycopg2
import spotipy
import lyricsgenius
from dotenv import load_dotenv
import time
import random
from tqdm import tqdm
import logging
from spotify_auth import get_spotify_client

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('song_import.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

def connect_to_db():
    """Connect to PostgreSQL database with autocommit disabled"""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'hitscanadmin'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME', 'hit_scan')
        )
        conn.autocommit = False  # Ensure transactions are manual
        return conn, conn.cursor()
    except psycopg2.Error as e:
        logger.error(f"Database connection error: {e}")
        sys.exit(1)

def get_playlist_tracks(spotify, playlist_ids, limit=100):
    """Get tracks from playlists with better error handling"""
    all_tracks = []
    
    for playlist_id in playlist_ids:
        if not playlist_id.strip():
            continue
            
        try:
            # Verify playlist exists and is accessible
            playlist = spotify.playlist(
                playlist_id.strip(),
                fields='name,tracks.total',
                market='US'
            )
            logger.info(f"Found playlist: {playlist['name']}")
            
            offset = 0
            while True:
                try:
                    results = spotify.playlist_items(
                        playlist_id.strip(),
                        offset=offset,
                        fields='items(track(id,name,artists)),total',
                        market='US'
                    )
                    
                    if not results['items']:
                        break
                        
                    tracks = [item['track'] for item in results['items'] 
                            if item['track'] and not item['track'].get('is_local')]
                    all_tracks.extend(tracks)
                    logger.info(f"Retrieved {len(tracks)} tracks from {playlist['name']}")
                    
                    if len(all_tracks) >= limit:
                        return all_tracks[:limit]
                        
                    offset += len(results['items'])
                    if offset >= results['total']:
                        break
                        
                    time.sleep(1)  # Rate limiting
                    
                except spotipy.exceptions.SpotifyException as e:
                    if e.http_status == 401:
                        # Refresh token and retry
                        spotify.auth_manager.refresh_access_token()
                        continue
                    else:
                        logger.error(f"Error accessing playlist {playlist_id}: {e}")
                        break
                        
        except Exception as e:
            logger.error(f"Failed to process playlist {playlist_id}: {e}")
            continue
    
    return all_tracks[:limit]

def get_track_details(spotify, track_id):
    """Get detailed track information including audio features"""
    try:
        # Get basic track info
        track = spotify.track(track_id, market='US')
        
        # Get audio features
        features = spotify.audio_features([track_id])[0] if spotify.audio_features([track_id]) else None
        
        # Get artist details
        main_artist = track['artists'][0]
        artist = spotify.artist(main_artist['id'])
        
        # Get album details
        album = spotify.album(track['album']['id']) if track['album']['id'] else None
        
        return {
            'track': {
                'id': track['id'],
                'name': track['name'],
                'duration_ms': track['duration_ms'],
                'explicit': track['explicit'],
                'popularity': track['popularity'],
                'preview_url': track['preview_url'],
                'external_urls': track['external_urls'],
                'uri': track['uri']
            },
            'artist': {
                'id': artist['id'],
                'name': artist['name'],
                'genres': artist['genres'],
                'popularity': artist['popularity'],
                'followers': artist['followers']['total'],
                'images': artist['images']
            },
            'album': {
                'id': album['id'] if album else None,
                'name': album['name'] if album else track['album']['name'],
                'release_date': album['release_date'] if album else track['album']['release_date'],
                'total_tracks': album['total_tracks'] if album else track['album']['total_tracks'],
                'images': album['images'] if album else track['album']['images']
            },
            'audio_features': features
        }
        
    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 401:
            spotify.auth_manager.refresh_access_token()
            return get_track_details(spotify, track_id)  # Retry with fresh token
        logger.error(f"Error getting track details: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error getting track details: {e}")
        return None

def get_lyrics(genius, song_title, artist_name):
    """Get lyrics from Genius with improved error handling"""
    try:
        # Retry up to 3 times with delays
        for attempt in range(3):
            try:
                song = genius.search_song(song_title, artist_name)
                if song:
                    return song.lyrics
                
                # If no results, try with just the main artist (in case of featured artists)
                if "feat." in artist_name or "&" in artist_name:
                    main_artist = artist_name.split("feat.")[0].split("&")[0].strip()
                    song = genius.search_song(song_title, main_artist)
                    if song:
                        return song.lyrics
                
                return None
                
            except Exception as e:
                if attempt == 2:  # Last attempt
                    logger.error(f"Failed to get lyrics after 3 attempts for {song_title}: {e}")
                    return None
                time.sleep(2)  # Wait before retrying
                
    except Exception as e:
        logger.error(f"Unexpected error getting lyrics for {song_title}: {e}")
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
    query = """
    SELECT song_id FROM songs 
    WHERE spotify_id = %s
    """
    cursor.execute(query, (song_data['spotify_id'],))
    result = cursor.fetchone()
    
    if result:
        return result[0]
    
    # Insert new song with additional fields
    query = """
    INSERT INTO songs (
        title, 
        artist_id, 
        primary_genre_id, 
        spotify_id,
        album_id,
        album_name, 
        release_date, 
        duration_ms, 
        popularity, 
        explicit,
        preview_url,
        external_url,
        lyrics
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING song_id
    """
    
    cursor.execute(query, (
        song_data['title'],
        song_data['artist_id'],
        song_data['genre_id'],
        song_data['spotify_id'],
        song_data['album_id'],
        song_data['album_name'],
        song_data['release_date'],
        song_data['duration_ms'],
        song_data['popularity'],
        song_data['explicit'],
        song_data['preview_url'],
        song_data['external_url'],
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

def get_audio_features(spotify, track_ids):
    """Get audio features with batch processing and retries"""
    if not track_ids:
        return []
    
    features = []
    batch_size = 50  # Spotify API limit
    
    for i in range(0, len(track_ids), batch_size):
        batch = track_ids[i:i+batch_size]
        retries = 3
        
        while retries > 0:
            try:
                response = spotify.audio_features(batch)
                if response:
                    features.extend([f for f in response if f])
                break
            except spotipy.exceptions.SpotifyException as e:
                if e.http_status == 401:
                    spotify.auth_manager.refresh_access_token()
                    retries -= 1
                    continue
                elif e.http_status == 429:  # Rate limited
                    retry_after = int(e.headers.get('Retry-After', 1))
                    time.sleep(retry_after)
                    continue
                else:
                    logger.error(f"Error getting audio features: {e}")
                    break
            except Exception as e:
                logger.error(f"Unexpected error getting audio features: {e}")
                break
                
        time.sleep(0.5)  # Rate limiting between batches
    
    return features

def get_playlists_from_env():
    """Get playlist IDs from environment variables"""
    return {
        'Pop': os.getenv('POP_PLAYLISTS', '').split(','),
        'Hip Hop': os.getenv('HIP_HOP_PLAYLISTS', '').split(','),
        'Rock': os.getenv('ROCK_PLAYLISTS', '').split(','),
        'Electronic': os.getenv('ELECTRONIC_PLAYLISTS', '').split(','),
        'R&B': os.getenv('RNB_PLAYLISTS', '').split(',')
    }

def process_track(conn, cursor, track, genre_id, spotify, genius):
    """Process a single track with improved error handling"""
    try:
        # Get comprehensive track details
        track_details = get_track_details(spotify, track['id'])
        
        if not track_details:
            raise Exception(f"Could not get details for track {track['id']}")
            
        # Start transaction
        cursor.execute("BEGIN")
        
        try:
            # Insert artist
            artist_data = {
                'name': track_details['artist']['name'],
                'spotify_id': track_details['artist']['id'],
                'popularity': track_details['artist']['popularity'],
                'followers': track_details['artist']['followers'],
                'image_url': track_details['artist']['images'][0]['url'] if track_details['artist']['images'] else None
            }
            
            db_artist_id = insert_artist(cursor, artist_data)
            
            # Get lyrics
            lyrics = get_lyrics(genius, track_details['track']['name'], track_details['artist']['name'])
            
            # Insert song
            song_data = {
                'title': track_details['track']['name'],
                'artist_id': db_artist_id,
                'genre_id': genre_id,
                'spotify_id': track_details['track']['id'],
                'album_id': track_details['album']['id'],
                'album_name': track_details['album']['name'],
                'release_date': track_details['album']['release_date'],
                'duration_ms': track_details['track']['duration_ms'],
                'popularity': track_details['track']['popularity'],
                'explicit': track_details['track']['explicit'],
                'preview_url': track_details['track']['preview_url'],
                'external_url': track_details['track']['external_urls'].get('spotify'),
                'lyrics': lyrics
            }
            
            song_id = insert_song(cursor, song_data)
            
            # Insert audio features if available
            if track_details['audio_features']:
                insert_audio_features(cursor, song_id, track_details['audio_features'])
            
            conn.commit()
            logger.info(f"Successfully added: {track_details['track']['name']} by {track_details['artist']['name']}")
            return True
            
        except Exception as e:
            conn.rollback()
            raise e
            
    except Exception as e:
        logger.error(f"Error processing track {track.get('name', 'Unknown')}: {e}")
        return False

def populate_database():
    """Main database population function"""
    conn, cursor = connect_to_db()
    
    try:
        # Initialize Spotify client with auto token refresh
        spotify = get_spotify_client()
        
        # Test connection and token
        try:
            spotify.current_user()
        except:
            # Force token refresh
            spotify.auth_manager.refresh_access_token()
            
        # Initialize Genius API
        genius = lyricsgenius.Genius(os.getenv('GENIUS_ACCESS_TOKEN'))
        genius.verbose = False
        genius.remove_section_headers = True
        
        # Get genre IDs
        cursor.execute("SELECT genre_id, name FROM genres")
        genres = {name: id for id, name in cursor.fetchall()}
        
        # Get playlists from environment
        genre_playlists = get_playlists_from_env()
        
        # Process each genre
        for genre_name, playlist_ids in genre_playlists.items():
            if not playlist_ids[0]:
                logger.info(f"No playlists defined for {genre_name}, skipping...")
                continue
                
            logger.info(f"Processing {genre_name} playlists...")
            genre_id = genres[genre_name]
            
            # Get and process tracks
            tracks = get_playlist_tracks(spotify, playlist_ids)
            random.shuffle(tracks)
            
            with tqdm(tracks, desc=f"Adding {genre_name} songs") as pbar:
                for track in pbar:
                    success = process_track(conn, cursor, track, genre_id, spotify, genius)
                    pbar.set_postfix({'success': success})
                    time.sleep(0.5)  # General rate limiting
                    
    finally:
        cursor.close()
        conn.close()
        logger.info("Database population complete!")

if __name__ == "__main__":
    populate_database()