from flask import Flask
import sqlalchemy
import psycopg2
from sqlalchemy import create_engine, MetaData

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Sq9obiBTY7hyb10ga9lja5MgYQNz' 

engineAdmin = create_engine(
    'postgresql://admin_ilmolo:secret@localhost/cinemaIlMolo',
    isolation_level='REPEATABLE READ'
)
engineUserNotLogged = create_engine(
    'postgresql://userNotLogged:secret@localhost/cinemaIlMolo',
    isolation_level='REPEATABLE READ'
)
engineUserLogged = create_engine(
    'postgresql://logged:secret@localhost/cinemaIlMolo',
    isolation_level='REPEATABLE READ'
)
engineManager = create_engine(
    'postgresql://manager:secret@localhost/cinemaIlMolo',
    isolation_level='REPEATABLE READ'
)

metadata = MetaData ()

from app import model
from app.shared import login
from app import routes
from app.initializer import role

from app.manager.tableRoutes import movie, movieSchedule, theater, genre
from app.user import pay, personalClient
from app.manager import verifyBooking, statistiche
from app.manager import personalArea

from app.user import routesBooking