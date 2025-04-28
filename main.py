import os
import ssl
import pandas as pd
from dotenv import load_dotenv
from modules.data_collection import AcousticBrainzCollector
from modules.lyric_analysis import LyricAnalyzer
from modules.prediction import HitPredictor
from modules.lyric_fetcher import GeniusLyricFetcher
from utils.helpers import format_features
import nltk


# Fix SSL certificate issues
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download NLTK data
nltk.download('stopwords')
nltk.download('vader_lexicon')

load_dotenv()

def main():
    # Initialize components
    collector = AcousticBrainzCollector()
    lyric_analyzer = LyricAnalyzer()
    predictor = HitPredictor()
    
       # Configuration
    TARGET_GENRE = "rock"
    TRAIN_MODEL = True
    
    # Data Collection
    print(f"\nFetching top {TARGET_GENRE} tracks from Spotify...")
    tracks_df = collector.get_top_tracks_by_genre(TARGET_GENRE, limit=25)
    
    if tracks_df.empty:
        print("Error: No tracks fetched from Spotify")
        return

    print(f"Fetched {len(tracks_df)} tracks. Starting lyric analysis...")


    # Lyric Fetching
    print("\nFetching lyrics from Genius...")
    tracks_df = collector.add_lyrics_to_dataframe(tracks_df)

    # Show success rate
    success_count = tracks_df['lyrics'].notna().sum()
    print(f"Successfully fetched lyrics for {success_count}/{len(tracks_df)} tracks")

    
    # Feature Engineering
    print("\nAnalyzing tracks...")
    tracks_df = lyric_analyzer.add_analysis_features(tracks_df)
    
    # Prepare training data
    features = [
        'danceability', 'energy', 'tempo', 'valence',
        'sentiment_compound', 'theme_love'
    ]
    X = tracks_df[features]
    y = (tracks_df['popularity'] > 70).astype(int)  # Binary classification
    
    # Model Training
    if TRAIN_MODEL and not X.empty:
        print("\nTraining prediction model...")
        predictor.train_model(X, y)
    
    # Example Prediction
    print("\nMaking sample prediction...")
    new_song = {
        'danceability': 0.85,
        'energy': 0.75,
        'tempo': 122,
        'valence': 0.8,
        'lyrics': "I'm feeling good tonight, gonna dance until the morning light"
    }
    new_features = lyric_analyzer.analyze_single_song(new_song)
    formatted_features = format_features(new_features, features)
    prediction = predictor.predict(list(new_features.values()))
    
    # Display Results
    print("\n=== Prediction Results ===")
    print(f"Top Chart Probability: {prediction['probability_top_chart']:.2%}")
    print(f"Confidence: {prediction['confidence']:.2%}")
    print("\nKey Features:")
    for feat, val in zip(features, formatted_features):
        print(f"{feat:>20}: {val:.2f}")

if __name__ == "__main__":
    main()