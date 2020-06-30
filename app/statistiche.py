from flask import redirect, render_template, request, make_response, url_for, flash
from sqlalchemy import select, join, and_, func ,bindparam
from app.model import users, movies, genres, movieSchedule, theaters, clients, managers, booking
from datetime import date, timedelta , datetime
from app import app
from app.shared.login import User, Role, login_required, login_manager
import datetime
from app.user.routesBooking import choicemovie
from app.engineFunc import choiceEngine
from sqlalchemy.sql.functions import now

@app.route("/statistiche1")
def statistiche1():
    return render_template("/manager/statistiche/statistiche1.html")


#query per sapere il numero di prenotazioni associate ad un genere ed eta' media dei partecipanti
@app.route("/numeroPrenotazioniPerGenere")
def query1():
    
    s = booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).\
        join(movies, movieSchedule.c.idMovie == movies.c.id).join(genres,movies.c.idGenre == genres.c.id)
    queryCount = select([genres.c.description,func.count(booking.c.id).label('numero'),func.avg(booking.c.viewerAge).label('avgAge')]).\
        select_from(s).group_by(genres.c.description)
    
    conn = choiceEngine()
    ris1 = conn.execute(queryCount).fetchall()
    print(ris1)
    conn.close()
    return render_template("/manager/statistiche/statGenere.html",numeroPrenotazioni = ris1)

@app.route("/saldoPerFilm")
def query2():
    conn = choiceEngine()
    #incasso per film
    s = booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).\
        join(movies, movieSchedule.c.idMovie == movies.c.id)
    querynumeroPrenotazioni = select([movies.c.title,func.sum(movieSchedule.c.price).label('sum')]).\
        select_from(s).group_by(movies.c.title).order_by(movies.c.title)

    ris = conn.execute(querynumeroPrenotazioni).fetchall()
    print(ris)
    conn.close()
    return render_template("/manager/statistiche/saldoFilm.html", saldo = ris)


@app.route("/occupazioneSalaPerFilm",methods=['GET','POST'])
def query3():
    if request.method == 'POST': 
        sala= request.form.get('sale')
        film= request.form.get('film')
        if sala!= 'Seleziona...' and film != 'Seleziona...':
                settimana = date.today() - timedelta(days = 7)
                duesettimane = date.today() - timedelta(days = 14)
                mese = date.today() - timedelta(days = 30)

                conn = choiceEngine()
                #numeri di posti prenotati per sala per film
                nposti= select([theaters.c.seatsCapacity]).where(theaters.c.id == bindparam('sala'))
                unasettimana = select([func.count(booking.c.id).label('count')]).\
                    select_from(booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).\
                        join(movies,movieSchedule.c.idMovie == movies.c.id)).\
                        where(
                            and_(movieSchedule.c.idMovie == bindparam('film'),#controlla che funzioni bene la clausola where , datetime.now()???
                                  movieSchedule.c.theater == bindparam('sala'), date.today() >= movieSchedule.c.dateTime, movieSchedule.c.dateTime >= settimana)
                            )
                duesettimane = select([func.count(booking.c.id).label('count')]).\
                    select_from(booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).\
                        join(movies,movieSchedule.c.idMovie == movies.c.id)).\
                        where(
                            and_(movieSchedule.c.idMovie == bindparam('film'),
                                  movieSchedule.c.theater == bindparam('sala'), date.today() >= movieSchedule.c.dateTime,movieSchedule.c.dateTime >= duesettimane)
                            )
                unmese = select([func.count(booking.c.id).label('count')]).\
                    select_from(booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).\
                        join(movies,movieSchedule.c.idMovie == movies.c.id)).\
                        where(
                            and_(movieSchedule.c.idMovie == bindparam('film'),
                                  movieSchedule.c.theater == bindparam('sala'), date.today() >= movieSchedule.c.dateTime,movieSchedule.c.dateTime >= mese)
                            )
                posti = conn.execute(nposti,{'sala': sala}).fetchone()
                ris1 = conn.execute(unasettimana,{'sala': sala, 'film': film}).fetchone()
                ris2 = conn.execute(duesettimane,{'sala': sala, 'film': film}).fetchone()
                ris3 = conn.execute(unmese,{'sala': sala, 'film': film}).fetchone()
                
                conn.close()
                return render_template("/manager/statistiche/resultOccupazioneSala.html", sala = sala,\
                     posti = posti['seatsCapacity'] ,film = film, settimana = ris1['count'],\
                          duesettimane= ris2['count'], mese = ris3['count'])
                
               
    s3 = select([theaters])#trovo tutte le sale
    s41 = movieSchedule.join(movies, movieSchedule.c.idMovie== movies.c.id)
    s4 = select([func.distinct(movies.c.id).label('id'),movies.c.title]).select_from(s41).order_by(movies.c.title)#trovo solo i film con prenotazioni mi manca il count distinct 
    conn = choiceEngine()
    sale = conn.execute(s3)
    film = conn.execute(s4)
    resp = make_response(render_template("/manager/statistiche/occupazioneSala.html", theaters = sale, movies = film ))
    conn.close()
    return resp
    
#------------------DA COMPLETARE 
@app.route("/occupazioneSala",methods=['GET','POST'])
def occupazioneSala():
    if request.method == 'POST':
        conn = choiceEngine()
        query = select([movies.c.id, movies.c.title]).\
                    where(exists(select([movieSchedule.join(theaters, movieSchedule.c.theater == theaters.c.id)]).\
                          where(and_(movies.c.id == movieSchedule.c.idMovie, (theaters.c.seatsCapacity / 100) * 75 < (select(count(booking.c.id).\
                              where(booking.c.idmovieSchedule == movieSchedule.c.id)))))))
        user = conn.execute(query).fetchone()
        conn.close()
    