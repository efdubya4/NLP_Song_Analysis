import os
import ssl
import pandas as pd
from dotenv import load_dotenv
from modules.data_collection import AcousticBrainzCollector
from modules.lyric_analysis import LyricAnalyzer
from modules.prediction import HitPredictor
from modules.lyric_fetcher import GeniusLyricFetcher
from modules.spotify_integration import SpotifyCollector
from utils.helpers import format_features
import nltk
from textwrap import fill

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

def print_analysis(song_data, index=None):
    """Formatted printout for song analysis"""
    title = song_data['title']
    artist = song_data['artist']
    lyrics_preview = fill(song_data['lyrics'][:150] + "...", width=70) if isinstance(song_data.get('lyrics'), str) else "No lyrics available"
    
    print(f"\n\033[1m{title}\033[0m by {artist}")
    print("═" * (len(title) + len(artist) + 5))
    print(f"\n\033[4mLyrics Preview:\033[0m\n{lyrics_preview}")
    
    # Sentiment Analysis
    print("\n\033[1;36mSentiment Analysis Results:\033[0m")
    print(f"• Compound Sentiment: {song_data['sentiment_compound']:.2f} (range: -1 to 1)")
    print(f"• Positive Sentiment: {song_data['sentiment_positive']:.2f}")
    print(f"• Negative Sentiment: {song_data['sentiment_negative']:.2f}")
    print(f"• TextBlob Polarity: {song_data['textblob_polarity']:.2f} (emotional tone)")
    print(f"• TextBlob Subjectivity: {song_data['textblob_subjectivity']:.2f} (0 = factual, 1 = opinionated)")
    
    # Detected Themes
    themes = [theme.replace('theme_', '') 
             for theme, detected in song_data.items() 
             if theme.startswith('theme_') and detected == 1]
    if themes:
        print("\n\033[1;35mDetected Themes:\033[0m")
        for theme in themes:
            print(f"- {theme.capitalize()}")
    else:
        print("\n\033[1;35mNo strong themes detected\033[0m")
    
    # Text Statistics
    print("\n\033[1;34mText Statistics:\033[0m")
    print(f"• Word Count: {song_data.get('word_count', 0)}")
    print(f"• Unique Words: {song_data.get('unique_words', 0)}")
    print("═" * (len(title) + len(artist) + 5))


def main():
    # Initialize components
    collector = AcousticBrainzCollector()
    spotify_collector = SpotifyCollector()
    lyric_analyzer = LyricAnalyzer()
    # predictor = HitPredictor()
    
    # Configuration
    DATA_SOURCE = "AcousticBrainz"
    TARGET_GENRE = "pop"
    TRACK_LIMIT = 3
    
    print(f"\nFetching {TARGET_GENRE} tracks from AcousticBrainz...")
    tracks_df = collector.get_top_tracks_by_genre(TARGET_GENRE, limit=9)
    
    if tracks_df.empty:
        print("Error: No tracks fetched from AcousticBrainz")
        return

    print(f"Fetched {len(tracks_df)} tracks. Starting lyric analysis...")
    # if DATA_SOURCE == "spotify":
    #     tracks_df = spotify_collector.get_tracks(
    #         genre=TARGET_GENRE,
    #         limit=TRACK_LIMIT
    #     )
    # else:
    #     tracks_df = collector.get_top_tracks_by_genre(
    #         genre=TARGET_GENRE,
    #         limit=TRACK_LIMIT
    #     )
    
    if tracks_df.empty:
        print("\033[1;31mError: No tracks fetched\033[0m")
        return

    print(f"\033[1;32mSuccessfully fetched {len(tracks_df)} tracks\033[0m")
    
    # Lyric Fetching
    print("\nFetching lyrics from Genius...")
    tracks_df = collector.add_lyrics_to_dataframe(tracks_df)
    success_count = tracks_df['lyrics'].notna().sum()
    print(f"Successfully fetched lyrics for {success_count}/{len(tracks_df)} tracks")

    # Lyric Analysis
    print("\nAnalyzing lyrics...")
    analyzed_df = lyric_analyzer.analyze(tracks_df)

    #Print results
    for idx, song in analyzed_df.iterrows():
        print_analysis(song)
    
    # Select only sentiment and theme columns
    # output_columns = ['title', 'artist'] + [
    #     col for col in analyzed_df.columns 
    #     if col.startswith(('sentiment_', 'textblob_', 'theme_'))
    # ]
    
    # Save results
    analyzed_df.to_csv('lyric_analysis_results.csv', index=False)
    print("\nResults saved to 'lyric_analysis_results.csv'")

if __name__ == "__main__":
    main()