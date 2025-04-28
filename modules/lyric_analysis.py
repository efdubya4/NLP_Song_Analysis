import pandas as pd
from textblob import TextBlob
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
from nltk.corpus import stopwords
from collections import Counter
import re

nltk.download('stopwords')
nltk.download('vader_lexicon')

class LyricAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))
        self.theme_keywords = {
            'love': ['love', 'heart', 'baby', 'kiss', 'hold', 'touch'],
            'party': ['party', 'dance', 'night', 'club', 'fun', 'drink'],
            'breakup': ['break', 'hurt', 'pain', 'tears', 'leave'],
            'empowerment': ['strong', 'power', 'rise', 'fight', 'win', 'queen']
        }
    
    def add_analysis_features(self, df):
        """Add all lyric analysis features to dataframe"""
        if 'lyrics' not in df.columns:
            raise ValueError("DataFrame must contain 'lyrics' column")
        
        # Sentiment Analysis
        sentiment = df['lyrics'].apply(self._get_sentiment)
        df = pd.concat([df, sentiment], axis=1)
        
        # Theme Detection
        for theme in self.theme_keywords:
            df[f'theme_{theme}'] = df['lyrics'].apply(
                lambda x: self._detect_theme(x, theme)
            ).astype(int)
        
        # Basic Text Statistics
        df['word_count'] = df['lyrics'].apply(
            lambda x: len(x.split()) if pd.notna(x) else 0
        )
        df['unique_words'] = df['lyrics'].apply(
            lambda x: len(set(word.lower() for word in x.split())) 
            if pd.notna(x) else 0
        )
        
        return df
    
    def _get_sentiment(self, text):
        """Comprehensive sentiment analysis"""
        if not text or pd.isna(text):
            return {
                'sentiment_compound': 0,
                'sentiment_positive': 0,
                'sentiment_negative': 0,
                'textblob_polarity': 0,
                'textblob_subjectivity': 0
            }
        
        # VADER Sentiment
        vader = self.sia.polarity_scores(text)
        
        # TextBlob Sentiment
        blob = TextBlob(text)
        
        return {
            'sentiment_compound': vader['compound'],
            'sentiment_positive': vader['pos'],
            'sentiment_negative': vader['neg'],
            'textblob_polarity': blob.sentiment.polarity,
            'textblob_subjectivity': blob.sentiment.subjectivity
        }
    
    def _detect_theme(self, text, theme):
        """Basic topic modeling (expand with proper NLP models)"""
        if not text or theme not in self.theme_keywords:
            return 0
        
        keywords = self.theme_keywords[theme]
        words = re.findall(r'\w+', text.lower())
        return 1 if any(keyword in words for keyword in keywords) else 0
    
    def get_top_words(self, lyrics, n=10):
        """Get most frequent non-stopwords"""
        if not lyrics:
            return []
        
        words = [word.lower() for word in lyrics.split() 
                if word.lower() not in self.stop_words and word.isalpha()]
        return [word for word, count in Counter(words).most_common(n)]
