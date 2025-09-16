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

#define tables
# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     email = Column(String)
