import os
import re
import nltk
import spotipy
import numpy as np
import lyricsgenius
from dotenv import load_dotenv
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob

# Load environment variables
load_dotenv()

# Initialize APIs
genius = lyricsgenius.Genius(os.getenv('GENIUS_ACCESS_TOKEN'))
spotify = spotipy.Spotify(
    auth_manager=spotipy.SpotifyClientCredentials(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
    )
)

# Download necessary NLTK packages
nltk.download('vader_lexicon', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Initialize NLP tools
sia = SentimentIntensityAnalyzer()
stop_words = set(stopwords.words('english'))

# Define viral topic keywords
viral_topics = {
    'love': 5,
    'dance': 8,
    'party': 7,
    'night': 6,
    'heart': 5,
    'break': 6,
    'girl': 4,
    'boy': 4,
    'baby': 5,
    'time': 3,
    'feel': 4,
    'life': 3,
    'dream': 5,
    'world': 3,
    'summer': 7,
    'money': 6,
    'free': 5,
    'light': 4,
    'fire': 5,
    'body': 6
}

def clean_lyrics(lyrics):
    """Clean and preprocess lyrics text."""
    if not lyrics:
        return ""
    
    # Remove section headers like [Verse], [Chorus], etc.
    lyrics = re.sub(r'\[.*?\]', '', lyrics)
    
    # Remove empty lines
    lyrics = re.sub(r'\n\s*\n', '\n', lyrics)
    
    # Remove URLs, numbers, special characters
    lyrics = re.sub(r'http\S+', '', lyrics)
    lyrics = re.sub(r'\d+', '', lyrics)
    lyrics = re.sub(r'[^\w\s]', '', lyrics)
    
    return lyrics.strip()

def get_song_details(track_name, artist_name):
    """Get song details from Spotify and lyrics from Genius."""
    try:
        # Search for the track on Spotify
        search_query = f"track:{track_name} artist:{artist_name}"
        results = spotify.search(q=search_query, type="track", limit=1)
        
        if not results['tracks']['items']:
            return None, "Track not found on Spotify"
        
        track = results['tracks']['items'][0]
        track_id = track['id']
        
        # Get artist popularity
        artist_id = track['artists'][0]['id']
        artist_info = spotify.artist(artist_id)
        
        # Get audio features
        audio_features = spotify.audio_features(track_id)[0]
        
        # Get lyrics from Genius
        song = genius.search_song(track_name, artist_name)
        lyrics = song.lyrics if song else ""
        
        return {
            'track_id': track_id,
            'track_name': track['name'],
            'artist_name': track['artists'][0]['name'],
            'artist_id': artist_id,
            'artist_popularity': artist_info['popularity'],
            'track_popularity': track['popularity'],
            'audio_features': audio_features,
            'lyrics': lyrics,
            'cleaned_lyrics': clean_lyrics(lyrics)
        }, None
        
    except Exception as e:
        return None, f"Error fetching song details: {str(e)}"

def analyze_lyrics_sentiment(lyrics):
    """Analyze sentiment of lyrics."""
    if not lyrics:
        return {'compound': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
    
    sentiment = sia.polarity_scores(lyrics)
    return sentiment

def analyze_lyrics_topics(lyrics):
    """Analyze topics in lyrics using basic keyword matching."""
    if not lyrics:
        return {'topic_score': 0, 'topics': {}}
    
    words = word_tokenize(lyrics.lower())
    words = [word for word in words if word.isalnum() and word not in stop_words]
    
    # Count occurrences of viral topics
    topic_counts = {}
    for word in words:
        if word in viral_topics:
            if word in topic_counts:
                topic_counts[word] += 1
            else:
                topic_counts[word] = 1
    
    # Calculate topic score
    topic_score = 0
    for word, count in topic_counts.items():
        topic_score += viral_topics[word] * min(count, 5)  # Cap influence of repeated words
    
    # Normalize by text length
    if words:
        topic_score = topic_score / (len(words) ** 0.5)  # Square root to reduce penalization for longer songs
    
    return {
        'topic_score': min(10, topic_score),  # Cap at 10
        'topics': topic_counts
    }

def analyze_lyrics_complexity(lyrics):
    """Analyze lyrical complexity."""
    if not lyrics:
        return {'complexity_score': 0}
    
    words = word_tokenize(lyrics.lower())
    words = [word for word in words if word.isalnum()]
    
    if not words:
        return {'complexity_score': 0}
    
    # Calculate metrics
    unique_words = len(set(words))
    total_words = len(words)
    word_repetition = total_words / unique_words if unique_words > 0 else 0
    
    # TextBlob for readability
    blob = TextBlob(lyrics)
    sentences = len(blob.sentences)
    words_per_sentence = total_words / sentences if sentences > 0 else 0
    
    # Simple complexity score (lower is more repetitive, higher is more complex)
    # For virality, mid-range complexity works best
    raw_complexity = (unique_words / total_words) * 10 if total_words > 0 else 0
    
    # Adjust so that mid-range complexity scores higher for virality
    adjusted_complexity = 10 - abs(5 - raw_complexity)
    
    return {
        'complexity_score': adjusted_complexity,
        'unique_word_ratio': unique_words / total_words if total_words > 0 else 0,
        'word_repetition': word_repetition,
        'words_per_sentence': words_per_sentence
    }

def calculate_virality_score(song_data):
    """Calculate virality score based on multiple factors."""
    if not song_data:
        return 0, {}
    
    # Get component scores
    sentiment = analyze_lyrics_sentiment(song_data['cleaned_lyrics'])
    topics = analyze_lyrics_topics(song_data['cleaned_lyrics'])
    complexity = analyze_lyrics_complexity(song_data['cleaned_lyrics'])
    audio = song_data['audio_features']
    
    # Component weights
    weights = {
        'artist_popularity': 0.15,
        'track_popularity': 0.10,
        'danceability': 0.12,
        'energy': 0.10,
        'valence': 0.08,
        'sentiment': 0.12,
        'topic_relevance': 0.18,
        'complexity': 0.15
    }
    
    # Calculate component scores
    component_scores = {
        'artist_popularity': song_data['artist_popularity'] / 10,  # Scale to 0-10
        'track_popularity': song_data['track_popularity'] / 10,
        'danceability': audio['danceability'] * 10,
        'energy': audio['energy'] * 10,
        'valence': audio['valence'] * 10,
        'sentiment': (sentiment['positive'] - sentiment['negative'] + 1) * 5,  # Scale to 0-10
        'topic_relevance': topics['topic_score'],
        'complexity': complexity['complexity_score']
    }
    
    # Calculate weighted score
    weighted_scores = {name: score * weights[name] for name, score in component_scores.items()}
    final_score = sum(weighted_scores.values())
    
    # Scale to 0-100
    scaled_score = min(100, max(0, final_score * 10))
    
    return scaled_score, {
        'component_scores': component_scores,
        'weighted_scores': weighted_scores,
        'sentiment_analysis': sentiment,
        'topic_analysis': topics,
        'complexity_analysis': complexity
    }

def analyze_song(track_name, artist_name):
    """Main function to analyze a song for virality potential."""
    song_data, error = get_song_details(track_name, artist_name)
    if error:
        return {"error": error}
    
    virality_score, analysis_details = calculate_virality_score(song_data)
    
    result = {
        "track_name": song_data['track_name'],
        "artist_name": song_data['artist_name'],
        "virality_score": virality_score,
        "artist_popularity": song_data['artist_popularity'],
        "track_popularity": song_data['track_popularity'],
        "analysis": analysis_details
    }
    
    return result

if __name__ == "__main__":
    # Example usage
    track_name = input("Enter track name: ")
    artist_name = input("Enter artist name: ")
    
    result = analyze_song(track_name, artist_name)
    print(f"\nVirality Analysis for {result.get('track_name', track_name)} by {result.get('artist_name', artist_name)}")
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Virality Score: {result['virality_score']:.2f}/100")
        print(f"Artist Popularity: {result['artist_popularity']}/100")
        print(f"Track Popularity: {result['track_popularity']}/100")
        
        print("\nComponent Scores:")
        for component, score in result['analysis']['component_scores'].items():
            print(f"- {component}: {score:.2f}/10")
        
        if result['analysis']['topic_analysis']['topics']:
            print("\nViral Topics Detected:")
            for topic, count in result['analysis']['topic_analysis']['topics'].items():
                print(f"- {topic}: {count} occurrences")