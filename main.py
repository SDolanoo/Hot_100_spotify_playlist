import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ################################GET TITLES######################################

travel_date = "2012-04-21"  # input("What your would you like to travel(YYYY-MM-DD): ")
year = travel_date[0:4:]

response = requests.get(f"https://www.billboard.com/charts/hot-100/{travel_date}/#")
billboard_website = response.text

soup = BeautifulSoup(billboard_website, "html.parser")

titles = [name.getText().strip() for name in soup.select(".a-no-trucate")][::2]

# ###########################SPOTIFY##############################

SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
SPOTIFY_MY_USERNAME = os.environ.get("MY_USERNAME")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri='http://example.com',
        username=SPOTIFY_MY_USERNAME,
        show_dialog=True,
        cache_path=".cache-spotify"))

user_id = sp.current_user()['id']

uris = [sp.search(title)['tracks']['items'][0]['uri'] for title in titles]

PLAYLIST_ID = sp.user_playlist_create(user=SPOTIFY_MY_USERNAME,
                                      name=f'HOT 100 OF {year}',
                                      public=False,
                                      description="Playlist created using python")['id']

sp.user_playlist_add_tracks(playlist_id=PLAYLIST_ID, tracks=uris, user=user_id)
