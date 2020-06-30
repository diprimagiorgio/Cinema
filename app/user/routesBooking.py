from flask import redirect, render_template, request, make_response, url_for, flash
from flask_login import current_user
from sqlalchemy import insert, select, join, bindparam
from app import app
from app.shared.login import login_required
from app.model import movies, genres, movieSchedule, theaters, booking, users, clients
from app.user.functionForBooking import createIntegerListFromQuery, createIntegerListFromString, removeElemInTemporaryList, KeyIsInTemporaryList, isNotInTemporaryList, addTemporaryListInList, startTimer, timerIsAlive, timerBookingInProgress, convertToInt
from app.user.pay import pay
from app.engineFunc import choiceEngine
import datetime



#Giosuè Zannini
@app.route('/choiceMovie', methods = ['POST', 'GET'])
def choicemovie():
    if not current_user.is_authenticated:
        flash("Autenticarsi per prenotare", "info")
    if request.method == 'POST':
        choice = request.form.get("choice") #idmovieSchedule
        if choice:
            if not timerBookingInProgress(current_user.get_id()):
                return redirect(url_for("book", idmovieSchedule = choice))
            flash("Hai già una prenotazione in corso", "error")
        else:
            flash('Effettuare una scelta', 'error')
    # mi ritorna tutti i film in programmazione futura
    query = select([movieSchedule.\
            join(movies, movieSchedule.c.idMovie == movies.c.id).\
            join(genres, movies.c.idGenre == genres.c.id)]).\
            order_by(movieSchedule.c.dateTime).\
            where(movieSchedule.c.dateTime > (datetime.datetime.now() + datetime.timedelta(minutes=15))) # blocco la prenotazione di un film 15 minuti prima della sua visione
    conn = choiceEngine()
    result = conn.execute(query)
    resp = make_response(render_template("/user/logged/choiceMovie.html", result = result))
    conn.close()
    return resp




#Giosuè Zannini
@app.route('/book/<int:idmovieSchedule>', methods = ['POST', 'GET'])
@login_required()
def book(idmovieSchedule):
    conn = choiceEngine()
    #mi ritorna il numero della sala e la capienza 
    queryTheater = select([theaters.c.id, theaters.c.seatsCapacity]).\
                   select_from(theaters.join(movieSchedule, theaters.c.id == movieSchedule.c.theater)).\
                   where(movieSchedule.c.id == bindparam('idmovieSchedule'))
    infoTheater = conn.execute(queryTheater, {'idmovieSchedule' : idmovieSchedule}).fetchone()
    conn.close()
    theaterName = infoTheater['id'] #numero della sala
    #creo una nuova chiave nel dizionario nel caso non sia stata creata
    KeyIsInTemporaryList(idmovieSchedule)
    if request.method == 'POST':
        listOfBooking = [] #tiene traccia dei posti che sta prenotando questo utente
        for i in range(infoTheater['seatsCapacity']):#creo lista con i posti scelti dall'utente
            seat = request.form.get("seat[" + str(i) + "]")
            if seat:
                listOfBooking.append(i + 1) #popolo la lista
        if listOfBooking:#caso in cui ha scelto almeno un posto
            if isNotInTemporaryList(idmovieSchedule, listOfBooking):#caso in cui non ha scelto posti già in fase di prenotazione, vengono aggiunti alla temporary list
                seconds = len(listOfBooking) * 60 #tempo di prenotazione dato all'utente
                startTimer(idmovieSchedule, listOfBooking, seconds, current_user.get_id())
                flash("Hai a disposizione %d secondi per completare la prenotazione" % seconds,"info")
                return redirect(url_for("completeBooking", idmovieSchedule = idmovieSchedule, listOfBooking = listOfBooking))
            else:
                flash('Posto\i già occupato\i, cambialo\i', 'error')    
        else:
            flash('Scegliere almeno un posto', 'error') 
    conn = choiceEngine()
    #mi ritorna i posti già prenotati
    queryBooking = select([booking.c.seatNumber]).\
                   select_from(booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id)).\
                   where(movieSchedule.c.id == bindparam('idmovieSchedule'))
    #mi torna una lista di interi contenenti i posti occupati
    seatsOccuped = createIntegerListFromQuery(conn.execute(queryBooking, {'idmovieSchedule' : idmovieSchedule}))
    #oltre ai posti realmente prenotati mi blocca la scelta anche dei posti che stanno per essere prenotati
    addTemporaryListInList(idmovieSchedule, seatsOccuped)
    resp = make_response(render_template("/user/logged/book.html", infoTheater = infoTheater, seatsOccuped = seatsOccuped, idmovieSchedule = idmovieSchedule))
    conn.close()
    return resp
    



