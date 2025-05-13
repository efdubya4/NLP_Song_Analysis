import os
import librosa
import speech_recognition as sr
from pydub import AudioSegment
import numpy as np
from song_analysis import analyze_lyrics_sentiment, analyze_lyrics_topics, analyze_lyrics_complexity, calculate_virality_score

class AudioAnalyzer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def convert_to_wav(self, audio_path):
        """Convert any audio file to WAV format."""
        try:
            audio = AudioSegment.from_file(audio_path)
            wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
            audio.export(wav_path, format='wav')
            return wav_path
        except Exception as e:
            print(f"Error converting audio: {str(e)}")
            return None

    def extract_lyrics(self, audio_path):
        """Extract lyrics from audio file using speech recognition."""
        try:
            # Convert to WAV if needed
            if not audio_path.endswith('.wav'):
                audio_path = self.convert_to_wav(audio_path)
                if not audio_path:
                    return None

            # Load audio file
            with sr.AudioFile(audio_path) as source:
                audio = self.recognizer.record(source)
                
            # Perform speech recognition
            lyrics = self.recognizer.recognize_google(audio)
            return lyrics
            
        except Exception as e:
            print(f"Error extracting lyrics: {str(e)}")
            return None

    def analyze_audio_features(self, audio_path):
        """Extract audio features using librosa."""
        try:
            # Load audio file
            y, sr = librosa.load(audio_path)
            
            # Extract features
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            zero_crossing_rate = librosa.feature.zero_crossing_rate(y)[0]
            
            # Calculate energy and danceability approximations
            energy = np.mean(librosa.feature.rms(y=y)[0])
            
            # Normalize values
            features = {
                'danceability': min(tempo / 200, 1.0),  # Rough approximation
                'energy': min(energy * 10, 1.0),
                'valence': np.mean(spectral_centroids) / np.max(spectral_centroids),  # Rough approximation
                'tempo': tempo
            }
            
            return features
            
        except Exception as e:
            print(f"Error analyzing audio: {str(e)}")
            return None

def analyze_audio_file(file_path):
    """Main function to analyze an audio file."""
    analyzer = AudioAnalyzer()
    
    # Extract lyrics
    lyrics = analyzer.extract_lyrics(file_path)
    if not lyrics:
        return {"error": "Could not extract lyrics from audio"}
    
    # Get audio features
    audio_features = analyzer.analyze_audio_features(file_path)
    if not audio_features:
        return {"error": "Could not analyze audio features"}
    
    # Create song data structure similar to Spotify API
    song_data = {
        'track_name': os.path.basename(file_path),
        'artist_name': 'Unknown',  # Could be enhanced with audio fingerprinting
        'artist_popularity': 50,  # Default values
        'track_popularity': 50,
        'audio_features': audio_features,
        'lyrics': lyrics,
        'cleaned_lyrics': lyrics  # You might want to use your clean_lyrics function here
    }
    
    # Calculate virality score using existing functions
    virality_score, analysis_details = calculate_virality_score(song_data)
    
    result = {
        "track_name": song_data['track_name'],
        "artist_name": song_data['artist_name'],
        "virality_score": virality_score,
        "lyrics": lyrics,
        "audio_features": audio_features,
        "analysis": analysis_details
    }
    
    return result

if __name__ == "__main__":
    file_path = input("Enter path to audio file: ")
    
    if not os.path.exists(file_path):
        print("Error: File not found")
    else:
        result = analyze_audio_file(file_path)
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"\nAudio Analysis Results:")
            print(f"Track: {result['track_name']}")
            print(f"Virality Score: {result['virality_score']:.2f}/100")
            
            print("\nAudio Features:")
            for feature, value in result['audio_features'].items():
                print(f"- {feature}: {value:.2f}")
            
            print("\nComponent Scores:")
            for component, score in result['analysis']['component_scores'].items():
                print(f"- {component}: {score:.2f}/10")
            
            if result['analysis']['topic_analysis']['topics']:
                print("\nViral Topics Detected:")
                for topic, count in result['analysis']['topic_analysis']['topics'].items():
                    print(f"- {topic}: {count} occurrences")