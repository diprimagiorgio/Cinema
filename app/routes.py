from flask import redirect, render_template, request, make_response, url_for, flash
from sqlalchemy import insert, select, join, delete, and_
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from app.model import users, movies, genres, movieSchedule, theaters, clients, managers, booking
from datetime import date, timedelta , datetime
from app import app, engine
from app.login import User, Role, login_required, login_manager
from app.routesBooking import choicemovie
from sqlalchemy.sql.functions import now


#utlizzo l'interfaccia core e la modalita di utilizzo expression language
#TODO cercare di capire come fare, per tipo io vorrei login prima stampare la pagina e poi ricevere i dat e bello o brutto
#@login_required







@app.route('/')
def index():
    if current_user.is_authenticated and current_user.role > Role.CLIENT:
        return render_template("/manager/shared/layout.html")
    return render_template("/user/shared/layout.html")

@app.route('/dataBase')
def dataBase():
    return render_template("/tables/menuTable.html")
    
    


@app.route('/logout')
@login_required()
def logout():
    logout_user()
    return redirect(url_for('index'))

#Luca Bizzotto
@app.route('/registerManager',methods= ['GET','POST'])
def registerManager():
    if request.method == 'POST': 
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("email")
        password = request.form.get("password")
        if not name or not email or not password or not surname :
            flash("Devi inserire tutti i dati")
            return redirect ("/registerManager")
        conn = engine.connect()
        u = select([users]).where(users.c.email == email)#mi serve per contrallare che la mail inserita non sia gia stata utilizzata
        y = conn.execute(u).fetchone()
        conn.close()
        if y is not None:
            flash('Email gia usata, riprova con un altra!', 'error') 
            return redirect('/registerManager')
        conn = engine.connect()
        ins = users.insert(None).values(name=name, surname = surname, email = email, password = password)    
        conn.execute(ins)
        conn.close()
        conn = engine.connect()
        query = select([users]).where(users.c.email == email)#mi serve per ritrovarmi l'ID corretto
        ris = conn.execute(query).fetchone()
        insmanager= managers.insert(None).values(id = ris.id,admin = False , financialReport=None)
        conn.execute(insmanager)
        conn.close()
        return redirect("/")
    return render_template("/user/noLogged/registerManager.html")

#Luca Bizzotto
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
            return redirect ("/signIn")
        min =date.today() - timedelta(days = 4745)
        if datetime.strptime(birthdate,"%Y-%m-%d").date()> min:
            flash("Inserisci una data di compleanno valida","error")
            return redirect ("/register")
        conn = engine.connect()
        u = select([users]).where(users.c.email == email)#mi serve per contrallare che la mail inserita non sia gia stata utilizzata
        y = conn.execute(u).fetchone()
        conn.close()
        if y is not None:
            flash('Email gia usata, riprova con un altra!', 'error') 
            return redirect('/signIn')
        conn = engine.connect()
        ins = users.insert(None).values(name=name, surname = surname, email = email, password = password)    
        conn.execute(ins)
        conn.close()
        conn = engine.connect()
        query = select([users]).where(users.c.email == email)
        ris = conn.execute(query).fetchone()
        insclients= clients.insert(None).values(id = ris.id, birthDate = birthdate, credit=0.)
        conn.execute(insclients)
        conn.close()

        return redirect("/")
    return render_template("/user/noLogged/register.html") 

#Luca Bizzotto
@app.route("/accountInfo")
def account_info() :
    conn = engine.connect()
    join = users.join(clients, users.c.id == clients.c.id)
    query = select([users,clients]).select_from(join).where(users.c.id == current_user.get_id())
    u = conn.execute(query)          #ritorna none se non contiene nessuna riga
    resp = make_response(render_template("/user/logged/accountInfo.html", infoPersonali = u))
    conn.close()
    return resp


#Giosuè Zannini
#------------------------Shared function Login-----------------------#

def findUser(table, email, password, sel):
    conn = engine.connect()
    query = select(sel).\
            select_from(users.join(table)).\
            where(and_(users.c.email == email, users.c.password == password))
    user = conn.execute(query).fetchone()            #ritorna none se non contiene nessuna riga
    conn.close()
    return user
#--------------------------------------------------------------#

    

#Giosuè Zannini
@app.route("/loginClient", methods=['POST', 'GET'])
def loginClient():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            email = request.form.get("email")
            password = request.form.get("password")
            user = findUser(clients, email, password, [users])  
            if user:
                login_user(User(user.id, Role.CLIENT))
                flash('Loggato correttamente', 'info')
                return render_template("/user/shared/layout.html")
            flash('Email o password errate riprovare!', 'error')
        else:
            flash('Sei già loggato', 'error')
    return render_template("/user/noLogged/loginClient.html")

#Giosuè Zannini
@app.route("/loginManager", methods=['POST', 'GET'])
def loginManager():
    if request.method == 'POST':
        if not current_user.is_authenticated: 
            email = request.form.get("email")
            password = request.form.get("password")
            user = findUser(managers, email, password, [users, managers.c.admin])
            if user:
                if user.admin:
                    role = Role.ADMIN
                else:
                    role = Role.SUPERVISOR
                login_user(User(user.id, role))
                return render_template("/manager/shared/layout.html")
            flash('Email o password errate riprovare!', 'error')
        else:
            flash('Sei già loggato', 'error')        
    return render_template("/manager/shared/loginManager.html")

    #potrei fare che se admin vedo 
    #               il bilancio
    #               la possibilità di registrare menager
    #               le tabelle 

    #se manager vede le tabelle




    
#Luca Bizzotto
@app.route("/updateCredit",methods = ['GET','POST'])
def change1():
    if request.method == 'POST':
        money = request.form.get("import")
        conn = engine.connect()
        base = select([clients]).where(clients.c.id == current_user.get_id())
        ris = conn.execute(base).fetchone()
        if float(money) < 0 :
            flash("Non puoi inserire valori negativi!",'error')
            return redirect("/updateCredit")
        query = clients.update().values(credit = float(money) + float(ris.credit)).where(clients.c.id == current_user.get_id())
        flash("Ricarica avvenuta con successo!",'info' )
        conn.execute(query)
        conn.close()
        return redirect("/updateCredit")
    else:
        return render_template("/user/logged/updateCredit.html")




