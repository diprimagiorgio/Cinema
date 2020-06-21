from flask import redirect, render_template, request, make_response, url_for, flash
from sqlalchemy import insert, select, join, delete, and_
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from app.model import users, movies, genres, movieSchedule, theaters, clients, managers, booking
from datetime import date, timedelta , datetime
from app import app, engine
from app.login import User, Role, login_required, login_manager
import datetime
from app.routesBooking import choicemovie
from sqlalchemy.sql.functions import now


#utlizzo l'interfaccia core e la modalita di utilizzo expression language
#TODO cercare di capire come fare, per tipo io vorrei login prima stampare la pagina e poi ricevere i dat e bello o brutto
#@login_required







@app.route('/')
def index():
    conn = engine.connect()
    if current_user.is_authenticated:
        return redirect(url_for('account_info'))         #chiamo la funzione invece del file
    return render_template("/tables/menuTable.html")

    
    
        
        
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
    
    min =date.today() - timedelta(days = 4745)
    if datetime.strptime(birthdate,"%Y-%m-%d").date()> min:
        flash("Inserisci una data di compleanno valida","error")
        return redirect ("/signIn")
    
    conn = engine.connect()
    u = select([users]).where(users.c.email == email)
    y = conn.execute(u).fetchone()
    conn.close()
    
    if y is not  None:
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
#luca
@app.route("/accountInfo")
def account_info() :
    conn = engine.connect()
    join = users.join(clients, users.c.id == clients.c.id)
    query = select([users,clients]).select_from(join).where(users.c.id == current_user.get_id())
    
    
    
    u = conn.execute(query)          #ritorna none se non contiene nessuna riga
    
    
    
                                 
    resp = make_response(render_template("accountInfo.html", infoPersonali = u))
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
        email = request.form.get("email")
        password = request.form.get("password")
        user = findUser(clients, email, password, [users])  
        if user:
            login_user(User(user.id, Role.CLIENT))
            return render_template("success.html")#------------------------------------------------------------CAMBIARE RITORNO
        flash('Email o password errate riprovare!', 'error')
    return render_template("loginClient.html")

#Giosuè Zannini
@app.route("/loginManager", methods=['POST', 'GET'])
def loginManager():
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
            return render_template("success.html")#------------------------------------------------------------CAMBIARE RITORNO
        flash('Email o password errate riprovare!', 'error')
    return render_template("loginManager.html")


#luca

    

@app.route("/updateCredit",methods = ['GET','POST'])
def change1():
    if request.method == 'POST':
        money = request.form.get("import")
        conn = engine.connect()
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
        return render_template("updateCredit.html")





#------------------------Shared function-----------------------#
def queryAndTemplate(s, htmlTemplate):
    conn = engine.connect()
    result = conn.execute(s)
    resp = make_response(render_template(htmlTemplate, result = result))
    conn.close()
    return resp

def queryAndFun(s, nameFun):
    conn = engine.connect()
    result = conn.execute(s)
    conn.close()
    return redirect(url_for(nameFun))
#--------------------------------------------------------------#
#----------------------------SHOW TIME-------------------------#
#dopo io dovrei dividere quelle passate da quelle non passate, con due visualizzazioni diverse
@app.route("/listShowsTime")
def listShowTime():
    #mostro solo i film successivi 
    s = select([movieSchedule.\
            join(movies, movieSchedule.c.idMovie == movies.c.id).\
            join(genres, genres.c.id == movies.c.idGenre)
        ])
    return queryAndTemplate(s, "listShowTime.html")

@app.route("/insertShowTime",  methods=['GET','POST'])
def insertShowTime():
    if request.method == 'POST':
        date = request.form.get('date')
        price = request.form.get('price')
        movie = request.form.get('movie')
        theater = request.form.get('theater')
        if date and price and movie and theater:
            ins = movieSchedule.insert().\
                values(dateTime = date, price = price, idMovie = movie, theater = theater)
            flash("Spettacolo inserito con successo", 'info')
            return queryAndFun(ins, 'listShowTime')
        else:
            flash('Dati mancanti', 'error')
        #devo inserire nel database
    s1 = select([theaters])#trovo tutte le sale
    s2 = select([movies])#trovo tutti i film
    conn = engine.connect()
    th = conn.execute(s1)
    mv = conn.execute(s2)
    resp = make_response(render_template("insertShowTime.html", theaters = th, movies = mv))
    conn.close()
    return resp
    
