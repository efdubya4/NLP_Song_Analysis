import pandas as pd
import requests
import lyricsgenius
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import os

# Initialize APIs
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='f6a5a0fa696441128c0e5bd3d7667c67',
    client_secret='e23e2595e1a1423d86809db56c95dc5c'
))
genius = lyricsgenius.Genius('5fW2U8JpJkvXr-LqEl6qc8NeSM2epwuppNsO_bisvXnjLESDlXWyWV-0-9OKqY0R')

ACOUSTICBRAINZ_API = "https://acousticbrainz.org/api/v1/"

def get_acoustic_features(mbid):
    """Get audio features from AcousticBrainz using MusicBrainz ID"""
    try:
        response = requests.get(f"{ACOUSTICBRAINZ_API}{mbid}/high-level", timeout=10)
        if response.status_code == 200:
            return response.json()
        print(f"AcousticBrainz API returned {response.status_code}")
        return None
    except Exception as e:
        print(f"Error getting AcousticBrainz data: {e}")
        return None

def get_track_data(artist_name, track_name):
    """Get combined data from Spotify and AcousticBrainz for a single track"""
    print(f"Fetching data for {artist_name} - {track_name}...")
    
    # Get Spotify metadata
    try:
        results = sp.search(q=f'artist:{artist_name} track:{track_name}', type='track', limit=1)
        if not results['tracks']['items']:
            print("Track not found on Spotify")
            return None
        
        track = results['tracks']['items'][0]
        print(f"Found Spotify track: {track['name']} (Popularity: {track['popularity']})")
    except Exception as e:
        print(f"Spotify API error: {e}")
        return None
    
    # Try to get MusicBrainz ID
    mbid = None
    try:
        artist_info = sp.artist(track['artists'][0]['id'])
        mbid = artist_info.get('external_ids', {}).get('musicbrainz')
        if mbid:
            print(f"Found MusicBrainz ID: {mbid}")
        else:
            print("No MusicBrainz ID found")
    except Exception as e:
        print(f"Couldn't get MusicBrainz ID: {str(e)}")
    
    # Get audio features from AcousticBrainz
    features = {}
    if mbid:
        ab_data = get_acoustic_features(mbid)
        if ab_data:
            print("Successfully retrieved AcousticBrainz data")
            features = {
                'tempo': ab_data.get('rhythm', {}).get('bpm'),
                'danceability': ab_data.get('rhythm', {}).get('danceability'),
                'energy': ab_data.get('highlevel', {}).get('energy', {}).get('value'),
                'valence': ab_data.get('highlevel', {}).get('valence', {}).get('value'),
                'acousticness': ab_data.get('highlevel', {}).get('acoustic', {}).get('value'),
                'genre': ab_data.get('highlevel', {}).get('genre', {}).get('value'),
                'mood': ab_data.get('highlevel', {}).get('mood', {}).get('value'),
            }
        else:
            print("No AcousticBrainz data available")
    else:
        print("No MusicBrainz ID available - skipping AcousticBrainz")
    
    # Get lyrics from Genius
    lyrics = None
    try:
        song = genius.search_song(track_name, artist_name)
        if song:
            lyrics = song.lyrics
            print("Successfully retrieved lyrics")
        else:
            print("Lyrics not found on Genius")
    except Exception as e:
        print(f"Genius API error: {e}")
    
    # Compile all data
    track_data = {
        'spotify_id': track['id'],
        'mbid': mbid,
        'name': track['name'],
        'artist': track['artists'][0]['name'],
        'album': track['album']['name'],
        'release_date': track['album']['release_date'],
        'duration_ms': track['duration_ms'],
        'popularity': track['popularity'],
        **features,
        'lyrics': lyrics
    }
    
    return track_data

