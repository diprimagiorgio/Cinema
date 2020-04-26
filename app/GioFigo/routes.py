from flask import redirect, render_template, request, make_response, url_for
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from sqlalchemy import *

from GioFigo.model import users             #circular input
from GioFigo import app, engine
from GioFigo.login import User

#utlizzo l'interfaccia core e la modalità di utilizzo expression language




#TODO cercare di capire come fare, per tipo io vorrei login prima stampare la pagina e poi ricevere i dat è bello o brutto




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
    email = request.form.get("email")
    password = request.form.get("password")
    if not name or not email or not password:
        return render_template("failure.html",message =  "Devi inserire tutti i dati")
    conn = engine.connect()
    ins = users.insert().values( name=name, email = email, password = password)
    conn.execute(ins)
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










@app.route("/loginAttempt", methods=['POST'])
def loginAttempt():
    email = request.form.get("name");
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


