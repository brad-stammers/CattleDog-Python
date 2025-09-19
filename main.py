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

from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Book, Music,Film, Television, Game
from forms import BookForm
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
    return render_template('books.html', current_page="Books", all_books=list_books)

@app.route("/books/<int:book_id>")
def show_book(book_id):
    book = session.get(Book, book_id)
    return render_template("book_details.html", book=book)

@app.route("/books/add", methods=["GET", "POST"])
def add_new_book():
    form = BookForm()
    if form.validate_on_submit():
        if form.submit.data:
            new_book = Book(
                title=form.title.data,
                author=form.author.data,
                publisher=form.publisher.data,
                publish_date=form.publish_date.data,
                genre=form.genre.data,
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
    return render_template('add_book.html', form=form)

@app.route("/books/edit/<int:book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    book = session.get(Book, book_id)
    form = BookForm(
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        publish_date=book.publish_date,
        genre=book.genre,
        synopsis=book.synopsis,
        series=book.series,
        series_no=book.series_no,
        media=book.media,
        isbn=book.isbn,
        cover_path=book.cover_path
    )
    if form.validate_on_submit():
        if form.submit.data:
            book.title=form.title.data,
            book.author=form.author.data,
            book.publisher=form.publisher.data,
            book.publish_date=form.publish_date.data,
            book.genre=form.genre.data,
            book.synopsis=form.synopsis.data,
            book.series=form.series.data,
            book.series_no=form.series_no.data,
            book.media=form.media.data,
            book.isbn=form.isbn.data,
            book.cover_path=form.cover_path.data
            session.commit()
        return redirect(url_for('books'))
    return render_template('add_book.html', form=form)

@app.route("/books/delete/<int:book_id>")
def delete_book(book_id):
    book = session.get(Book, book_id)
    session.delete(book)
    session.commit()
    return redirect(url_for('books'))


@app.route("/films")
def films():
    all_films = session.query(Film).all()
    list_films = [film.to_dict() for film in all_films]
    return render_template('films.html', current_page="Films", all_films=list_films)

@app.route("/films/add", methods=["GET", "POST"])
def add_new_film():
    pass

@app.route("/television")
def television():
    all_tv = session.query(Television).all()
    list_tv = [tv.to_dict() for tv in all_tv]
    return render_template('television.html', current_page="Television", all_tv=list_tv)

@app.route("/television/add", methods=["GET", "POST"])
def add_new_television():
    pass

@app.route("/games")
def games():
    all_games = session.query(Game).all()
    list_games = [game.to_dict() for game in all_games]
    return render_template('games.html', current_page="Games", all_games=list_games)

@app.route("/games/add", methods=["GET", "POST"])
def add_new_game():
    pass

@app.route("/music")
def music():
    all_music = session.query(Music).all()
    list_music = [mus.to_dict() for mus in all_music]
    return render_template('music.html', current_page="music", all_music=list_music)

@app.route("/music/add", methods=["GET", "POST"])
def add_new_music():
    pass

if __name__ == "__main__":
    app.run(debug=True)

