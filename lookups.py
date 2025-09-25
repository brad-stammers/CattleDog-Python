import discogs_client
import requests
from flask import request
import os
import time
from dotenv import load_dotenv

load_dotenv()

BOOK_SEARCH_URL = "https://www.googleapis.com/books/v1/volumes"
FILM_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
FILM_DETAILS_URL = "https://api.themoviedb.org/3/movie/"
TV_SEARCH_URL = "https://api.themoviedb.org/3/search/tv"
TV_DETAILS_URL = "https://api.themoviedb.org/3/tv/"
GAME_SEARCH_URL = "https://api.rawg.io/api/games"

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
FILM_API_TOKEN = os.environ["TMDB_ACCESS_TOKEN"]
GAME_API_KEY = os.environ['RAWG_API_KEY']

FILM_API_HEADERS = {
    "Authorization": f"Bearer {os.environ['TMDB_ACCESS_TOKEN']}",
    "accept": "application/json"
}

GAME_API_HEADERS = {
    "Accept": "application/json"
}

def music_lookup(title):
    discog = discogs_client.Client('ExampleApplication/0.1', user_token=MUSIC_API_TOKEN)
    results = discog.search(title, type='release')
    return results

def book_lookup(title):
    print(title)
    results = []
    print(request.method)
    if request.method == "POST":
        if title:
            resp = requests.get(
                BOOK_SEARCH_URL,
                params={"q": f"intitle:{title}", "langRestrict": "en"},
            )
            print(resp)
            print(resp.status_code)
            if resp.status_code == 200:
                results = resp.json().get("items", [])

    return results

def film_lookup(title):
    results = []
    if request.method == "POST":
        if title:
            resp = requests.get(
                FILM_SEARCH_URL,
                params={"query": title, "include_adult": "false", "language": "en-US"},
                headers=FILM_API_HEADERS
            )
            if resp.status_code == 200:
                results = resp.json()

    return results

def film_genres(movie_id):
    results = []
    if movie_id:
        resp = requests.get(
            f"{FILM_DETAILS_URL}{movie_id}",
            params={"language": "en-US"},
            headers=FILM_API_HEADERS
        )
        if resp.status_code == 200:
            results = resp.json()
            genres = []
            for gen in results['genres']:
                genres.append(gen['name'])

    return genres

def television_lookup(title):
    results = []
    if request.method == "POST":
        if title:
            resp = requests.get(
                TV_SEARCH_URL,
                params={"query": title, "include_adult": "false", "language": "en-US"},
                headers=FILM_API_HEADERS
            )
            if resp.status_code == 200:
                results = resp.json()

    return results

def television_genres(tv_id):
    results = []
    if tv_id:
        resp = requests.get(
            f"{TV_DETAILS_URL}{tv_id}",
            params={"language": "en-US"},
            headers=FILM_API_HEADERS
        )
        if resp.status_code == 200:
            results = resp.json()
            genres = []
            for gen in results['genres']:
                genres.append(gen['name'])

    return genres

def game_lookup(title):
    results = []
    params = {
        "key": GAME_API_KEY,
        "search": title,          # the game title to search
        "page_size": 5,           # limit number of results
    }
    if request.method == "POST":
        if title:
            resp = requests.get(
                GAME_SEARCH_URL,
                params=params,
                headers=GAME_API_HEADERS
            )
            resp.raise_for_status()
            if resp.status_code == 200:
                results = resp.json()

    return results

def game_dlc(game_id):
    results = []
    params = {
        "key": GAME_API_KEY
    }
    if game_id:
        resp = requests.get(
            f"{GAME_SEARCH_URL}/{game_id}/additions",
            params=params,
            headers=GAME_API_HEADERS
        )
        resp.raise_for_status()
        if resp.status_code == 200:
            results = resp.json()

    return results

def game_details(game_id):
    results = []
    params = {
        "key": GAME_API_KEY
    }
    if game_id:
        resp = requests.get(
            f"{GAME_SEARCH_URL}/{game_id}",
            params=params,
            headers=GAME_API_HEADERS
        )
        resp.raise_for_status()
        if resp.status_code == 200:
            results = resp.json()

    return results



