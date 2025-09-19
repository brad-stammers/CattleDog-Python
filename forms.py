from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, SelectMultipleField, TextAreaField, DateField, IntegerField
from wtforms.validators import DataRequired, URL, Optional

#book form
class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    publisher = StringField('Publisher')
    publish_date = DateField("Published Date", validators=[Optional()])
    genre = SelectMultipleField("Genre", choices=[" ", "Action and Adventure", "Comedy", "Crime", "Fantasy", "Historical", "Horror", "Mystery", "Non-Fiction", "Romance", "Thriller", "Science Fiction", "Young Adult"], validators=[DataRequired()])
    synopsis = TextAreaField('Synopsis')
    series = StringField("Series")
    series_no = IntegerField("No in Series", validators=[Optional()])
    media = SelectField("Format", choices=[" ", "E-Book", "Graphic Novel", "Hardcover", "Paperback"], validators=[DataRequired()])
    isbn = StringField("Priority")
    cover_path = StringField("Cover Image", validators=[URL(), Optional()])
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')


