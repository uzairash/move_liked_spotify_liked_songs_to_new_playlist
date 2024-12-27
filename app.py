import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Replace these with your Spotify Developer App credentials
CLIENT_ID = "ec15dd15cafc4e4aa067e5a00895852d"
CLIENT_SECRET = "0556acc8a2534e36ba07aee5907f9964"
REDIRECT_URI = "http://localhost:8888/callback"

# Spotify scopes
SCOPES = "playlist-modify-private playlist-read-private user-library-read"


def authenticate_spotify():
    # Set up authentication manager
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPES
    )
    
    # Get the authorization URL
    auth_url = auth_manager.get_authorize_url()
    print("Visit the following URL to authorize:")
    print(auth_url)
    
    # Prompt user to paste the code after authorization
    code = input("Enter the code from the URL after authorization: ")
    
    # Exchange the code for an access token
    token_info = auth_manager.get_access_token(code=code)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    return sp

def get_liked_songs(sp):
    liked_songs = []
    results = sp.current_user_saved_tracks()
    while results:
        for item in results['items']:
            track = item['track']
            liked_songs.append(track['id'])  # Store track IDs
        results = sp.next(results) if results['next'] else None
    return liked_songs

def create_playlist(sp, name="from liked songs", public=False):
    user_id = sp.me()['id']
    playlist = sp.user_playlist_create(user_id, name, public)
    return playlist['id']

def add_songs_to_playlist(sp, playlist_id, track_ids):
    for i in range(0, len(track_ids), 100):  # Spotify allows max 100 tracks per request
        sp.playlist_add_items(playlist_id, track_ids[i:i+100])

if __name__ == "__main__":
    # Authenticate with Spotify
    sp = authenticate_spotify()

    # Fetch liked songs
    print("Fetching liked songs...")
    liked_songs = get_liked_songs(sp)
    print(f"Found {len(liked_songs)} liked songs.")

    # Create a new playlist
    print("Creating a new playlist...")
    playlist_id = create_playlist(sp)
    print(f"Playlist created with ID: {playlist_id}")

    # Add liked songs to the playlist
    print("Adding songs to the playlist...")
    add_songs_to_playlist(sp, playlist_id, liked_songs)
    print("All liked songs have been added to the playlist!")