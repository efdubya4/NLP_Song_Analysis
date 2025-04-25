import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import gensim
import nltk
from dotenv import load_dotenv


import os
import pandas as pd
from dotenv import load_dotenv
from modules.data_collection import SpotifyDataCollector, GeniusLyricFetcher
from modules.lyric_analysis import LyricAnalyzer
from modules.prediction import HitPredictor
from utils.helpers import format_features


# Initialize environment
load_dotenv()
nltk.download('vader_lexicon')

def main():
    # Initialize components
    data_collector = SpotifyDataCollector()
    lyric_analyzer = LyricAnalyzer()
    predictor = HitPredictor()
    
    # Example workflow
    print("Fetching top pop tracks...")
    pop_tracks = data_collector.get_top_tracks_by_genre('pop')
    
    # Analyze lyrics (in reality you'd fetch these from Genius API)
    print("Analyzing lyrics...")
    pop_tracks['sentiment'] = pop_tracks['lyrics'].apply(lyric_analyzer.analyze_sentiment)
    pop_tracks['themes'] = pop_tracks['lyrics'].apply(lyric_analyzer.extract_themes)
    
    # Prepare training data (simplified example)
    X = pop_tracks[['danceability', 'energy', 'tempo', 'valence']]
    y = (pop_tracks['popularity'] > 70).astype(int)  # Binary classification
    
    # Train model
    print("Training prediction model...")
    predictor.train_model(X, y)
    
    # Example prediction for a new song
    new_song_features = [0.85, 0.75, 120, 0.8]  # danceability, energy, tempo, valence
    prediction = predictor.predict(new_song_features)
    
    print(f"\nPrediction for new song:")
    print(f"Top chart probability: {prediction['probability_top_chart']:.2%}")
    print(f"Confidence: {prediction['confidence']:.2%}")

if __name__ == "__main__":
    main()