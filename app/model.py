from sqlalchemy import Table, Column, Integer, String, Float, Date, ForeignKey, CheckConstraint, DateTime, Boolean, column
from app import metadata, engine
from datetime import date
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
                Column('credit', Float, nullable = False ),#credito potrebbe essere not null e >=0
                Column('birthDate', Date),
             #   CheckConstraint( (column('birthDate') > date.today().__str__() ), name='minBirthDate'),           # non funziona da vedere 
                CheckConstraint(column('credit') >= 0, name='credit_gt_0')

            )

managers = Table('managers', metadata,
                Column('id', None , ForeignKey('users.id'), primary_key = True),
                Column('admin', Boolean, nullable = False),
                Column('financialReport', Float)#>=0 not null
            )

theaters = Table('theaters', metadata,
                Column('id', Integer, primary_key = True),
                Column('seatsCapacity', Integer, nullable = False),#numero posti >=0
                Column('available', Boolean, nullable = False, default = True)
            )

movies = Table('movies', metadata,
             Column('id', Integer, primary_key = True, autoincrement=True), 
             Column('title', String),#not null
             Column('minimumAge', Integer, default = 0),#CHECK >=0
             Column('duration', Integer, nullable = False),#CHECK >=0
             Column('idGenre', None, ForeignKey('genres.id', onupdate="CASCADE", ondelete="NO ACTION"),  nullable = False),
             Column('available', Boolean, nullable = False, default = True)


            )

genres = Table('genres', metadata,
               Column('id', Integer, primary_key = True, autoincrement=True),
               Column('description', String)#NOT NULL
            )

movieSchedule = Table('movieSchedule', metadata,         
                    Column('id', Integer, primary_key = True, autoincrement=True),
                    Column('dateTime',DateTime),#NOT NULL
                    Column('price', Float),#NOT NULL >=0
                    Column('idMovie', None, ForeignKey('movies.id', onupdate="CASCADE", ondelete="NO ACTION" ), nullable = False),
                    Column('theater', None, ForeignKey(column='theaters.id', onupdate="CASCADE", ondelete="SET NULL"), nullable = False)#,  nullable = False) perchè se voglio cancellare un theater ...
                    
                )

booking = Table('booking', metadata, 
                Column('id', Integer, primary_key = True),
                Column('viewerName', String),#NOT NULL
                Column('viewerAge', Integer),#NOT NULL
                Column('seatNumber', Integer, nullable = False),
                Column('clientUsername',None, ForeignKey('clients.id'), nullable = False),
                Column('idmovieSchedule', None, ForeignKey('movieSchedule.id'), nullable = False)
            )

metadata.create_all(engine)
#----------fine tabella