from sqlalchemy import Table, Column, Integer, String, Float, Date, ForeignKey, CheckConstraint, UniqueConstraint, DateTime, Boolean, column
from app import metadata, engineAdmin
import datetime



from sqlalchemy import event, DDL



    
    




#--------tabella
users = Table( 'users', metadata,
            Column('id', Integer , primary_key = True, autoincrement=True),
            Column('name', String),
            Column('surname', String),
            Column('email', String, unique = True, nullable = False),
            Column('password', String, nullable = False)
        )

clients = Table( 'clients', metadata,
                Column('id', None , ForeignKey('users.id'), primary_key = True),
                Column('credit', Float, nullable = False, default = 0.0),
                Column('birthDate', Date),
                CheckConstraint(column('credit') >= 0, name='credit_ct_0'),
                CheckConstraint(column('birthDate') < str(datetime.date.today()), name='birth_ct_')
            )

managers = Table('managers', metadata,
                Column('id', None , ForeignKey('users.id'), primary_key = True),
                Column('admin', Boolean, nullable = False, default = False),
                Column('financialReport', Float, default = 0),
                CheckConstraint(column('financialReport') >= 0, name='credit_mg_0')
            )

theaters = Table('theaters', metadata,
                Column('id', Integer, primary_key = True),
                Column('seatsCapacity', Integer, nullable = False),
                Column('available', Boolean, nullable = False, default = True),
                CheckConstraint(column('seatsCapacity') >= 0, name='capacity_th_0')
            )

movies = Table('movies', metadata,
             Column('id', Integer, primary_key = True, autoincrement=True), 
             Column('title', String, nullable = False),
             Column('minimumAge', Integer, default = 0),
             Column('duration', Integer, nullable = False),
             Column('idGenre', None, ForeignKey('genres.id', onupdate="CASCADE", ondelete="NO ACTION"),  nullable = False),
             Column('available', Boolean, nullable = False, default = True),
             CheckConstraint(column('minimumAge') >= 0, name='age_ms_0'),
             CheckConstraint(column('duration') >= 0, name='duration_ms_0')
            )

genres = Table('genres', metadata,
               Column('id', Integer, primary_key = True, autoincrement=True),
               Column('description', String, nullable = False)
            )

movieSchedule = Table('movieSchedule', metadata,         
                    Column('id', Integer, primary_key = True, autoincrement=True),
                    Column('dateTime',DateTime,nullable = False),
                    Column('price', Float, nullable = False),
                    Column('idMovie', None, ForeignKey('movies.id', onupdate="CASCADE", ondelete="NO ACTION" ), nullable = False),
                    Column('theater', None, ForeignKey(column='theaters.id', onupdate="CASCADE", ondelete="SET NULL"), nullable = False),#,  nullable = False) perchè se voglio cancellare un theater ...
                    CheckConstraint(column('price') >= 0, name='price_ms_0')     
                )

booking = Table('booking', metadata, 
                Column('id', Integer, primary_key = True, autoincrement=True),
                Column('viewerName', String, nullable = False),
                Column('viewerAge', Integer, nullable = False),
                Column('seatNumber', Integer, nullable = False),
                Column('clientUsername',None, ForeignKey('clients.id'), nullable = False),
                Column('idmovieSchedule', None, ForeignKey('movieSchedule.id'), nullable = False),
                CheckConstraint(column('viewerAge') >= 0, name='age_bk_0'),
                UniqueConstraint('seatNumber', 'idmovieSchedule', name='uix_1')
            )

metadata.create_all(engineAdmin)
#----------fine tabella








#trigger = DDL(
#    "CREATE TRIGGER ins_Admin AFTER INSERT ON managers"
#    "FOR EACH ROW "
#    "WHEN (1 < (SELECT COUNT(NEW.admin) FROM managers WHERE admin == true))"
#    "BEGIN SET NEW.admin=false; END"
#)




