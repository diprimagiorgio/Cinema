from flask_login import LoginManager, UserMixin, current_user
from app import app, engineAdmin
from enum import IntEnum
from sqlalchemy import select, and_, bindparam
from app.model import users, clients, managers
from functools import wraps
from flask import redirect, flash


#configurazione flask_login
login_manager = LoginManager()
login_manager.init_app(app)



#---------classePerLogin
class User(UserMixin):              #in questo modo indico che estende la classe mi da a disposizione is_authenticated is_active is_anonymus, get_id
    #costruttore classe
    def __init__(self, id, role):
        self.id = id
        self.role = role
    
#---------FineClasse

#---------Classe per il ruolo
#Giosuè Zannini
class Role(IntEnum):
    CLIENT = 0
    SUPERVISOR = 1
    ADMIN = 2
    
    
#from app.engineFunc import choiceEngine
    
#Giosuè Zannini
#------------------------Shared function Login-----------------------#

def findUser(table, email, password, sel):
    conn = engineAdmin.connect()
    #ritorna un utente
    query = select(sel).\
            select_from(users.join(table)).\
            where(and_(users.c.email == bindparam('email'), users.c.password == bindparam('password')))
    user = conn.execute(query, {'email' : email, 'password' : password}).fetchone()            #ritorna none se non contiene nessuna riga
    conn.close()
    return user
#--------------------------------------------------------------#



#-----callBack con il compito di trasformare un ID in un istanza della classe
#Giosuè Zannini
@login_manager.user_loader
def load_user(user_id):
    conn = engineAdmin.connect()
    query = select([clients]).\
            where(clients.c.id == user_id)
    result = conn.execute(query).fetchone()
    role = Role.CLIENT
    if not result:
        query = select([managers]).\
                where(managers.c.id == user_id)
        result = conn.execute(query).fetchone()
        if result['admin']:
            role = Role.ADMIN
        else:
            role = Role.SUPERVISOR
    conn.close()
    return User(result['id'], role)



#------------------------------------------OVERRIDE
#utilizzo:  quando si usa il decoratore se non si mette dentro parentesi nulla possono accedere tutti 
#           gli utenti loggati, invece se si specifica un ruolo può accedere solo quel ruolo in specifico
#Giosuè Zannini
def login_required(role = 0):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if app.config.get('LOGIN_DISABLED'):
                return func(*args, **kwargs)
            elif not current_user.is_authenticated or current_user.role < role:
                return app.login_manager.unauthorized()
            return func(*args, **kwargs)
        return decorated_view
    return wrapper


#-----------------------------------------GESTISCE LA PAGINA DI RITORNO IN CASO DI ACCESSO NON CONSENTITO A QUALCHE PAGINA
#Giosuè Zannini
@app.login_manager.unauthorized_handler
def unauth_handler():
    flash('Non sei autorizzato ad accedere a quest\'area', 'error')
    return redirect("/")




