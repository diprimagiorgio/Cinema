from flask_login import LoginManager, UserMixin, current_user
from app import app, engine

from enum import Enum

from sqlalchemy import select

from app.model import users, clients, managers

from functools import wraps

from flask import current_app







#configurazione flask_login
login_manager = LoginManager()
login_manager.init_app(app)
#flask login ha bisogno di tre cose


#---------classePerLogin
class User(UserMixin):              #in questo modo indico che estende la classe mi da a disposizione is_authenticated is_active is_anonymus, get_id
    #costruttore classe
    def __init__(self, id, role):
        self.id = id
        self.role = role
    
#---------FineClasse
#---------Classe per il ruolo
class Role(Enum):
    C = 'CLIENT'
    M = 'MANAGER'
    



#-----callBack con il compito di trasformare un ID in un istanza della classe
@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    join = users.join(clients, users.c.id == clients.c.id)
    query = select([users]).select_from(join).where(users.c.id == user_id)
    result = conn.execute(query).fetchone()
    role = Role.C
    if not result:
        join = users.join(managers, users.c.id == managers.c.id)
        query = select([users]).select_from(join).where(users.c.id == user_id)
        result = conn.execute(query).fetchone()
        role = Role.M
    conn.close()
    return User(result.id, role)



#------------------------------------------OVERRIDE
#utilizzo:  quando si usa il decoratore se non si mette dentro parentesi nulla possono accedere tutti 
#           gli utenti loggati, invece se si specifica un ruolo può accedere solo quel ruolo in specifico
def login_required(role='ANY'):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_app.config.get('LOGIN_DISABLED'):
                return func(*args, **kwargs)
            elif not current_user.is_authenticated or ((current_user.role != role) and (role != "ANY")):
                return current_app.login_manager.unauthorized()
            return func(*args, **kwargs)
        return decorated_view
    return wrapper







