import discogs_client
import requests
from flask import jsonify
import os
import time
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = None
TOKEN_EXPIRES_AT = 0

def get_igdb_token():
    global ACCESS_TOKEN, TOKEN_EXPIRES_AT
    # Check if token is valid
    if ACCESS_TOKEN and time.time() < TOKEN_EXPIRES_AT - 60:  # refresh 1 min before expiry
        return ACCESS_TOKEN

    # Request new token
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': os.environ["IGDB_CLIENT_ID"],
        'client_secret': os.environ["IGDB_CLIENT_SECRET"],
        'grant_type': 'client_credentials'
    }
    resp = requests.post(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    ACCESS_TOKEN = data['access_token']
    TOKEN_EXPIRES_AT = time.time() + data['expires_in']
    return ACCESS_TOKEN

MUSIC_API_TOKEN = os.environ["DISCOGS_ACCESS_TOKEN"]

FILM_API_HEADERS = {
    "Authorization": f"Bearer {os.environ['TMDB_ACCESS_TOKEN']}",
    "accept": "application/json"
}

GAME_API_HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Client-ID": os.environ['IGDB_CLIENT_SECRET']
}

def music_lookup(title):
    discog = discogs_client.Client('ExampleApplication/0.1', user_token=MUSIC_API_TOKEN)
    results = discog.search(title, type='release')
    return results

def music_release(release_id):
    discog = discogs_client.Client('ExampleApplication/0.1', user_token=MUSIC_API_TOKEN)
    result = discog.release(release_id)
    return result
