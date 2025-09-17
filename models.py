from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    publisher: Mapped[str] = mapped_column(String(250), nullable=True)
    publish_date: Mapped[str] = mapped_column(DateTime, nullable=True)
    genre: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    synopsis: Mapped[str] = mapped_column(String(500), nullable=True)
    series: Mapped[str] = mapped_column(String(250), nullable=True)
    series_no: Mapped[int] = mapped_column(Integer, nullable=True)
    media: Mapped[str] = mapped_column(String(250), nullable=False)
    isbn: Mapped[str] = mapped_column(String(250), nullable=True)
    cover_path: Mapped[str] = mapped_column(String(250), nullable=True)

    def __repr__(self):
        return f"<Book(id={self.id}, title={self.title}, author={self.author}, publisher={self.publisher}, publish_date={self.publish_date}, genre={self.genre}, synopsis={self.synopsis}, series={self.series}, series_no={self.series_no}, media={self.media}, isbn={self.isbn}, cover_path={self.cover_path})>"
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    def get_all_books(self, **kwargs):
        session = kwargs.get("session")



class Music(Base):
    __tablename__ = "music"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    artist: Mapped[str] = mapped_column(String(250), nullable=False)
    release_date: Mapped[str] = mapped_column(DateTime, nullable=True)
    media: Mapped[str] = mapped_column(String(250), nullable=False)
    genre: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    track_list: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    cover_path: Mapped[str] = mapped_column(String(250), nullable=True)

    def __repr__(self):
        return f"<Music(id={self.id}, title={self.title}, artist={self.artist}, release_date={self.release_date}, media={self.media}, genre={self.genre}, track_list={self.track_list}, cover_path={self.cover_path})>"
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Film(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    genre: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    rating: Mapped[str] = mapped_column(String(250), nullable=True)
    media: Mapped[str] = mapped_column(String(250), nullable=False)
    synopsis: Mapped[str] = mapped_column(String(500), nullable=True)
    cover_path: Mapped[str] = mapped_column(String(250), nullable=True)

    def __repr__(self):
        return f"<Film(id={self.id}, title={self.title}, genre={self.genre}, year={self.year}, rating={self.rating}, media={self.media}, synopsis={self.synopsis}, cover_path={self.cover_path})>"
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Television(Base):
    __tablename__ = "television"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    genre: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    rating: Mapped[str] = mapped_column(String(250), nullable=True)
    media: Mapped[str] = mapped_column(String(250), nullable=False)
    season: Mapped[int] = mapped_column(Integer, nullable=True)
    episode_list: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    cover_path: Mapped[str] = mapped_column(String(250), nullable=True)

    def __repr__(self):
        return f"<Film(id={self.id}, title={self.title}, genre={self.genre}, year={self.year}, rating={self.rating}, media={self.media}, season={self.season}, episode_list={self.episode_list}, cover_path={self.cover_path})>"
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    genre: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    media: Mapped[str] = mapped_column(String(250), nullable=False)
    franchise: Mapped[str] = mapped_column(String(250), nullable=True)
    game_type: Mapped[str] = mapped_column(String(250), nullable=True)
    platform: Mapped[str] = mapped_column(String(250), nullable=True)
    dlc: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    expansions: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)
    synopsis: Mapped[str] = mapped_column(String(500), nullable=True)
    cover_path: Mapped[str] = mapped_column(String(250), nullable=True)

    def __repr__(self):
        return f"<Film(id={self.id}, title={self.title}, genre={self.genre}, media={self.media}, franchise={self.franchise}, game_type={self.game_type}, platform={self.platform}, dlc={self.dlc}, expansions={self.expansions}, synopsis={self.synopsis}, cover_path={self.cover_path})>"
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

