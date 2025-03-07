from app import app, engineAdmin
from app.initializer.initializer import initializer
from flask import redirect, flash

@app.route("/init")
def init():
    initRole()
    initializer()
    flash("Database inizializzato correttamente", "info")
    return redirect('/')





def initRole():
     #-------------------------------ROLE E USER userNotLogged-----------------------------------------#
    conn = engineAdmin.connect()
    conn.execute("""
            CREATE ROLE "role_userNotLogged";
            CREATE USER "userNotLogged" WITH PASSWORD 'secret';
            """)
    conn.close()
   
    conn = engineAdmin.connect()
    conn.execute(""" 
            GRANT SELECT, INSERT ON users, clients TO "role_userNotLogged"; 
            GRANT SELECT ON managers, movies, "movieSchedule", genres, theaters TO "role_userNotLogged";
            GRANT SELECT, UPDATE ON users_id_seq TO "role_userNotLogged"; 
            GRANT "role_userNotLogged" TO "userNotLogged";
            """)
    conn.close()
    #---------------------------ROLE E USER userLogged------------------------------------------------#
    conn = engineAdmin.connect()
    conn.execute("""
            CREATE ROLE "role_userLogged"; 
            CREATE USER logged WITH PASSWORD 'secret'; 
            """)
    conn.close()
   
    conn = engineAdmin.connect()
    conn.execute(""" 
            GRANT SELECT, INSERT ON booking TO "role_userLogged";
            GRANT UPDATE (credit) ON clients TO "role_userLogged";
            GRANT SELECT, UPDATE ON booking_id_seq TO "role_userLogged"; 
            GRANT "role_userLogged",  "role_userNotLogged" TO logged; 
            """)
    conn.close()
    #---------------------ROLE E USER userLogged
    conn = engineAdmin.connect()
    conn.execute("""
            CREATE ROLE role_manager;
            CREATE USER manager WITH PASSWORD 'secret';  
            """)
    conn.close()
   
    conn = engineAdmin.connect()
    conn.execute(""" 
           GRANT SELECT, INSERT, UPDATE, DELETE ON genres, theaters, movies, "movieSchedule" TO manager;
           GRANT SELECT ON booking TO manager;
           GRANT SELECT, UPDATE ON genres_id_seq, "movieSchedule_id_seq", movies_id_seq, theaters_id_seq TO role_manager; 
           GRANT role_manager TO manager; 
            """)
    conn.close()