#Giosuè Zannini
@app.route('/completeBooking/<int:idmovieSchedule>/<listOfBooking>', methods = ['POST', 'GET'])
@login_required()
def completeBooking(idmovieSchedule, listOfBooking):
    #crea una lista di interi da una stringa contenente i posti da voler prenotare
    listOfBooking = createIntegerListFromString(listOfBooking)
    conn = choiceEngine()
    query = select([movieSchedule.c.price]).\
            where(movieSchedule.c.id == bindparam('idmovieSchedule'))
    #mi torna il prezzo che deve pagare il cliente per la visione
    price = conn.execute(query, {'idmovieSchedule' : idmovieSchedule}).fetchone()['price'] * len(listOfBooking)
    conn.close() 
    if request.method == 'POST':  
        #età minima per lo spettatore e numero sala
        conn = choiceEngine()
        query = select([movies.c.minimumAge, movieSchedule.c.theater]).\
                select_from(movieSchedule.join(movies, movieSchedule.c.idMovie == movies.c.id)).\
                where(movieSchedule.c.id == bindparam('idmovieSchedule'))
        info = conn.execute(query, {'idmovieSchedule' : idmovieSchedule}).fetchone()
        conn.close()
        minimumAge = info['minimumAge']
        theaterName = info['theater']
        correct = True #gestisce se sono stati inseriti i dati in modo corretto
        minAge = True #gestisce l'età minima
        viewer = [] #nome spettatori
        viewerAge = [] #età spettatori
        autoCompile = request.form.get("autoCompile") #spunta per inserimento automatico dei dati
        for i in range(len(listOfBooking)):
            if i == 0 and autoCompile: #caso in cui uso i dati dell'utente che sta prenotando
                conn = choiceEngine()
                # ritorna i dati dell'utente
                query = select([users.c.name, clients.c.birthDate]).\
                        select_from(users.join(clients, users.c.id == clients.c.id)).\
                            where(clients.c.id == current_user.get_id())
                user = conn.execute(query).fetchone()
                conn.close()
                viewer.append(user["name"])
                viewerAge.append(datetime.date.today().year - user["birthDate"].year) 
                if datetime.date.today().year - user["birthDate"].year < minimumAge:
                    minAge = False
            else:      
                viewer.append(request.form.get("viewer[" + str(i) + "]"))
                viewerAge.append(convertToInt(request.form.get("viewerAge[" + str(i) + "]")))
                if not viewer[i] or not viewerAge[i]:#caso informazioni mancanti
                    correct = False   
                elif viewerAge[i] < minimumAge:#caso età minima non rispettata
                    minAge = False
        if not correct:
            flash("Informazioni mancanti", "error")
        elif not minAge:
            flash("Età minima non rispettata", "error")
        else:
            if timerIsAlive(current_user.get_id()): #caso in cui il thread è ancora attivo
                if pay(current_user.get_id(), price):#esegue il pagamento
                    conn = choiceEngine()            
                    #creazione query e inserimento del DB
                    for i in range(len(listOfBooking)):
                        query = (booking.insert().\
                                        values(viewerName = bindparam('viewer'), viewerAge = bindparam('viewerAge'), seatNumber = bindparam('seatNumber'), 
                                               clientUsername = current_user.get_id(), idmovieSchedule = bindparam('idmovieSchedule')))
                        conn.execute(query, {'viewer' : viewer[i], 'viewerAge' : viewerAge[i], 'seatNumber' : listOfBooking[i], 'idmovieSchedule' : idmovieSchedule})
                    conn.close()    
                    flash("Prenotazione avvenuta con successo", "info")       
                else:
                    flash("Credito insufficiente", "error")
                removeElemInTemporaryList(listOfBooking, idmovieSchedule) #rimuove dalla lista dei temporanei i posti di questo utente
            else: #caso in cui il tempo per la prenotazione è scaduto
                flash("Tempo per la prenotazione scaduto", "error") 
            return redirect("/")
    return render_template("/user/logged/completeBooking.html", listOfBooking = listOfBooking, idmovieSchedule = idmovieSchedule, price = price)