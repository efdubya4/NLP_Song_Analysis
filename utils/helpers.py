import numpy as np
import re

def format_features(feature_dict, required_features):
    """
    Formats a dictionary of features into the correct order for model prediction
    
    Args:
        feature_dict (dict): Dictionary containing all extracted features
        required_features (list): List of features the model expects, in order
        
    Returns:
        list: Features in the correct order for model prediction
    """
    return [feature_dict.get(feat, 0) for feat in required_features]

def normalize_tempo(tempo):
    """Normalize tempo (BPM) to 0-1 scale assuming typical range of 60-180 BPM"""
    return (np.clip(tempo, 60, 180) - 60) / 120

def clean_lyrics(text):
    """Basic lyric cleaning function"""
    if not text:
        return ""
    
    # Remove content in brackets (like [Verse 1])
    text = re.sub(r'\[.*?\]', '', text)
    # Remove special characters but keep apostrophes
    text = re.sub(r"[^a-zA-Z' ]", '', text)
    return text.strip()

def log_transform(value, offset=1):
    """Apply log transformation to skewed features"""
    return np.log(value + offset)