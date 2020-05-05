from flask import redirect, render_template, request, make_response, url_for, flash
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
from sqlalchemy import insert, select, join, delete

from app.model import users,movies,genres,movieSchedule, theaters          #circular input
from app import app, engine
from app.login import User

#utlizzo l'interfaccia core e la modalita di utilizzo expression language
#TODO cercare di capire come fare, per tipo io vorrei login prima stampare la pagina e poi ricevere i dat e bello o brutto
#@login_required
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
    ins = users.insert(None).values( name=name, email = email, password = password)
    conn.execute(ins)
    conn.close()
    return redirect("/")



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


@app.route("/insertMovie", methods=['GET','POST'])
def insertMovie():
    if request.method == 'POST':
        title = request.form.get("title")
        age = request.form.get("age")
        duration = request.form.get("duration")
        genre = request.form.get("genre")
        if title and age and duration and genre:
            ins = movies.insert().values(title =title , minimumAge = age, duration = duration, idGenre = genre)
            flash("Movie insert with success", 'info')
            return queryAndFun(ins, 'listMovies')
        flash("Dati mancanti", 'error')
    s = select([genres])
    return queryAndTemplate(s,"insertMovie.html")

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
            return queryAndFun(ins, 'listTheater')
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

@app.route("/removeTheater", methods=['GET', 'POST'])
def removeTheater():
    if request.method == 'POST':
        id = request.form.get("id")
        if id:                                         #verifico che id sia settato 
            rem = theaters.delete().\
                where(theaters.c.id == id)
            flash('The theater {} has been removed with success'.format(id), 'info')
            return queryAndFun(rem, 'listTheater')
        else:
            flash('You have to insert the value to remove', 'error')
    s = select([theaters])    
    return queryAndTemplate(s, "removeTheater.html")

#mancherebbe una funzione che fa l'update
#-----------------------------------------------------------#
