from sqlalchemy import Table, Column, Integer, String, Float, Date, ForeignKey, CheckConstraint, DateTime
from app import metadata, engine
#--------tabella
users = Table( 'users', metadata,
            Column('id', Integer , primary_key = True, autoincrement=True),
            Column('name', String),
            Column('surname', String),
            Column('email', String, unique = True, nullable = False),
            Column('password', String)
        )

clients = Table( 'clients', metadata,
                Column('id', None , ForeignKey('users.id'), primary_key = True),
                Column('credit', Float),
                Column('birthDate', Date)#, CheckConstraint( (date.today() - 'birthDate').days > 0 )),
            )

managers = Table('managers', metadata,
                Column('id', None , ForeignKey('users.id'), primary_key = True),
                Column('admin', Float, nullable = False),
                Column('financialReport', Float)
            )

theaters = Table('theaters', metadata,
             Column('id', Integer, primary_key = True),
             Column('placesAvailable', Integer, nullable = False)
            )

movies = Table('movies', metadata,
             Column('id', Integer, primary_key = True), 
             Column('title', String),
             Column('minimumAge', Integer, default = 0),
             Column('duration', Float, nullable = False),

            )

genreMovies = Table('genreMovies', metadata,
                   Column('idMovie', None, ForeignKey('movies.id'), primary_key = True),
                   Column('idGenre', None, ForeignKey('genres.id'), primary_key = True)
                )

genres = Table('genres', metadata,
               Column('id', Integer, primary_key = True),
               Column('description', String)
            )

                Column('dateTime',DateTime),
metadata.create_all(engine)
#----------fine tabella