#potrei fare juna remove dove gli do
#posso dare una pagina per inserire
#--------------------------------------------------------------#
#---------------------------MOVIES-----------------------------#
@app.route("/listMovies")       #mostra Tutti Film Inseriti per accedere devi essere un utendte di un certo tipo
def listMovies():
    s = select([movies.\
            join(genres, genres.c.id == movies.c.idGenre)
        ])
    return queryAndTemplate(s, "listMovies.html")
    

#ho deciso di fare il controllo se il film è nel db o meno. Anche se non è nel db io segnalo che l'ho tolto. Ma non rombo l'integrità del db
#prima di cancellare un film però devo controllare che non si siano delle proiezioni in programma.
#TODO capire come mi devo comportare: ho pensato di mettere un radio button, dove indichi
#   se ci sono programmazioni collegate non ancora avvenute, cancellale rifiuta operazione
#   se ci sono programmazioni già avvenute, cancella o rifiuta operazione 
@app.route('/removeMovie', methods=['POST', 'GET'])
def removeMovie():                  #dovrei controllare che non ci siano date in programmazione
    if request.method == 'POST':
        id = request.form.get('id')
        if id:
            rem = movies.delete().\
                where(movies.c.id == id)
            flash("Il film è stato rimosso", 'info')                
            return queryAndFun(rem, 'listMovies')
        flash('Inserisci tutti i dati richiesti', 'error')
    s = select([movies])
    return queryAndTemplate(s, 'removeMovie.html')
#-----------------------------------------------------------#
#---------------------------SALE----------------------------#
@app.route("/listTheaters")       #mostra Tutti sale
def listTheaters():
    s = select([theaters])
    return queryAndTemplate(s, "listTheaters.html")


@app.route("/insertTheater", methods=['GET', 'POST'])
def insertTheater():
    if request.method == 'POST':
        capacity = request.form.get("capacity")
        id = request.form.get('id')
        if capacity and id and not theaterIsPresent(id):                     #verifico che mi abbiano passato i parametri e che non siano già registrate sale con lo stesso id
            ins = theaters.insert().values(id = id, seatsCapacity=capacity)
            flash("Theater insert with success!",'info' )
            return queryAndFun(ins, 'listTheaters')
        else:
            if not capacity or not id:
                flash("Dati mancanti",'error')
            else:
                flash('Theater number {} is already stored!'.format(id), 'error')
    return render_template("insertTheater.html")

def theaterIsPresent(id):                                                   #verifiche che il tetro con l'id passato sia presente del db torna boolean
    s = select([theaters]).where(theaters.c.id == id)
    conn = engine.connect()
    result = conn.execute(s).fetchone()
    conn.close()
    return True if result else False 
#prima di cancellare devo verificare che non ci siano spettacoli in quella sala
@app.route("/removeTheater", methods=['GET', 'POST'])
def removeTheater():
    if request.method == 'POST':
        id = request.form.get("id")
        if id:                                         #verifico che id sia settato 
            rem = theaters.delete().\
                where(theaters.c.id == id)
            flash('The theater {} has been removed with success'.format(id), 'info')
            return queryAndFun(rem, 'listTheaters')
        else:
            flash('You have to insert the value to remove', 'error')
    s = select([theaters])    
    return queryAndTemplate(s, "removeTheater.html")

#mancherebbe una funzione che fa l'update
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
            
            conn = engine.connect()
            ris1 = conn.execute(query).fetchone()
            queryAvgAge = select([func.avg(booking.c.viewerAge)]).select_from(s).where(movies.c.idGenre == genere)
            
            ris2 = conn.execute(queryAvgAge).fetchone()
            
            conn.close()
            
            return render_template("resultStatistiche.html",answer = ris1, genre = genere, age = ris2 )

        else:
            if sala!= 'Seleziona...' and film != 'Seleziona...'and genere =='Seleziona...':
                conn = engine.connect()
                #numeri di posti prenotati per sala per film
                s = booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id)
                queryPosti = select([func.count(booking.c.id)]).select_from(s).where(and_(movieSchedule.c.idMovie == film, movieSchedule.c.theater == sala))
                ris3 = conn.execute(queryPosti).fetchone()
                print(ris3) #risposta da mandare ad un html
                conn.close()
                
                conn = engine.connect()
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
    conn = engine.connect()
    generi = conn.execute(s2)
    sale = conn.execute(s3)
    film = conn.execute(s4)
    resp = make_response(render_template("statistiche.html", genres = generi, theaters = sale, movies = film ))
    conn.close()
    return resp
