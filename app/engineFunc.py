import sqlalchemy
from app.login import Role, current_user




def choiceEngine():
    if not current_user.is_authenticated:
        conn = engine1.connect()
    if current_user.is_authenticated:
        if current_user.Role == Role.CLIENT:
            conn = engineUserLogged.connect()
        if current_user.Role == Role.SUPERVISOR:
            conn = engineManager.connect()
        else:
            conn = engineAdmin.connect()
    return conn
        