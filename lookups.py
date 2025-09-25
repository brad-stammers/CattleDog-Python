import discogs_client
import requests
from flask import jsonify, request
import os
import time
from dotenv import load_dotenv

load_dotenv()

BOOK_SEARCH_URL = "https://www.googleapis.com/books/v1/volumes"
FILM_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
FILM_DETAILS_URL = "https://api.themoviedb.org/3/movie/"
TV_SEARCH_URL = "https://api.themoviedb.org/3/search/tv"
TV_DETAILS_URL = "https://api.themoviedb.org/3/tv/"
GAME_SEARCH_URL = "https://api.igdb.com/v4/games"

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
GAME_API_CLIENT_ID = os.environ['IGDB_CLIENT_ID']
GAME_API_CLIENT_SECRET = os.environ['IGDB_CLIENT_SECRET']
GAME_API_ACCESS_TOKEN = None
GAME_API_TOKEN_EXPIRES_AT = 0

FILM_API_HEADERS = {
    "Authorization": f"Bearer {os.environ['TMDB_ACCESS_TOKEN']}",
    "accept": "application/json"
}

GAME_API_HEADERS = {
    "Authorization": f"Bearer {GAME_API_ACCESS_TOKEN}",
    "Client-ID": GAME_API_CLIENT_ID
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


def get_game_access_token():
    global GAME_API_ACCESS_TOKEN, GAME_API_TOKEN_EXPIRES_AT
    # Check if token is valid
    if GAME_API_ACCESS_TOKEN and time.time() < GAME_API_TOKEN_EXPIRES_AT - 60:  # refresh 1 min before expiry
        return GAME_API_ACCESS_TOKEN

    # Request new token
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': GAME_API_CLIENT_ID,
        'client_secret': GAME_API_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    resp = requests.post(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    GAME_API_ACCESS_TOKEN = data['access_token']
    print(GAME_API_ACCESS_TOKEN)
    GAME_API_TOKEN_EXPIRES_AT = time.time() + data['expires_in']
    return GAME_API_ACCESS_TOKEN

def game_lookup(title):
    token = get_game_access_token()
    print(token)
    results = []
    query = f"""
        search "{title}";
        fields id, name, cover.image_id, genres.name, platforms.name, first_release_date;
        limit 5;
    """
    print(query)
    # if request.method == "GET":
    if title:
        resp = requests.post(
            GAME_SEARCH_URL,
            params={"data": query},
            headers=GAME_API_HEADERS
        )
        print("Status Code:", resp.status_code)
        print("Raw Response:", resp.text)
        resp.raise_for_status()
        print(resp)
        if resp.status_code == 200:
            results = resp.json()
            print(results)

    return results