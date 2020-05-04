from flask import redirect, render_template, request, make_response, url_for, flash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from sqlalchemy import *

from app.model import users, clients, managers           #circular input
from app import app, engine
from app.login import User, Role, login_required

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
@login_required()
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
@login_required()
def registrants():
    conn = engine.connect()
    s = select([users])
    result = conn.execute(s)
    resp = make_response(render_template("registred.html", students = result))
    conn.close()
    return resp



@app.route("/loginClient", methods=['POST', 'GET'])
def loginAttempt1():
    if(request.method == 'POST'):
        email = request.form.get("email");
        password = request.form.get("password")
        conn = engine.connect()
        join = users.join(clients, users.c.id == clients.c.id)
        query = select([users]).select_from(join).where(and_(users.c.email == email, users.c.password == password))
        user = conn.execute(query).fetchone()            #ritorna none se non contiene nessuna riga
        conn.close()  
        if user:
            login_user(User(user.id, Role.C))
            return render_template("success.html")
        flash('Email o password errate riprovare!')#con questo metodo scrivo un messaggio di errore nel html
    return render_template("login.html")



@app.route("/loginManager", methods=['POST', 'GET'])
def loginAttempt2():
    if(request.method == 'POST'):
        email = request.form.get("email");
        password = request.form.get("password")
        conn = engine.connect()
        join = users.join(managers, users.c.id == managers.c.id)
        query = select([users]).select_from(join).where(and_(users.c.email == email, users.c.password == password))
        user = conn.execute(query).fetchone()            #ritorna none se non contiene nessuna riga
        conn.close()
        if user:
            login_user(User(user.id, Role.M))
            return render_template("success.html")
        flash('Email o password errate riprovare!')#con questo metodo scrivo un messaggio di errore nel html
    return render_template("loginManager.html")
