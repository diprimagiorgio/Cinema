from app import app
from sqlalchemy import insert, select, join, delete, outerjoin, bindparam, and_, text
from flask import  request, flash, redirect, url_for, render_template, make_response
from app.model import movies, movieSchedule, genres, theaters
from .shared import queryAndTemplate, queryAndFun, queryHasResultWithConnection
from .theater import selectTheaters
from datetime import datetime, timedelta
from app.shared.login import Role, login_required
from app.engineFunc import choiceEngine

#file Diprima Giorgio

#---------------------------------SELECT---------------------------------#


@app.route("/futureShowsTime")
@login_required(Role.SUPERVISOR)
def futureEvents():
    #mostro solo i film successivi alla data odierna
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

@app.route("/listShowsTime")
@login_required(Role.SUPERVISOR)
def listShowTime():
    s = select([movieSchedule.\
            join(movies, movieSchedule.c.idMovie == movies.c.id).\
            outerjoin(genres, genres.c.id == movies.c.idGenre)
        ])
    return queryAndTemplate(s, "/tables/movieSchedule/listShowTime.html")

#---------------------------------INSERT---------------------------------#
#controllo che la prenotazione sia valida, ossia che non si siano spettacoli in programmazione sulla stessa sala in quel momento
@app.route("/insertShowTime",  methods=['GET','POST'])
@login_required(Role.SUPERVISOR)
def insertShowTime():
    if request.method == 'POST':
        date = request.form.get('date')
        price = request.form.get('price')
        movie = request.form.get('movie')
        theater = request.form.get('theater')
        if date and price and movie and theater:

            #controllo che l'inserimento non porti a sovrapposizione di spettacoli
            conn = choiceEngine()
            conn = conn.execution_options( isolation_level="SERIALIZABLE" )
            trans = conn.begin()
            try:
                #Trovo la durata del film che voglio andare a mettere in proiezione
                sel = select([movies]).where(movies.c.id == bindparam('id_movie'))
                result = conn.execute(sel,{ 'id_movie' : movie}).fetchone()
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
                #se c'è un risultato allora la sala è occupata
                if(queryHasResultWithConnection(sel, conn, { 'theater' : theater,'date': date} )):
                    flash("Sala occupata! Cambia sala o orario", 'error')
                    raise
                else:        
                    #inserisco il film nel database
                    ins = movieSchedule.insert().\
                        values(dateTime = bindparam('date'), price = bindparam('price'), idMovie = bindparam('movie'), theater = bindparam('theater'))
                    flash("Spettacolo inserito con successo", 'info')
                    conn.execute(ins, {'date' : date, 'price' : price ,'movie' : movie ,'theater' : theater } )
                    trans.commit()
                    ret = redirect(url_for('listShowTime'))
            except:
                trans.rollback()
                ret = redirect(url_for('insertShowTime'))
            finally:
                conn.close()
                trans.close()
                return ret

        else:
            flash('Dati mancanti', 'error')
    s1 = selectTheaters #trovo tutte le sale
    s2 = select([movies]).where(movies.c.available == True) #trovo tutti i film
    conn = choiceEngine()
    mv = conn.execute(s2)
    th = conn.execute(s1)
    resp = make_response(render_template("/tables/movieSchedule/insertShowTime.html", theaters = th, movies = mv))
    conn.close()
    return resp