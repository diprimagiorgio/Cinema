from flask import redirect, render_template, request, make_response, url_for, flash
from sqlalchemy import insert, select, join, and_
from flask_login import current_user
from app.model import movies, genres, movieSchedule, theaters, booking
from app import app, engine
from app.login import login_required
import datetime
from app.functionForBooking import createIntegerListFromQuery, createIntegerListFromString, removeElemInTemporaryList, KeyIsInTemporaryList, isNotInTemporaryList, addTemporaryListInList, startTimer, timerIsAlive, timerBookingInProgress, convertToInt



#Giosuè Zannini
@app.route('/choiceMovie', methods = ['POST', 'GET'])
def choicemovie():
    if request.method == 'POST':
        choice = request.form.get("choice") #idmovieSchedule
        if choice:
            if not timerBookingInProgress(current_user.get_id()):
                return redirect(url_for("book", idmovieSchedule = choice))
            flash("Hai già una prenotazione in corso", "error")
        else:
            flash('Effettuare una scelta', 'error')
    query = select([movieSchedule.\
            join(movies, movieSchedule.c.idMovie == movies.c.id).\
            join(genres, movies.c.idGenre == genres.c.id)]).\
            order_by(movieSchedule.c.dateTime).\
            where(movieSchedule.c.dateTime > (datetime.datetime.now() - datetime.timedelta(minutes=15))) # blocco la prenotazione di un film 15 minuti prima della sua visione
    conn = engine.connect()
    result = conn.execute(query)
    resp = make_response(render_template("choiceMovie.html", result = result))
    conn.close()
    return resp




#Giosuè Zannini
@app.route('/book/<int:idmovieSchedule>', methods = ['POST', 'GET'])
@login_required()
def book(idmovieSchedule):
    conn = engine.connect()
    queryTheater = select([theaters.c.id, theaters.c.seatsCapacity]).\
                   select_from(theaters.join(movieSchedule, theaters.c.id == movieSchedule.c.theater)).\
                   where(movieSchedule.c.id == idmovieSchedule)
    #mi ritorna il numero della sala e la capienza 
    infoTheater = conn.execute(queryTheater).fetchone()
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
                seconds = len(listOfBooking) * 30 #tempo di prenotazione dato all'utente
                startTimer(idmovieSchedule, listOfBooking, seconds, current_user.get_id())
                flash("Hai a disposizione %d secondi per completare la prenotazione" % seconds,"info")
                return redirect(url_for("completeBooking", idmovieSchedule = idmovieSchedule, listOfBooking = listOfBooking))
            else:
                flash('Posto\i già occupato\i, cambialo\i', 'error')    
        else:
            flash('Scegliere almeno un posto', 'error') 
    conn = engine.connect()
    #mi ritorna i posti già prenotati
    queryBooking = select([booking.c.seatNumber]).\
                   select_from(booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id)).\
                   where(movieSchedule.c.id == idmovieSchedule)
    #mi torna una lista di interi contenenti i posti occupati
    seatsOccuped = createIntegerListFromQuery(conn.execute(queryBooking))
    #oltre ai posti realmente prenotati mi blocca la scelta anche dei posti che stanno per essere prenotati
    addTemporaryListInList(idmovieSchedule, seatsOccuped)
    resp = make_response(render_template("book.html", infoTheater = infoTheater, seatsOccuped = seatsOccuped, idmovieSchedule = idmovieSchedule))
    conn.close()
    return resp
    



#Giosuè Zannini
@app.route('/completeBooking/<int:idmovieSchedule>/<listOfBooking>', methods = ['POST', 'GET'])
@login_required()
def completeBooking(idmovieSchedule, listOfBooking):
    #crea una lista di interi da una stringa contenente i posti da voler prenotare
    listOfBooking = createIntegerListFromString(listOfBooking)
    conn = engine.connect()
    query = select([movieSchedule.c.price]).\
            where(movieSchedule.c.id == idmovieSchedule)
    #mi torna il prezzo che deve pagare il cliente per la visione
    price = conn.execute(query).fetchone()['price'] * len(listOfBooking)
    conn.close() 
    if request.method == 'POST':  
        conn = engine.connect()
        query = select([movies.c.minimumAge, movieSchedule.c.theater]).\
                select_from(movieSchedule.join(movies, movieSchedule.c.idMovie == movies.c.id)).\
                where(movieSchedule.c.id == idmovieSchedule)
        #età minima per lo spettatore e numero sala
        info = conn.execute(query).fetchone()
        conn.close()
        minimumAge = info['minimumAge'] #età minima 
        theaterName = info['theater'] #numero sala
        correct = True #gestisce se sono stati inseriti i dati in modo corretto
        minAge = True #gestisce l'età minima
        viewer = [] #nome spettatori
        viewerAge = [] #età spettatori
        for i in range(len(listOfBooking)):
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
                #--------------------------FUNZIONE GIORGIO--------------------------
                if (True): # pay(current_user.get_id(), price):----------------------------------------------------Da sistemare
                    queryIns = [] #contiene le query
                    #creazione query
                    for i in range(len(listOfBooking)):
                        queryIns.append(booking.insert().\
                                        values(viewerName = viewer[i], viewerAge = viewerAge[i], seatNumber = listOfBooking[i], 
                                               clientUsername = current_user.get_id(), idmovieSchedule = idmovieSchedule))
                    conn = engine.connect()            
                    #inserimento nel DB
                    for q in queryIns:
                        conn.execute(q)
                    conn.close()    
                    #libero il posto dalla lista dei prenotanti
                    removeElemInTemporaryList(listOfBooking, idmovieSchedule)
                    flash("Prenotazione avvenuta con successo", "info")       
                else:
                    flash("Credito insufficiente", "error")
            else: #caso in cui il tempo per la prenotazione è scaduto
                flash("Tempo per la prenotazione scaduto", "error") 
            return redirect("/")
    return render_template("completeBooking.html", listOfBooking = listOfBooking, idmovieSchedule = idmovieSchedule, price = price)




