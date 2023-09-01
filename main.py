import spotipy
from bs4 import BeautifulSoup
import requests
from spotipy.oauth2 import SpotifyOAuth
import os

URL = "https://www.billboard.com/charts/hot-100/"
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
REDIRECT_URI = "http://example.com"

########################## Billboard web scrape #########################################################
# Get date for playlist
print("Welcome to the playlist maker. Enter a date and I'll make a top 100 songs playlist on Spotify from that week.")
input_date = input("Enter a date in this format YYYY-MM-DD: ")

# Scrape data
response = requests.get(f"{URL}/{input_date}").text
soup = BeautifulSoup(response, "html.parser")

# Create list of artist and song names
song_names = [name.find(name="h3", class_="c-title").getText().replace("\n", "").replace("\t", "") for
              name in soup.find_all(name="ul", class_="o-chart-results-list-row")]
artist_names = [
    name.find(name="span", class_="a-no-trucate").getText().replace("\n", "").replace("\t", "") for
    name in soup.find_all(name="ul", class_="o-chart-results-list-row")]
print(song_names)
print(artist_names)

#################################### Spotify ###########################################################
# Authenticate
SPOTIFY_ENDPOINT = "https://api.spotify.com/v1/users/"
scope = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                              client_secret=CLIENT_SECRET,
                              redirect_uri=REDIRECT_URI,
                              scope="playlist-modify-private"))

# Get user id and create playlist
user_id = sp.current_user()["id"]
playlist = sp.user_playlist_create(user=user_id, public=False, name=f"{input_date} Top Hits")

# Get song id of all songs in top 100 list
track_list = []
for x in range(len(artist_names)):
    song_data = sp.search(f"{artist_names[x]} {song_names[x]}", limit=1)
    #song_data = sp.search(f"%track:{song_names[x]}%artist:{artist_names[x]}")
    song_id = song_data["tracks"]["items"][0]["id"]
    track_list.append(song_id)


# # Add songs to playlist
list_id = playlist["id"]
sp.playlist_add_items(playlist_id=list_id, items=track_list)

