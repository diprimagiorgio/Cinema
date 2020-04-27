from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from app import app, engine
from sqlalchemy import *
from app.model import users

#configurazione flask_login
login_manager = LoginManager()
login_manager.init_app(app)
#flask login ha bisogno di tre cose


#---------classePerLogin
class User(UserMixin):              #in questo modo indico che estende la classe mi da a disposizione is_authenticated is_active is_anonymus, get_id
    #costruttore classe
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
#---------FineClasse



#-----callBack con il compito di trasformare un ID in un istanza della classe
@login_manager.user_loader
def load_user(user_id):
    conn = engine.connect()
    s = select([users]).where(
        and_( users.c.id == user_id )
        )
    result = conn.execute(s).fetchone()
    conn.close()
    return User(result.id, result.name, result.email, result.password)


