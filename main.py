########################################################################################################################
###
###                                  CattleDog App
###
###    Summary:  An application to catalogue details for libraries of books, music, film, television and games
###              It also has a facility to scan an item barcode and download the details from online records
###
###    Author:          Brad Stammers
###    Creation Date:   12/09/2025
###
###
########################################################################################################################

from flask import Flask, render_template, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image
from pyzbar.pyzbar import decode
import base64
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Book, Music,Film, Television, Game
from forms import BookForm, FilmForm, TelevisionForm, GameForm, MusicForm
from lookups import music_lookup, music_release
import io
import os
from dotenv import load_dotenv

load_dotenv()

# initialise database
engine = create_engine(os.environ['DATABASE_PATH'])
# create tables if they don't exist
Base.metadata.create_all(engine)
# create session
Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_PATH']
app.config['SQLALCHEMY_TRCK_NOTIFICATIONS'] = False


@app.route("/")
def home():
    return render_template('home.html')

#book routes
@app.route("/books")
def books():
    all_books = session.query(Book).all()
    list_books = [book.to_dict() for book in all_books]
    return render_template('books/books.html', current_page="Books", all_books=list_books)

@app.route("/books/<int:book_id>")
def show_book(book_id):
    book = session.get(Book, book_id)
    return render_template("books/book_details.html", book=book)

@app.route("/books/add", methods=["GET", "POST"])
def add_new_book():
    form = BookForm()
    if form.validate_on_submit():
        if form.submit.data:
            print(f"Genre from form = {form.genre.data}")
            new_book = Book(
                title=form.title.data,
                author=form.author.data,
                publisher=form.publisher.data,
                publish_date=form.publish_date.data,
                genre=", ".join(form.genre.data),
                synopsis=form.synopsis.data,
                series=form.series.data,
                series_no=form.series_no.data,
                media=form.media.data,
                isbn=form.isbn.data,
                cover_path=form.cover_path.data
            )
            session.add(new_book)
            session.commit()
        return redirect(url_for('books'))
    return render_template('books/add_book.html', form=form)

