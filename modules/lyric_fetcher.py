import os
import requests
from dotenv import load_dotenv
import re
from bs4 import BeautifulSoup
from typing import Optional
import lyricsgenius

load_dotenv()

class GeniusLyricFetcher:
    def __init__(self):
        self.base_url = "https://api.genius.com"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('GENIUS_ACCESS_TOKEN')}",
            "User-Agent": "Mozilla/5.0"  # Some APIs require user-agent
        }
        # Initialize session properly
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.timeout = 10  # seconds

        self.genius = lyricsgenius.Genius(
        os.getenv("GENIUS_ACCESS_TOKEN"),
        verbose=False,
        remove_section_headers=True
        )
    
    def get_lyrics(self, song_title: str, artist_name: str) -> Optional[str]:
        """Main method to fetch lyrics with multiple fallbacks"""
        try:
            # Clean inputs first
            clean_title = self._clean_string(song_title)
            clean_artist = self._clean_string(artist_name)
            
            print(f"Fetching lyrics for: {clean_title} by {clean_artist}")
            
            # Try API first
            lyrics = self._get_via_api(clean_title, clean_artist)
            if lyrics:
                return lyrics
                
            # Fallback to web scraping
            return self._get_via_web_scraping(clean_title, clean_artist)
            
        except Exception as e:
            print(f"Failed to get lyrics for {song_title}: {str(e)}")
            return None
    
    def _get_via_api(self, title: str, artist: str) -> Optional[str]:
        """Official Genius API method"""
        try:
            song = self.genius.search_song(title, artist)
            if not song:
                return None

            raw_lyrics = song.lyrics

            # Step 1: Remove everything before the first actual lyric line
            if 'Lyrics' in raw_lyrics:
                raw_lyrics = raw_lyrics.split('Lyrics', 1)[1]
            
            # Step 2: Remove lines in brackets, like [Verse 1], [Chorus], etc.
            lyrics_no_brackets = re.sub(r'\[.*?\]', '', raw_lyrics)

            # Step 3: Remove any non-lyrical metadata (e.g., contributor counts, descriptions)
            lyrics_lines = lyrics_no_brackets.splitlines()
            clean_lyrics = [line.strip() for line in lyrics_lines if line.strip() and not re.match(r'^\d+ Contributors|Translations|Read More', line)]

            return "\n".join(clean_lyrics)

            # # Search for the song
            # search_url = f"{self.base_url}/search"
            # response = self.session.get(
            #     search_url,
            #     params={'q': f"{title} {artist}"},
            #     timeout=self.timeout
            # )
            # response.raise_for_status()
            
            # # Parse results
            # hits = response.json().get('response', {}).get('hits', [])
            # if not hits:
            #     return None
                
            # # Get the first matching song
            # song_path = hits[0]['result']['api_path']
            # song_url = f"{self.base_url}{song_path}"
            
            # # Fetch lyrics
            # song_response = self.session.get(song_url, timeout=self.timeout)
            # song_response.raise_for_status()
            
            # return song_response.json().get('response', {}).get('song', {}).get('lyrics', {}).get('plain')
            
        except Exception as e:
            print(f"API method failed: {str(e)}")
            return None
    
    def _get_via_web_scraping(self, title: str, artist: str) -> Optional[str]:
        """Fallback web scraping method"""
        print("Fallback web scraping method...")
        return None
        # # try:
        # #     # Search Genius website
        # #     search_term = f"{title} {artist}".replace(' ', '+')
        # #     search_url = f"https://genius.com/api/search/multi?q={search_term}"
            
        # #     response = self.session.get(search_url, timeout=self.timeout)
        # #     response.raise_for_status()
            
        # #     # Find first song result
        # #     results = response.json().get('response', {}).get('sections', [{}])[0].get('hits', [])
        # #     if not results:
        # #         return None
                
        # #     song_url = results[0].get('result', {}).get('url')
        # #     if not song_url:
        # #         return None
                
        # #     # Fetch lyrics page
        # #     page_response = self.session.get(song_url, timeout=self.timeout)
        # #     page_response.raise_for_status()
            
        # #     # Parse with BeautifulSoup
        # #     soup = BeautifulSoup(page_response.text, 'html.parser')
        # #     lyrics_div = soup.find('div', {'data-lyrics-container': 'true'})
            
        # #     if lyrics_div:
        # #         # Clean up the lyrics
        # #         for br in lyrics_div.find_all('br'):
        # #             br.replace_with('\n')
        # #         for a in lyrics_div.find_all('a'):
        # #             a.unwrap()
        # #         return lyrics_div.get_text('\n').strip()
                
        # #     return None
            
        # except Exception as e:
        #     print(f"Web scraping failed: {str(e)}")
        #     return None
    
    def _clean_string(self, text: str) -> str:
        """Clean song/artist names for searching"""
        if not text:
            return ""
            
        # Remove content in parentheses/brackets
        text = re.sub(r'[\(\[].*?[\)\]]', '', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r"[^\w\s'\-]", '', text)
        # Collapse multiple spaces
        text = re.sub(r'\s+', ' ', text)
        return text.strip()