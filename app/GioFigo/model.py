from sqlalchemy import Table, Column,  Integer, String
from GioFigo import metadata, engine
#--------tabella
users = Table( 'users', metadata,
    Column('id', Integer, primary_key = True, autoincrement=True),
    Column('name', String),
    Column('email', String, unique = True),
    Column('password', String)
)
metadata.create_all(engine)
#----------fine tabella