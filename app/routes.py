from flask import redirect, render_template, request, make_response, url_for, flash
from sqlalchemy import insert, select, join, delete, and_, bindparam
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user

from app.model import users,clients, managers
from app import app, engine
from app.login import User, Role, login_required, current_user                           #qui ho aggiunto current user perchè c'e nel layout
import time


#utlizzo l'interfaccia core e la modalita di utilizzo expression language

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('account_info'))         #chiamo la funzione invece del file
    return render_template("menuTable.html")

@app.route('/signIn')
def singIn():
    return render_template("register.html")

@app.route('/logout')
@login_required()
def logout():
    logout_user()
    return redirect(url_for('index'))

#luca
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
#luca
@app.route("/account_info")
def account_info() :
    conn = engine.connect()
    s = select([clients])
    result = conn.execute(s)
    resp = make_response(render_template("account_info.html", students = result))
    conn.close()
    return resp



#giosuè
@app.route("/loginClient", methods=['POST', 'GET'])
def loginAttempt1():
    if(request.method == 'POST'):
        email = request.form.get("email")
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
#luca
@app.route("/updatecredit1")
@login_required()#richiede utente loggato
def change():
    return render_template("updatecredit.html")

@app.route("/updatecredit2",methods = ['POST'])
def change1():
    money = request.form.get("import")
    conn = engine.connect()
    base = select([clients]).where(clients.columns.id == current_user.get_id())
    ris = conn.execute(base).fetchone()
    query = clients.update().values(credit = float(money) + float(ris.credit)).where(clients.columns.id == current_user.get_id())
    conn.execute(query)
    conn.close()
    return render_template("login.html")



#giosuè
@app.route("/loginManager", methods=['POST', 'GET'])
def loginAttempt2():
    if(request.method == 'POST'):
        email = request.form.get("email")
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

@app.route("/pay/<id_cl>/<amount>")
def paga(id_cl, amount):
    if(pay(id_cl, amount)):
        return "Pagamento è andato a buon fine"
    else:
        return "Pagamento FALLITO"


"""
    Devo prendere un amount da un cliente e trasferirlo all'amministartore
"""
def pay(id, amount):
    conn = engine.connect()
    trans = conn.begin()
    try:
        #verifico che l'utente abbia un credito sufficiente
        s_cl = select([clients]).\
                    where( 
                        and_( 
                                clients.c.id == bindparam('id'),
                                clients.c.credit >= bindparam('amount') 
                        )
                    )
        result = conn.execute(s_cl,  {'id' : id, 'amount' : amount}).fetchone()
        if not result:
            raise
        #rimuovo il credito dall'utente
        u_cl = clients.update().\
                    where(clients.c.id == bindparam('id_cl')).\
                    values( credit =  result['credit'] - float(amount) )

        conn.execute(u_cl, {'id_cl' : id})
        time.sleep(30)
        #selezione dell'id del manager
        s_mn = select([managers]).\
                where(managers.c.admin == True)
        result = conn.execute(s_mn).fetchone()
        #decremento il bilancio dell'amministratore
        u_mn = managers.update().\
                where(managers.c.id == result['id']).\
                values( financialReport = result['financialReport'] + float(amount) )
        conn.execute(u_mn)

        trans.commit()
        resp = True
    except:
        trans.rollback()
        resp = False
    finally:
        conn.close()
        trans.close()
        return resp