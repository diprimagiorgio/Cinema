from flask import Flask
import sqlalchemy
import psycopg2

from sqlalchemy import create_engine, MetaData

app = Flask(__name__)
app.config['SECRET_KEY'] = 'prova' #is used to keep the client-side session secure


#I'm using core and expression language

engine = create_engine(
    'postgresql://admin:secret@localhost/cinemaIlMolo',
    isolation_level='REPEATABLE_READ',
    echo = True
)
metadata = MetaData ()


from app import login
from app import routes
from app.tableRoutes import movie, movieSchedule, theater, genre
from app import initializer, pay
#bisogna fare anche per genre

