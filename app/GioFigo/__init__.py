from flask import Flask
import sqlalchemy
from sqlalchemy import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'prova' #is used to keep the client-side session secure

#utlizzo l'interfaccia core e la modalità di utilizzo expression language
engine = create_engine('sqlite:///site.db')
metadata = MetaData ()
from GioFigo import login
from GioFigo import routes


