-- Active: 1746051802775@@127.0.0.1@5432
-- Create the database
CREATE DATABASE IF NOT EXISTS hit_scan;
USE hit_scan;

-- Create genres table
CREATE TABLE genres (
    genre_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    typical_bpm_range VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create artists table
CREATE TABLE artists (
    artist_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    spotify_id VARCHAR(50) UNIQUE,
    popularity INT,
    followers INT,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create artist_genres junction table
CREATE TABLE artist_genres (
    artist_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (artist_id, genre_id),
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
);

-- Create songs table
CREATE TABLE songs (
    song_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INT NOT NULL,
    primary_genre_id INT NOT NULL,
    spotify_id VARCHAR(50) UNIQUE,
    release_date DATE,
    duration_ms INT,
    popularity INT,
    explicit BOOLEAN DEFAULT FALSE,
    lyrics TEXT,
    lyrics_updated_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
    FOREIGN KEY (primary_genre_id) REFERENCES genres(genre_id)
);

-- Create song_genres junction table for secondary genres
CREATE TABLE song_genres (
    song_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (song_id, genre_id),
    FOREIGN KEY (song_id) REFERENCES songs(song_id) ON DELETE CASCADE,
    FOREIGN KEY (genre_id) REFERENCES genres(genre_id) ON DELETE CASCADE
);

-- Create audio_features table
CREATE TABLE audio_features (
    song_id INT PRIMARY KEY,
    danceability FLOAT,
    energy FLOAT,
    key_value INT,
    loudness FLOAT,
    mode INT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    time_signature INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (song_id) REFERENCES songs(song_id) ON DELETE CASCADE
);

-- Create analysis_results table
CREATE TABLE analysis_results (
    analysis_id INT AUTO_INCREMENT PRIMARY KEY,
    song_id INT NOT NULL,
    virality_score FLOAT,
    sentiment_score FLOAT,
    sentiment_magnitude FLOAT,
    complexity_score FLOAT,
    repetition_score FLOAT,
    topic_relevance_score FLOAT,
    originality_score FLOAT,
    analysis_version VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (song_id) REFERENCES songs(song_id) ON DELETE CASCADE
);

-- Create trending_history table
CREATE TABLE trending_history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    song_id INT NOT NULL,
    date DATE NOT NULL,
    chart_position INT,
    streams_count BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (song_id) REFERENCES songs(song_id) ON DELETE CASCADE
);

-- Insert the 5 main genres
INSERT INTO genres (name, description, typical_bpm_range) VALUES
('Pop', 'Contemporary popular music characterized by catchy melodies and accessible structures', '90-130'),
('Hip Hop', 'Music characterized by rhythmic vocals, beats, and often sampling', '85-115'),
('Rock', 'Guitar-driven music with strong rhythms and often rebellious themes', '110-140'),
('Electronic', 'Computer-generated music with electronic sounds and beats', '120-150'),
('R&B', 'Rhythm and blues with soulful vocals and contemporary production', '60-100');