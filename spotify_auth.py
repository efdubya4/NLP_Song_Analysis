import spotipy
from spotipy.oauth2 import SpotifyPKCE
import os
import base64
import hashlib
import secrets
import string
from dotenv import load_dotenv
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
from threading import Thread
import json
import time
import requests
import sys

def generate_code_verifier(length=64):
    """Generate a random code verifier string for PKCE"""
    possible = string.ascii_letters + string.digits + '-._~'
    return ''.join(secrets.choice(possible) for _ in range(length))

def generate_code_challenge(verifier):
    """Generate a code challenge from the verifier using SHA256"""
    sha256_hash = hashlib.sha256(verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(sha256_hash).decode().replace('=', '')
    return code_challenge

class TokenManager:
    """Manage Spotify access and refresh tokens"""
    def __init__(self, client_id):
        self.client_id = client_id
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = None
        
    def set_tokens(self, access_token, refresh_token, expires_in):
        """Store new tokens and calculate expiry time"""
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expiry = time.time() + expires_in
        
    def is_token_expired(self):
        """Check if the current access token is expired"""
        if not self.token_expiry:
            return True
        return time.time() > self.token_expiry
    
    async def refresh_access_token(self):
        """Get new access token using refresh token"""
        if not self.refresh_token:
            raise Exception("No refresh token available")
            
        try:
            url = "https://accounts.spotify.com/api/token"
            payload = {
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
                'client_id': self.client_id
            }
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            response = requests.post(url, data=payload, headers=headers)
            response.raise_for_status()
            token_info = response.json()
            
            self.access_token = token_info['access_token']
            # Some responses may include a new refresh token
            if 'refresh_token' in token_info:
                self.refresh_token = token_info['refresh_token']
            self.token_expiry = time.time() + token_info['expires_in']
            
            return self.access_token
            
        except Exception as e:
            raise Exception(f"Failed to refresh token: {str(e)}")

class SpotifyAuthHandler(BaseHTTPRequestHandler):
    """Handle the OAuth callback"""
    def do_GET(self):
        query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        
        if 'code' in query_components:
            self.server.auth_code = query_components['code'][0]
            response = """
            <html><body>
                <h1>Authentication Successful!</h1>
                <p>You can close this window.</p>
            </body></html>
            """
        else:
            self.server.auth_code = None
            response = """
            <html><body>
                <h1>Authentication Failed!</h1>
                <p>Please try again.</p>
            </body></html>
            """
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(response.encode())

def get_spotify_client():
    """Create authenticated Spotify client using PKCE flow"""
    load_dotenv()
    
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI', 'http://127.0.0.1:9090/callback')
    scope = os.getenv('SPOTIFY_SCOPES', 'playlist-read-private playlist-read-collaborative')
    
    if not client_id:
        raise Exception("Missing Spotify client ID in .env file")
    
    server = None
    try:
        # Initialize PKCE auth flow
        auth = SpotifyPKCE(
            client_id=client_id,
            redirect_uri=redirect_uri,
            scope=scope,
            open_browser=True
        )
        
        # Start local server to handle the callback
        server = HTTPServer(('127.0.0.1', 9090), SpotifyAuthHandler)
        server.auth_code = None
        server_thread = Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        # Open browser for user authorization
        auth_url = auth.get_authorize_url()
        webbrowser.open(auth_url)
        
        # Wait for the callback
        timeout = 300  # 5 minutes timeout
        start_time = time.time()
        while server.auth_code is None:
            if time.time() - start_time > timeout:
                raise Exception("Authentication timed out")
            time.sleep(0.1)
        
        # Get access token using the auth code
        auth.get_access_token(server.auth_code, check_cache=False)
        
        # Create Spotify client with auth manager
        spotify = spotipy.Spotify(auth_manager=auth)
        
        # Test the connection
        user = spotify.current_user()
        print(f"Successfully authenticated as: {user['display_name']}")
        return spotify
        
    except Exception as e:
        print("\nDebug Information:")
        print(f"Client ID: {client_id[:5]}...")
        print(f"Redirect URI: {redirect_uri}")
        print(f"Scope: {scope}")
        raise Exception(f"Spotify authentication failed: {str(e)}")
        
    finally:
        if server:
            server.shutdown()
            server.server_close()

if __name__ == "__main__":
    try:
        spotify = get_spotify_client()
        print("Authentication successful!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)