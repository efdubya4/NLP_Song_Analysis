import os
import psycopg2
from dotenv import load_dotenv

def setup_database():
    # Load environment variables
    load_dotenv()
    
    # Connect to PostgreSQL server
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', ''),
        database='postgres'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    
    # Create database if it doesn't exist
    db_name = os.getenv('DB_NAME', 'hits_scan')
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{db_name}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f'CREATE DATABASE {db_name}')
    
    # Close connection to postgres database
    cursor.close()
    conn.close()
    
    # Connect to our new database
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', ''),
        database=db_name
    )
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS genres (
        genre_id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL,
        description TEXT,
        typical_bpm_range VARCHAR(50)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        artist_id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        spotify_id VARCHAR(50) UNIQUE,
        popularity INTEGER,
        followers INTEGER,
        image_url TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS songs (
        song_id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        artist_id INTEGER REFERENCES artists(artist_id),
        primary_genre_id INTEGER REFERENCES genres(genre_id),
        spotify_id VARCHAR(50) UNIQUE,
        release_date DATE,
        duration_ms INTEGER,
        popularity INTEGER,
        explicit BOOLEAN,
        lyrics TEXT
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audio_features (
        feature_id SERIAL PRIMARY KEY,
        song_id INTEGER REFERENCES songs(song_id) UNIQUE,
        danceability FLOAT,
        energy FLOAT,
        key_value INTEGER,
        loudness FLOAT,
        mode INTEGER,
        speechiness FLOAT,
        acousticness FLOAT,
        instrumentalness FLOAT,
        liveness FLOAT,
        valence FLOAT,
        tempo FLOAT,
        time_signature INTEGER
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS artist_genres (
        artist_id INTEGER REFERENCES artists(artist_id),
        genre_id INTEGER REFERENCES genres(genre_id),
        PRIMARY KEY (artist_id, genre_id)
    )
    """)
    
    # Insert basic genres
    genres = [
        ('Pop', 'Popular music genre', '90-130'),
        ('Hip Hop', 'Hip hop and rap music', '85-115'),
        ('Rock', 'Rock music genre', '100-140'),
        ('Electronic', 'Electronic dance music', '120-140'),
        ('R&B', 'Rhythm and Blues', '60-100')
    ]
    
    for genre in genres:
        cursor.execute("""
        INSERT INTO genres (name, description, typical_bpm_range)
        VALUES (%s, %s, %s)
        ON CONFLICT (name) DO NOTHING
        """, genre)
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    setup_database()