def analyze_track(track_data):
    """Display analysis of the track"""
    if not track_data:
        print("No data available for analysis")
        return
    
    print("\n == ANALYSIS RESULTS ==")
    print(f"{track_data['artist']} - {track_data['name']}")
    print(f"Album: {track_data['album']} ({track_data['release_date'][:4]})")
    print(f"Duration: {int(track_data['duration_ms']/60000):.2f} minutes")
    print(f"Popularity: {track_data['popularity']}/100")
    
    if track_data.get('tempo'):
        print("\n🎶 AUDIO FEATURES:")
        print(f"• Tempo: {track_data['tempo']} BPM")
        print(f"• Danceability: {track_data.get('danceability', 'N/A')}")
        print(f"• Energy: {track_data.get('energy', 'N/A')}")
        print(f"• Valence: {track_data.get('valence', 'N/A')} (musical positiveness)")
        print(f"• Acousticness: {track_data.get('acousticness', 'N/A')}")
        print(f"• Genre: {track_data.get('genre', 'N/A')}")
        print(f"• Mood: {track_data.get('mood', 'N/A')}")
    else:
        print("\nℹ️ No audio features available")
    
    if track_data.get('lyrics'):
        print("\nLYRICS EXCERPT:")
        print(track_data['lyrics'][:200].replace('\n', ' ') + "...")
    else:
        print("\nℹ️ No lyrics available")
# def process_acousticbrainz_dataset(directory):
#     """Process bulk downloaded AcousticBrainz data"""
#     features_list = []
    
#     for filename in os.listdir(directory):
#         if filename.endswith('.json'):
#             with open(os.path.join(directory, filename)) as f:
#                 data = json.load(f)
                
#                 features = {
#                     'mbid': filename.replace('.json', ''),
#                     'tempo': data.get('rhythm', {}).get('bpm'),
#                     'danceability': data.get('rhythm', {}).get('danceability'),
#                     'energy': data.get('highlevel', {}).get('energy', {}).get('value'),
#                     'valence': data.get('highlevel', {}).get('valence', {}).get('value'),
#                     'acousticness': data.get('highlevel', {}).get('acoustic', {}).get('value'),
#                     'genre': data.get('highlevel', {}).get('genre', {}).get('value'),
#                     'mood': data.get('highlevel', {}).get('mood', {}).get('value'),
#                 }
#                 features_list.append(features)
    
#     return pd.DataFrame(features_list)

def main():
    # Example: Get data for Sade - Cherish the Day
    artist = "The Lady in My Life"
    track = "Michael Jackson"
    
    # Get single track data
    track_data = get_track_data(artist, track)
    
    if track_data:
        # Create DataFrame from single track
        spotify_df = pd.DataFrame([track_data])
        spotify_df.to_csv(f'{artist}_{track}_analysis.csv', index=False)

        analyze_track(track_data)
    else:
        print("Failed to retrieve track data")


        # If you have bulk AcousticBrainz data, merge it
        # if os.path.exists('acousticbrainz_data/'):
    #         ab_df = process_acousticbrainz_dataset('acousticbrainz_data/')
    #         merged_df = pd.merge(spotify_df, ab_df, on='mbid', how='left')
            
    #         # Save results
    #         merged_df.to_csv(f'{artist}_{track}_analysis.csv', index=False)
    #         print(f"\nAnalysis saved to {artist}_{track}_analysis.csv")
            
    #         # Print summary
    #         print("\n=== Analysis Summary ===")
    #         print(f"Artist: {track_data['artist']}")
    #         print(f"Track: {track_data['name']}")
    #         print(f"Album: {track_data['album']}")
    #         print(f"Release Date: {track_data['release_date']}")
    #         print(f"Tempo: {track_data.get('tempo', 'N/A')} BPM")
    #         print(f"Energy: {track_data.get('energy', 'N/A')}")
    #         print(f"Valence: {track_data.get('valence', 'N/A')}")
    #         print(f"Genre: {track_data.get('genre', 'N/A')}")
    #         print(f"Mood: {track_data.get('mood', 'N/A')}")
    #         print(f"Lyrics snippet: {track_data['lyrics'][:100] if track_data['lyrics'] else 'N/A'}...")
    #     else:
    #         print("\nNo AcousticBrainz bulk data directory found - using API data only")
    #         spotify_df.to_csv('sade_cherish_the_day_analysis.csv', index=False)
    # else:
    #     print("\nFailed to retrieve track data")

if __name__ == "__main__":
    main()