from flask import redirect, render_template, request, make_response, url_for, flash
from sqlalchemy import insert, select, join, delete, and_
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from app.model import users, movies, genres, movieSchedule, theaters, clients, managers, booking
from datetime import date, timedelta , datetime
from app import app
from app.login import User, Role, login_required, login_manager, findUser
from app.engineFunc import choiceEngine
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
    
@app.route('/financialReport')
def financialReport():
    sel = select([managers]).\
            where( managers.c.admin == True)
    conn = choiceEngine()
    res = conn.execute(sel).fetchone()
    conn.close()
    return render_template("/manager/admin/financialReport.html", result = res)

    
    

        #è scritto sbagliato e sarebbe meglio fare tutto in una funzione
@app.route('/signIn')
def singIn():
    return render_template("/user/noLogged/register.html")

@app.route('/logout')
@login_required()
def logout():
    logout_user()
    return redirect('/')

@app.route('/registerManager',methods= ['GET','POST'])
def registerManager():
    if request.method == 'POST': 
        
        name = request.form.get("name")
        print(name)
        surname = request.form.get("surname")
        email = request.form.get("email")
        password = request.form.get("password")
        if not name or not email or not password or not surname :
            flash("Devi inserire tutti i dati")
            return redirect ("/registerManager")
        conn = choiceEngine()
        u = select([users]).where(users.c.email == email)#mi serve per contrallare che la mail inserita non sia gia stata utilizzata
        y = conn.execute(u).fetchone()
        conn.close()

        if y is not None:
            flash('Email gia usata, riprova con un altra!', 'error') 
            return redirect('/registerManager')



        conn = choiceEngine()
        ins = users.insert(None).values(name=name, surname = surname, email = email, password = password)    
        conn.execute(ins)
        conn.close()

        conn = choiceEngine()
        query = select([users]).where(users.c.email == email)#mi serve per ritrovarmi l'ID corretto
        ris = conn.execute(query).fetchone()
        insmanager= managers.insert(None).values(id = ris.id,admin = False , financialReport=None)
        conn.execute(insmanager)
        conn.close()

        return redirect("/")

        

    return render_template("/user/noLogged/registerManager.html")





#luca
@app.route('/register', methods =['POST'] )
def register():
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
        return redirect ("/signIn")
    
    #conn = engine.connect()
    conn = choiceEngine()#-------------------------------------------------------
    u = select([users]).where(users.c.email == email)#mi serve per contrallare che la mail inserita non sia gia stata utilizzata
    y = conn.execute(u).fetchone()
    conn.close()
    
    if y is not None:
        flash('Email gia usata, riprova con un altra!', 'error') 
        return redirect('/signIn')
    
    
    
    conn = choiceEngine()
    ins = users.insert(None).values(name=name, surname = surname, email = email, password = password)    
    conn.execute(ins)
    conn.close()
    
    conn = choiceEngine()
    query = select([users]).where(users.c.email == email)
    ris = conn.execute(query).fetchone()
    insclients= clients.insert(None).values(id = ris.id, birthDate = birthdate, credit=0.)
    conn.execute(insclients)
    conn.close()
    
    return redirect("/")
#luca
@app.route("/accountInfo")
def account_info() :
    conn = choiceEngine()
    join = users.join(clients, users.c.id == clients.c.id)
    query = select([users,clients]).select_from(join).where(users.c.id == current_user.get_id())
    
    
    
    u = conn.execute(query)          #ritorna none se non contiene nessuna riga
    
    
    
                                 
    resp = make_response(render_template("/user/logged/accountInfo.html", infoPersonali = u))
    conn.close()
    return resp


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

    #potrei fare che se admin vedo 
    #               il bilancio
    #               la possibilità di registrare menager
    #               le tabelle 

    #se manager vede le tabelle


#luca

    

@app.route("/updateCredit",methods = ['GET','POST'])
def change1():
    if request.method == 'POST':
        money = request.form.get("import")
        conn = choiceEngine()
        base = select([clients]).where(clients.c.id == current_user.get_id())
        ris = conn.execute(base).fetchone()
        if float(money) < 0 :
            flash("you can't insert neagtive value!",'error')
            return redirect("/updateCredit")
        query = clients.update().values(credit = float(money) + float(ris.credit)).where(clients.c.id == current_user.get_id())
        flash("Recharge with success!",'info' )
        conn.execute(query)
        conn.close()
        return redirect("/updateCredit")
    else:
        return render_template("/user/logged/updateCredit.html")




#-----------------------------------------------------------#
app.route("/statistiche",  methods=['GET','POST'])
def statistiche():
    
    if request.method == 'POST':        
        genere= request.form.get('genere')
        sala= request.form.get('sale')
        film= request.form.get('film')
        if genere != 'Seleziona...':
            
            s = booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).join(movies, movieSchedule.c.idMovie == movies.c.id)
            query = select([func.count(booking.c.id)]).select_from(s).where(movies.c.idGenre == genere)
            
            conn = choiceEngine()
            ris1 = conn.execute(query).fetchone()
            queryAvgAge = select([func.avg(booking.c.viewerAge)]).select_from(s).where(movies.c.idGenre == genere)
            
            ris2 = conn.execute(queryAvgAge).fetchone()
            
            conn.close()
            
            return render_template("resultStatistiche.html",answer = ris1, genre = genere, age = ris2 )

        else:
            if sala!= 'Seleziona...' and film != 'Seleziona...'and genere =='Seleziona...':
                conn = choiceEngine()
                #numeri di posti prenotati per sala per film
                s = booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id)
                queryPosti = select([func.count(booking.c.id)]).select_from(s).where(and_(movieSchedule.c.idMovie == film, movieSchedule.c.theater == sala))
                ris3 = conn.execute(queryPosti).fetchone()
                print(ris3) #risposta da mandare ad un html
                conn.close()
                
                conn = choiceEngine()
                #incasso per film
                s = booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id)
                querynumeroPrenotazioni = select([func.sum(movieSchedule.c.price)]).select_from(s).where(movieSchedule.c.idMovie == film)
            
                ris4 = conn.execute(querynumeroPrenotazioni).fetchone()
                print(ris4)
                conn.close()
                
                
                
            flash('Dati mancanti', 'error')
    s2 = select([genres])#trovo tutti i generi
    s3 = select([theaters])#trovo tutte le sale
    s41 = movieSchedule.join(movies, movieSchedule.c.idMovie== movies.c.id)
    #s4 = select([func.distinct(movies.c.id),movies.c.title]).select_from(s41).order_by(movies.c.title)#trovo solo i film con prenotazioni mi manca il count distinct 
    s4 = select([movies]).select_from(s41).order_by(movies.c.title)
    conn = choiceEngine()
    generi = conn.execute(s2)
    sale = conn.execute(s3)
    film = conn.execute(s4)
    resp = make_response(render_template("statistiche.html", genres = generi, theaters = sale, movies = film ))
    conn.close()
    return resp
