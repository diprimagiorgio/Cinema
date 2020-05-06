from flask import redirect, render_template, request, make_response, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from sqlalchemy import *

from app.model import users, clients, managers, theaters, movies, genreMovies, genres, movieShedule, booking         #circular input
from app import app, engine
from app.login import User

#utlizzo l'interfaccia core e la modalita di utilizzo expression language




#TODO cercare di capire come fare, per tipo io vorrei login prima stampare la pagina e poi ricevere i dat e bello o brutto




@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('registrants'))         #chiamo la funzione invece del file
    return render_template("login.html")

@app.route('/signIn')
def singIn():
    return render_template("register.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods =['POST'] )
def register():
    name = request.form.get("name")
    surname = request.form.get("surname")
    email = request.form.get("email")
    password = request.form.get("password")
    birthdate = request.form.get("birthdate")
    if not name or not email or not password or not birthdate or not surname :
        return render_template("failure.html",message =  "Devi inserire tutti i dati")
    conn = engine.connect()
    ins = users.insert(None).values(name=name, surname = surname, email = email, password = password)    
    conn.execute(ins)
    conn.close()
    
    conn = engine.connect()
    query = select([users]).where(users.columns.email == email)
    ris = conn.execute(query).fetchone()
    insclients= clients.insert(None).values(id = ris.id, birthDate = birthdate, credit=0.)
    conn.execute(insclients)
    conn.close()
    
    return redirect("/")

@app.route("/registred")
@login_required
def registrants():
    conn = engine.connect()
    s = select([users])
    result = conn.execute(s)
    resp = make_response(render_template("registred.html", students = result))
    conn.close()
    return resp
@app.route("/login")
def login():
    return render_template("login.html")



def load_user_temp(user_id):
    conn = engine.connect()
    s = select([users]).where(
        and_( users.c.id == user_id )
        )
    result = conn.execute(s).fetchone()
    conn.close()
    return User(result.id, result.name, result.email, result.password)

@app.route("/account_info")
def account_info() :
    conn = engine.connect()
    s = select([clients])
    result = conn.execute(s)
    resp = make_response(render_template("account_info.html", students = result))
    conn.close()
    return resp

@app.route("/updatecredit1")
@login_required#richiede utente loggato
def change():
    return render_template("updatecredit.html")

@app.route("/updatecredit2",methods = ['POST'])###non funzia
def change1():
    money = request.form.get("import")
    conn = engine.connect()
    base = select([clients]).where(clients.columns.id == current_user.get_id())
    ris = conn.execute(base).fetchone()
    query = clients.update().values(credit = float(money) + float(ris.credit)).where(clients.columns.id == current_user.get_id())
    conn.execute(query)
    conn.close()
    return render_template("login.html")
    










@app.route("/loginAttempt", methods=['POST'])
def loginAttempt():
    email = request.form.get("name")
    password = request.form.get("password")
    if not email or not password:
        return render_template("failure.html", message = "Dati mancanti" + email + password)
    conn = engine.connect()
    s = select([users]).where(
        and_( users.c.email == email,
            users.c.password == password)
        )
    result = conn.execute(s).fetchone()            #ritorna none se non contirnr nessuna riga
    #TODO PROVARE CON IL COSTRUTTO DEL PROF OSSIA FETCH ONE -> io ho usato first
    conn.close()
    if not result:
        return render_template("failure.html", message = "password o email non corretti")
    else:
        user = load_user_temp(result['id'])              #dovrebbe andare anche con result.id
        login_user(user)
        return render_template("success.html", student = result)


