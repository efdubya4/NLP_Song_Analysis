import pandas as pd
import requests
import lyricsgenius
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import os

class LyricAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        
    def analyze_sentiment(self, text):
        """Analyze sentiment using VADER and TextBlob"""
        if not text or pd.isna(text):
            return None
            
        vader_scores = self.sia.polarity_scores(text)
        blob = TextBlob(text)
        
        return {
            'vader_compound': vader_scores['compound'],
            'vader_positive': vader_scores['pos'],
            'vader_negative': vader_scores['neg'],
            'textblob_polarity': blob.sentiment.polarity,
            'textblob_subjectivity': blob.sentiment.subjectivity
        }
    
    def extract_themes(self, lyrics, n_topics=3):
        """Basic topic modeling (expand with proper NLP models)"""
        if not lyrics:
            return []
            
        # Tokenize and simple cleaning
        words = [word.lower() for word in lyrics.split() 
                if word.isalpha() and len(word) > 2]
        
        # In a real implementation, you'd use LDA or similar here
        # This is a simplified placeholder
        common_themes = {
            'love': ['love', 'heart', 'baby', 'kiss', 'hold'],
            'party': ['dance', 'night', 'club', 'fun', 'drink'],
            'empowerment': ['strong', 'power', 'rise', 'fight', 'win']
        }
        
        detected_themes = []
        for theme, keywords in common_themes.items():
            if any(keyword in words for keyword in keywords):
                detected_themes.append(theme)
                
        return detected_themes if detected_themes else ['other']