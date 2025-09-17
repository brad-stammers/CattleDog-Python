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

@app.route("/books")
def books():
    all_books = session.query(Book).all()
    list_books = [book.to_dict() for book in all_books]
    return render_template('books.html', current_page="Books", all_books=list_books)

@app.route("/films")
def films():
    return render_template('films.html', current_page="Films")

@app.route("/television")
def television():
    return render_template('television.html', current_page="Television")

@app.route("/games")
def games():
    return render_template('games.html', current_page="Games")

@app.route("/music")
def music():
    return render_template('music.html', current_page="music")

if __name__ == "__main__":
    app.run(debug=True)

