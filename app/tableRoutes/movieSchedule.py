from app import app
from sqlalchemy import insert, select, join, delete, outerjoin, bindparam, and_, text
from flask import  request, flash, make_response, render_template
from app.model import movies, movieSchedule, genres, theaters
from .shared import queryAndTemplate, queryAndFun
from .theater import selectTheaters
from datetime import datetime, timedelta
from app.shared.login import Role, login_required
from app.engineFunc import choiceEngine


#---------------------------------SELECT---------------------------------#

#dopo io dovrei dividere quelle passate da quelle non passate, con due visualizzazioni diverse
@app.route("/futureShowsTime")
@login_required(Role.SUPERVISOR)
def futureEvents():
    #mostro solo i film successivi 
    s = select([movieSchedule.\
            join(movies, movieSchedule.c.idMovie == movies.c.id).\
            outerjoin(genres, genres.c.id == movies.c.idGenre)
        ]).where(movieSchedule.c.dateTime >= datetime.today() )
    return queryAndTemplate(s, "/tables/movieSchedule/listShowTime.html", otherPar = ["Passata", "/pastShowsTime",""])

@app.route("/pastShowsTime")
@login_required(Role.SUPERVISOR)
def pastEvents():
    s = select([movieSchedule.\
            join(movies, movieSchedule.c.idMovie == movies.c.id).\
            outerjoin(genres, genres.c.id == movies.c.idGenre)
        ]).where(movieSchedule.c.dateTime < datetime.today() )
    return queryAndTemplate(s, "/tables/movieSchedule/listShowTime.html", otherPar = ["Futura", "/futureShowsTime", "passata"])

@app.route("/listShowsTime")#per compatibilitàà con il codice precedente
@login_required(Role.SUPERVISOR)
def listShowTime():
    #mostro solo i film successivi 
    s = select([movieSchedule.\
            join(movies, movieSchedule.c.idMovie == movies.c.id).\
            outerjoin(genres, genres.c.id == movies.c.idGenre)
        ])
    return queryAndTemplate(s, "/tables/movieSchedule/listShowTime.html")

#---------------------------------INSERT---------------------------------#
#dovrei acnhe controllare che si inserisca una data futura
@app.route("/insertShowTime",  methods=['GET','POST'])
@login_required(Role.SUPERVISOR)
def insertShowTime():
    if request.method == 'POST':
        date = request.form.get('date')
        price = request.form.get('price')
        movie = request.form.get('movie')
        theater = request.form.get('theater')
        if date and price and movie and theater:
            #TODO: fare una connessione serializzabile, nessuno può inserire

            #controllo che l'inserimento non porti a sovrapposizione di spettacoli

            #Trovo la durata del film che voglio andare a mettere in proiezione
            sel = select([movies]).where(movies.c.id == bindparam('id_movie'))
            conn = choiceEngine()
            result = conn.execute(sel,{ 'id_movie' : movie}).fetchone()
            conn.close()
            
            runningTime = result['duration']
            date = datetime.strptime(date, '%Y-%m-%dT%H:%M')
            end = date + timedelta(minutes=runningTime)

            #verifico che il film che volgio inserire:
            #       - inizi dopo il film attualmente in proiezione
            #       o
            #       - finisca prima del film attualmente in proiezione
            sel = select([movieSchedule, movies]).\
                    where(
                        and_(
                            movieSchedule.c.idMovie == movies.c.id,
                            movieSchedule.c.theater == bindparam('theater'),
                            movieSchedule.c.dateTime +  text("interval '60 seconds'") * movies.c.duration >= bindparam('date'), 
                            movieSchedule.c.dateTime  <= end, 
                            )
                    )
            conn = choiceEngine()
            result = conn.execute(sel,{ 'theater' : theater,'date': date}).fetchone()
            conn.close()

            if(result):
                flash("Sala occupata! Cambia sala o orario", 'error')
            else:        
                #inserisco il film
                ins = movieSchedule.insert().\
                    values(dateTime = date, price = price, idMovie = movie, theater = theater)
                flash("Spettacolo inserito con successo", 'info')
                return queryAndFun(ins, 'listShowTime')
        else:
            flash('Dati mancanti', 'error')
        #devo inserire nel database
    s1 = selectTheaters#trovo tutte le sale
    s2 = select([movies])#trovo tutti i film
    conn = choiceEngine()
    mv = conn.execute(s2)
    th = conn.execute(s1)
    resp = make_response(render_template("/tables/movieSchedule/insertShowTime.html", theaters = th, movies = mv))
    conn.close()
    return resp
    
#potrei fare juna remove dove gli do
#posso dare una pagina per inserire
#---------------------------------DELETE---------------------------------#
#TODO posso cancellare solo vuoti senza programmazioni in futuro... Potrei anche dirie di no
#---------------------------------UPDATE---------------------------------#
#TODO posso monificare (Solo futuri??)