@app.route("/books/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    book = session.get(Book, book_id)
    genre_list = book.genre.split(", ")
    print(f"Genre from database = {genre_list}")
    form = BookForm(
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        publish_date=book.publish_date,
        genre=genre_list,
        synopsis=book.synopsis,
        series=book.series,
        series_no=book.series_no,
        media=book.media,
        isbn=book.isbn,
        cover_path=book.cover_path
    )
    if form.validate_on_submit():
        if form.submit.data:
            print("Form data:", form.genre.data, type(form.genre.data))
            book.title=form.title.data,
            book.author=form.author.data,
            book.publisher=form.publisher.data,
            book.publish_date=form.publish_date.data,
            book.genre=", ".join(form.genre.data),
            book.synopsis=form.synopsis.data,
            book.series=form.series.data,
            book.series_no=form.series_no.data,
            book.media=form.media.data,
            book.isbn=form.isbn.data,
            book.cover_path=form.cover_path.data
            session.commit()
        return redirect(url_for('books'))
    return render_template('books/add_book.html', form=form)

@app.route("/books/delete/<int:book_id>")
def delete_book(book_id):
    book = session.get(Book, book_id)
    session.delete(book)
    session.commit()
    return redirect(url_for('books'))

# film routes
@app.route("/films")
def films():
    all_films = session.query(Film).all()
    list_films = [film.to_dict() for film in all_films]
    return render_template('films/films.html', current_page="Films", all_films=list_films)

@app.route("/films/<int:film_id>")
def show_film(film_id):
    film = session.get(Film, film_id)
    return render_template("films/film_details.html", film=film)

@app.route("/films/add", methods=["GET", "POST"])
def add_new_film():
    form = FilmForm()
    if form.validate_on_submit():
        if form.submit.data:
            new_film = Film(
                title=form.title.data,
                genre=", ".join(form.genre.data),
                year=form.year.data,
                rating=form.rating.data,
                media=form.media.data,
                synopsis=form.synopsis.data,
                cover_path=form.cover_path.data
            )
            session.add(new_film)
            session.commit()
        return redirect(url_for('films'))
    return render_template('films/add_film.html', form=form)

@app.route("/films/edit/<int:film_id>", methods=["GET", "POST"])
def edit_film(film_id):
    film = session.get(Film, film_id)
    genre_list = film.genre.split(", ")
    form = FilmForm(
        title=film.title,
        genre=genre_list,
        year=film.year,
        rating=film.rating,
        media=film.media,
        synopsis=film.synopsis,
        cover_path=film.cover_path
    )
    if form.validate_on_submit():
        if form.submit.data:
            film.title=form.title.data,
            film.genre = ", ".join(form.genre.data),
            film.year=form.year.data,
            film.rating=form.rating.data,
            film.media = form.media.data,
            film.synopsis=form.synopsis.data,
            film.cover_path=form.cover_path.data
            session.commit()
        return redirect(url_for('films'))
    return render_template('films/add_film.html', form=form)

@app.route("/films/delete/<int:film_id>")
def delete_film(film_id):
    film = session.get(Film, film_id)
    session.delete(film)
    session.commit()
    return redirect(url_for('films'))

#television routes
@app.route("/television")
def television():
    all_tv = session.query(Television).all()
    list_tv = [tv.to_dict() for tv in all_tv]
    return render_template('television/television.html', current_page="Television", all_tv=list_tv)

@app.route("/television/<int:tv_id>")
def show_television(tv_id):
    tv = session.get(Television, tv_id)
    return render_template("television/television_details.html", tv=tv)

@app.route("/television/add", methods=["GET", "POST"])
def add_new_television():
    form = TelevisionForm()
    if form.validate_on_submit():
        if form.submit.data:
            new_tv = Television(
                title=form.title.data,
                genre=", ".join(form.genre.data),
                year=form.year.data,
                rating=form.rating.data,
                media=form.media.data,
                season=form.season.data,
                episode_list=form.episode_list.data,
                cover_path=form.cover_path.data
            )
            session.add(new_tv)
            session.commit()
        return redirect(url_for('television'))
    return render_template('television/add_television.html', form=form)

@app.route("/television/edit/<int:tv_id>", methods=["GET", "POST"])
def edit_television(tv_id):
    tv = session.get(Television, tv_id)
    genre_list = tv.genre.split(", ")
    form = TelevisionForm(
        title=tv.title,
        genre=genre_list,
        year=tv.year,
        rating=tv.rating,
        media=tv.media,
        season=tv.season,
        episode_list=tv.episode_list,
        cover_path=tv.cover_path
    )
    if form.validate_on_submit():
        if form.submit.data:
            tv.title=form.title.data,
            tv.genre = ", ".join(form.genre.data),
            tv.year=form.year.data,
            tv.rating=form.rating.data,
            tv.media = form.media.data,
            tv.season = form.season.data,
            tv.episode_list=form.episode_list.data,
            tv.cover_path=form.cover_path.data
            session.commit()
        return redirect(url_for('television'))
    return render_template('television/add_television.html', form=form)

@app.route("/television/delete/<int:tv_id>")
def delete_television(tv_id):
    tv = session.get(Television, tv_id)
    session.delete(tv)
    session.commit()
    return redirect(url_for('films'))

#game routes
@app.route("/games")
def games():
    all_games = session.query(Game).all()
    list_games = [game.to_dict() for game in all_games]
    return render_template('games/games.html', current_page="Games", all_games=list_games)

@app.route("/games/<int:game_id>")
def show_game(game_id):
    game = session.get(Game, game_id)
    return render_template("games/game_details.html", game=game)

@app.route("/games/add", methods=["GET", "POST"])
def add_new_game():
    form = GameForm()
    if form.validate_on_submit():
        if form.submit.data:
            new_game = Game(
                title=form.title.data,
                genre=", ".join(form.genre.data),
                media=form.media.data,
                franchise=form.franchise.data,
                platform=form.platform.data,
                dlc=form.dlc.data,
                expansions=form.expansions.data,
                synopsis=form.synopsis.data,
                cover_path=form.cover_path.data
            )
            session.add(new_game)
            session.commit()
        return redirect(url_for('games'))
    return render_template('games/add_game.html', form=form)

@app.route("/games/edit/<int:game_id>", methods=["GET", "POST"])
def edit_game(game_id):
    game = session.get(Game, game_id)
    genre_list = game.genre.split(", ")
    form = GameForm(
        title=game.title,
        genre=genre_list,
        media=game.media,
        franchise=game.franchise,
        platform=game.platform,
        dlc=game.dlc,
        expansions=game.expansions,
        synopsis=game.synopsis,
        cover_path=game.cover_path
    )
    if form.validate_on_submit():
        if form.submit.data:
            game.title=form.title.data,
            game.genre = ", ".join(form.genre.data),
            game.media = form.media.data,
            game.franchise=form.franchise.data,
            game.platform=form.platform.data,
            game.dlc=form.dlc.data,
            game.expansions=form.expansions.data,
            game.synopsis=form.synopsis.data,
            game.cover_path=form.cover_path.data
            session.commit()
        return redirect(url_for('games'))
    return render_template('games/add_game.html', form=form)

@app.route("/games/delete/<int:game_id>")
def delete_game(game_id):
    game = session.get(Game, game_id)
    session.delete(game)
    session.commit()
    return redirect(url_for('games'))


@app.route("/music")
def music():
    all_music = session.query(Music).all()
    list_music = [mus.to_dict() for mus in all_music]
    return render_template('music/music.html', current_page="Music", all_music=list_music)

@app.route("/music/<int:music_id>")
def show_music(music_id):
    album = session.get(Music, music_id)
    return render_template("music/music_details.html", music=album)

@app.route("/music/add", methods=["GET", "POST"])
def add_new_music():
    form = MusicForm()
    if form.validate_on_submit():
        if form.submit.data:
            new_music = Music(
                title=form.title.data,
                artist=form.artist.data,
                release_date=form.release_date.data,
                media=form.media.data,
                genre=", ".join(form.genre.data),
                track_list=form.track_list.data,
                cover_path=form.cover_path.data
            )
            session.add(new_music)
            session.commit()
        return redirect(url_for('music'))
    return render_template('music/add_music.html', form=form)

@app.route("/music/edit/<int:music_id>", methods=["GET", "POST"])
def edit_music(music_id):
    album = session.get(Music, music_id)
    genre_list = album.genre.split(", ")
    form = MusicForm(
        title=album.title,
        artist=album.artist,
        release_date=album.release_date,
        media=album.media,
        genre=genre_list,
        track_list=album.track_list,
        cover_path=album.cover_path
    )
    if form.validate_on_submit():
        if form.submit.data:
            album.title=form.title.data,
            album.artist=form.artist.data,
            album.release_date=form.release_date.data,
            album.media = form.media.data,
            album.genre = ", ".join(form.genre.data),
            album.track_list=form.track_list.data,
            album.cover_path=form.cover_path.data
            session.commit()
        return redirect(url_for('music'))
    return render_template('music/add_music.html', form=form)

@app.route("/music/delete/<int:music_id>")
def delete_music(music_id):
    album = session.get(Music, music_id)
    session.delete(album)
    session.commit()
    return redirect(url_for('music'))

music_results = []

@app.route("/music/search", methods=["GET", "POST"])
def search_music():
    global music_results
    if request.method == "POST":
        query = request.form.get("album")
        music_results = music_lookup(query)
    return render_template("music/music_search.html", results=music_results)

@app.route("/music/select/<int:index>", methods=["GET", "POST"])
def select_release(index):
    global music_results
    release = music_results[index]
    tracks = [track.title for track in release.tracklist]

    form = MusicForm(
        title=release.title,
        artist=release.artists[0].name,
        release_date=release.year,
        media=release.formats[0]['name'],
        genre=release.genres,
        cover_path=release.images[0]['uri'],
        track_list = ",".join(tracks)
    )
    if form.validate_on_submit():
        if form.submit.data:
            tracks = [t.strip() for t in form.track_list.data.split(",")]
            new_music = Music(
                title=form.title.data,
                artist=form.artist.data,
                release_date=form.release_date.data,
                media=form.media.data,
                genre=", ".join(form.genre.data),
                track_list=tracks,
                cover_path=form.cover_path.data
            )
            session.add(new_music)
            session.commit()
        return redirect(url_for('music'))
    return render_template('music/add_music.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)

