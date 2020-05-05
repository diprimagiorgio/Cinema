from sqlalchemy import Table, Column, Integer, String, Float, Date, ForeignKey, CheckConstraint, DateTime
from app import metadata, engine
#--------tabella
users = Table( 'users', metadata,
            Column('id', Integer , primary_key = True, autoincrement=True),
            Column('name', String),
            Column('surname', String),
            Column('email', String, unique = True, nullable = False),
            Column('password', String, nullable = False)#PENSARE MINIMO LUNGHEZZE
        )

clients = Table( 'clients', metadata,
                Column('id', None , ForeignKey('users.id'), primary_key = True),
                Column('credit', Float),#credito potrebbe essere not null e >=0
                Column('birthDate', Date)#, CheckConstraint( (date.today() - 'birthDate').days > 0 )),
            )

managers = Table('managers', metadata,
                Column('id', None , ForeignKey('users.id'), primary_key = True),
                Column('admin', Float, nullable = False),
                Column('financialReport', Float)#>=0 not null
            )

theaters = Table('theaters', metadata,
             Column('id', Integer, primary_key = True),
             Column('seatsCapacity', Integer, nullable = False)#numero posti >=0
            )

movies = Table('movies', metadata,
             Column('id', Integer, primary_key = True, autoincrement=True), 
             Column('title', String),#not null
             Column('minimumAge', Integer, default = 0),#CHECK >=0
             Column('duration', Float, nullable = False),#CHECK >=0
             Column('idGenre', None, ForeignKey('genres.id'))

            )

#genreMovies = Table('genreMovies', metadata,
#                   Column('idMovie', None, ForeignKey('movies.id'), primary_key = True),
#                   Column('idGenre', None, ForeignKey('genres.id'), primary_key = True)
#                )

genres = Table('genres', metadata,
               Column('id', Integer, primary_key = True, autoincrement=True),
               Column('description', String)#NOT NULL
            )

movieSchedule = Table('movieSchedule', metadata,        #RIPENSARE NOME DELLA TABELLA 
                Column('id', Integer, primary_key = True, autoincrement=True),
                Column('dateTime',DateTime),#NOT NULL
                Column('price', Float),#NOT NULL >=0
                Column('idMovie',None, ForeignKey('movies.id'), nullable = False),
                Column('theater', None, ForeignKey('theaters.id'), nullable = False)
                
              )
booking = Table('booking', metadata, 
                Column('id', Integer, primary_key = True),
                Column('viewerName', String),#NOT NULL
                Column('viewerAge', String),#NOT NULL
                Column('seatNumber', Integer, nullable = False),
                Column('clientUsername',None, ForeignKey('clients.id'), nullable = False),
                Column('idmovieShedule', None, ForeignKey('movieShedule.id'), nullable = False)
)

metadata.create_all(engine)
#----------fine tabella