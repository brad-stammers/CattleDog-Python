from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, URL, Optional

BOOK_GENRES = [
    (" ", " "),
    ("Action and Adventure", "Action and Adventure"),
    ("Comedy", "Comedy"),
    ("Crime", "Crime"),
    ("Fantasy", "Fantasy"),
    ("Historical", "Historical"),
    ("Horror", "Horror"),
    ("Mystery", "Mystery"),
    ("Non-Fiction", "Non-Fiction"),
    ("Romance", "Romance"),
    ("Thriller", "Thriller"),
    ("Science Fiction", "Science Fiction"),
    ("Young Adult", "Young Adult")
]
BOOK_FORMATS = [
    (" ", " "),
    ("E-Book", "E-Book"),
    ("Graphic Novel", "Graphic Novel"),
    ("Hardcover", "Hardcover"),
    ("Paperback", "Paperback")
]

FILM_GENRES = [
    ("Action", "Action"),
    ("Adventure", "Adventure"),
    ("Animation", "Animation"),
    ("Comedy", "Comedy"),
    ("Crime", "Crime"),
    ("Documentary", "Documentary"),
    ("Drama", "Drama"),
    ("Family", "Family"),
    ("Fantasy", "Fantasy"),
    ("History", "History"),
    ("Horror", "Horror"),
    ("Music", "Music"),
    ("Mystery", "Mystery"),
    ("Romance", "Romance"),
    ("Science Fiction", "Science Fiction"),
    ("Sports", "Sports"),
    ("Superhero", "Superhero"),
    ("Thriller", "Thriller"),
    ("War", "War"),
    ("Western", "Western")
]
TV_GENRES = [
    ("Action & Adventure", "Action & Adbenture"),
    ("Animation", "Animation"),
    ("Comedy", "Comedy"),
    ("Crime", "Crime"),
    ("Documentary", "Documentary"),
    ("Drama", "Drama"),
    ("Family", "Family"),
    ("Kids", "Kids"),
    ("Mystery", "Mystery"),
    ("News", "News"),
    ("Reality", "Reality"),
    ("Sci-Fi & Fantasy", "Sci-Fi & Fantasy"),
    ("Soap", "Soap"),
    ("Talk", "Talk"),
    ("War & Politics", "War & Politics"),
    ("Western", "Western")
]
FILM_RATINGS = [ (" ", " "), ("G", "G"), ("PG", "PG"), ("M", "M"), ("MA 15+", "MA 15+"), ("R 18+", "R 18+")]
FILM_FORMATS = [
    (" ", " "),
    ("4K Ultra", "4K Ultra"),
    ("Bluray", "Bluray"),
    ("Digital Download", "Digital Download"),
    ("DVD", "DVD"),
    ("VHS", "VHS"),
]

GAME_GENRES = [
    ("Action", "Action"),
    ("Action-Adventure", "Action-Adventure"),
    ("Adventure", "Adventure"),
    ("Casual", "Casual"),
    ("MMO", "MMO"),
    ("Puzzle", "Puzzle"),
    ("RPG", "RPG"),
    ("Simulation", "Simulation"),
    ("Sports", "Sports"),
    ("Strategy", "Strategy"),
    ("Survival", "Survival")

]
GAME_PLATFORMS = [
    ("Nintendo Switch", "Nintendo Switch"),
    ("PC", "PC"),
    ("Playstation 4", "Playstation 4"),
    ("Playstation 5", "Playstation 5"),
    ("Wii", "Wii"),
    ("Xbox", "Xbox")
]
GAME_FORMATS = [
    (" ", " "),
    ("CD", "CD"),
    ("Digital Download", "Digital Download"),
    ("DVD", "DVD")
]

MUSIC_GENRES = [
    ("Blues", "Blues"),
    ("Classical", "Classical"),
    ("Country", "Country"),
    ("Easy Listening", "Easy Listening"),
    ("Electronic", "Electronic"),
    ("Folk/World", "Folk/World"),
    ("Hip Hop/Rap", "Hip Hop/Rap"),
    ("Jazz", "Jazz"),
    ("Pop", "Pop"),
    ("R&B/Soul", "R&B/Soul"),
    ("Reggae", "Reggae"),
    ("Rock", "Rock"),
    ("Soundtrack", "Soundtrack")
]
MUSIC_FORMATS = [
    (" ", " "),
    ("Cassette", "Cassette"),
    ("CD", "CD"),
    ("Digital Download", "Digital Download"),
    ("Vinyl", "Vinyl")
]

#book form
class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    publisher = StringField('Publisher')
    publish_date = IntegerField("Published Date", validators=[Optional()])
    genre = SelectMultipleField("Genre", choices=BOOK_GENRES, validators=[DataRequired()])
    synopsis = TextAreaField('Synopsis')
    series = StringField("Series")
    series_no = IntegerField("No in Series", validators=[Optional()])
    media = SelectField("Format", choices=BOOK_FORMATS, validators=[DataRequired()], coerce=str)
    isbn = StringField("Priority")
    cover_path = StringField("Cover Image", validators=[URL(), Optional()])
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')

# film form
class FilmForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    genre = SelectMultipleField("Genre", choices=FILM_GENRES, validators=[DataRequired()])
    year = IntegerField("Year", validators=[Optional()])
    rating = SelectField("Rating", choices=FILM_RATINGS, validators=[Optional()], coerce=str)
    media = SelectField("Format", choices=FILM_FORMATS, validators=[DataRequired()], coerce=str)
    synopsis = TextAreaField('Synopsis', validators=[Optional()])
    cover_path = StringField("Cover Image", validators=[URL(), Optional()])
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')

#television form
class TelevisionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    genre = SelectMultipleField("Genre", choices=TV_GENRES, validators=[DataRequired()])
    year = IntegerField("Year", validators=[Optional()])
    rating = SelectField("Rating", choices=FILM_RATINGS, validators=[Optional()], coerce=str)
    media = SelectField("Format", choices=FILM_FORMATS, validators=[DataRequired()], coerce=str)
    season = IntegerField("Season", validators=[Optional()])
    episode_list = TextAreaField('Episode List', validators=[Optional()])
    cover_path = StringField("Cover Image", validators=[URL(), Optional()])
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')

#game form
class GameForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    genre = SelectMultipleField("Genre", choices=GAME_GENRES, validators=[DataRequired()])
    media = SelectField("Format", choices=GAME_FORMATS, validators=[DataRequired()], coerce=str)
    franchise = StringField("Franchise", validators=[Optional()])
    platform = SelectField("Platform", choices=GAME_PLATFORMS, validators=[DataRequired()], coerce=str)
    dlc = TextAreaField('DLC', validators=[Optional()])
    expansions = TextAreaField('Expansions', validators=[Optional()])
    synopsis = TextAreaField('Synopsis', validators=[Optional()])
    cover_path = StringField("Cover Image", validators=[URL(), Optional()])
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')

# music form
class MusicForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    artist = StringField('Artist', validators=[DataRequired()])
    release_date = IntegerField("Release Date", validators=[Optional()])
    media = SelectField("Format", choices=MUSIC_FORMATS, validators=[DataRequired()], coerce=str)
    genre = SelectMultipleField("Genre", choices=MUSIC_GENRES, validators=[DataRequired()])
    track_list = TextAreaField('Synopsis')
    cover_path = StringField("Cover Image", validators=[URL(), Optional()])
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')




