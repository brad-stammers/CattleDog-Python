from lookups import music_lookup, book_lookup, film_lookup, film_genres, television_lookup, television_genres, game_lookup

if __name__ == "__main__":
    results = game_lookup("Halo")
    print(results)