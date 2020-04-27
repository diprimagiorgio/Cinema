from sqlalchemy import Table, Column, Integer, String, Float
from app import metadata, engine
#--------tabella
users = Table( 'users', metadata,
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('name', String),
    Column('email', String, unique = True),
    Column('password', String)
)
theater = Table('theater', metadata,
             Column('id', Integer, primary_key = True),
             Column('placesAvailable', Integer, nullable = False))

movie = Table('movie', metadata,
             Column('title', String),
             Column('minimumAge', Integer, default = 0),
             Column('duration', Float, nullable = False),
             Column('id', Integer))

genreMovie = Table('genreMovie', metadata,
                   Column('idMovie', None, primary_key = True, ForeignKey('movie.id')),
                   Column('idGenre', None, primary_key = True, ForeignKey('genre.id')))
genre = Table('genre', metadata,
               Column('id', Integer, primary_key = True),
               Column('description', String))


metadata.create_all(engine)
#----------fine tabella