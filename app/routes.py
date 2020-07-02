from flask import redirect, render_template, request, make_response, url_for, flash
from sqlalchemy import insert, select, join, delete, and_, bindparam, func
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from app.model import users, movies, genres, movieSchedule, theaters, clients, managers, booking
from datetime import date, timedelta , datetime
from app import app
from app.shared.login import User, Role, login_required, login_manager, findUser
from app.engineFunc import choiceEngine
from sqlalchemy.sql.functions import now

@app.route('/')
def index():
    if current_user.is_authenticated and current_user.role > Role.CLIENT:
        return render_template("/manager/shared/layout.html")
    return render_template("/user/shared/layout.html")

@app.route('/logout')
@login_required()
def logout():
    logout_user()
    return redirect('/')

#Luca Bizzotto
#registrazione manager
@app.route('/registerManager',methods= ['GET','POST'])
@login_required(Role.SUPERVISOR)
def registerManager():
    if request.method == 'POST': 
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("email")
        password = request.form.get("password")
        if not name or not email or not password or not surname :#controllo non ci siano valori mancanti 
            flash("Devi inserire tutti i dati")#in caso mando un errore 
            return redirect ("/registerManager")
        conn = choiceEngine()
        #mi serve per controllare che la mail inserita non sia gia stata utilizzata
        u = select([users]).where(users.c.email == bindparam('email'))
        y = conn.execute(u,{'email': email}).fetchone()
        conn.close()
        if y is not None:
            flash('Email gia usata, riprova con un altra!', 'error') 
            return redirect('/registerManager')

        conn = choiceEngine()
        #insert sulla tabella users
        ins = users.insert(None).values(name=bindparam('name'), surname = bindparam('surname'), email = bindparam('email'), password = bindparam('password') )   
        conn.execute(ins,{'name': name, 'surname': surname, 'email': email, 'password': password})
        conn.close()

        conn = choiceEngine()
        query = select([users]).where(users.c.email == bindparam('email'))
        #mi serve per ritrovarmi l'ID corretto ed effettuare il giusto inserimento nella tabella user
        ris = conn.execute(query,{'email': email}).fetchone()
        insmanager= managers.insert(None).values(id = ris.id,admin = False , financialReport=None)
        conn.execute(insmanager)
        conn.close()
        return redirect("/")
    return render_template("/manager/admin/registerManager.html")

#Luca Bizzotto
# Registrazione del cliente 
@app.route('/register', methods =['GET','POST'] )
def register():
    if request.method == 'POST':
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("email")
        password = request.form.get("password")
        birthdate = request.form.get("birthdate")
        if not name or not email or not password or not birthdate or not surname :
            flash("Devi inserire tutti i dati")
            return redirect ("/register")
        #eta' minima di iscrizione 13 anni 
        min =date.today() - timedelta(days = 4745)
        if datetime.strptime(birthdate,"%Y-%m-%d").date()> min:#mi serve per convertire una stringa in un tipo datetime
            flash("Inserisci una data di compleanno valida","error")
            return redirect ("/register")
        conn = choiceEngine()
        #mi serve per controllare la mail inserita non sia gia stata utilizzata
        u = select([users]).where(users.c.email == bindparam('email'))
        y = conn.execute(u,{'email':email}).fetchone()
        conn.close()
        if y is not None:
            flash('Email gia usata, riprova con un altra!', 'error') 
            return redirect('/register')
        conn = choiceEngine()
        ins = users.insert(None).values(name= bindparam('name'), surname = bindparam('surname'), email = bindparam('email'), password = bindparam('password'))    
        conn.execute(ins,{'name': name, 'surname': surname,'email': email,'password': password})
        conn.close()
        conn = choiceEngine()
        query = select([users]).where(users.c.email == bindparam('email'))
        ris = conn.execute(query,{'email': email}).fetchone()
        insclients= clients.insert(None).values(id = ris.id, birthDate = birthdate, credit=0.)
        conn.execute(insclients)
        conn.close()
        flash('Ti sei registrato correttamente!', 'info') 

        return redirect("/")
    return render_template("/user/noLogged/register.html") 


#Giosuè Zannini
@app.route("/loginClient", methods=['POST', 'GET'])
def loginClient():
    if current_user.is_authenticated:
        flash('Sei già loggato', 'error')
        return redirect("/")
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = findUser(clients, email, password, [users])  
        
        if user:
            login_user(User(user.id, Role.CLIENT))
            flash('Loggato correttamente', 'info')
            return redirect("/choiceMovie")
        flash('Email o password errate riprovare!', 'error')
    return render_template("/user/noLogged/loginClient.html")


#Giosuè Zannini
@app.route("/loginManager", methods=['POST', 'GET'])
def loginManager():
    if current_user.is_authenticated: 
        flash('Sei già loggato', 'error') 
        return redirect("/")
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        user = findUser(managers, email, password, [users, managers.c.admin])
        if user:
            if user.admin:
                role = Role.ADMIN
            else:
                role = Role.SUPERVISOR
            login_user(User(user.id, role))
            if current_user.role == Role.SUPERVISOR:
                return render_template("/tables/menuTable.html")
            else:
                return redirect("/financialReport")
        flash('Email o password errate riprovare!', 'error')       
    return render_template("/manager/shared/loginManager.html")