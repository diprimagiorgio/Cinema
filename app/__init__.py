from flask import Flask
import sqlalchemy
import psycopg2

from sqlalchemy import create_engine, MetaData

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Sq9obiBTY7hyb10ga9lja5MgYQNz' #is used to keep the client-side session secure


#I'm using core and expression language

engine = create_engine(
    'postgresql://admin_ilmolo:secret@localhost/cinemaIlMolo',
    isolation_level='SERIALIZABLE',
    echo = True
)
engine1 = create_engine(
    'postgresql://userNotLogged:secret@localhost/cinemaIlMolo',
)
engine2 = create_engine(
    'postgresql://logged:secret@localhost/cinemaIlMolo',
)
engine2 = create_engine(
    'postgresql://manager:secret@localhost/cinemaIlMolo',
)




metadata = MetaData ()

from app import model
from app import login
from app import routes
from app import statistiche
from app import role

from app.tableRoutes import movie, movieSchedule, theater, genre
from app import initializer, pay, routesBooking, verifyBooking
#bisogna fare anche per genre

