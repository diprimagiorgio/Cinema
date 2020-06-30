import sqlalchemy
from app.shared.login import Role, current_user
from app import engineAdmin, engineManager, engineUserLogged, engineUserNotLogged




def choiceEngine():
    if not current_user.is_authenticated:
        conn = engineUserNotLogged.connect()
    if current_user.is_authenticated:
        if current_user.role == Role.CLIENT:
            conn = engineUserLogged.connect()
        if current_user.role == Role.SUPERVISOR:
            conn = engineManager.connect()
        else:
            conn = engineAdmin.connect()
    return conn
        