from flask import redirect, render_template, request, make_response, url_for, flash
from sqlalchemy import insert, select, join, delete, and_, func 
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from app.model import users, movies, genres, movieSchedule, theaters, clients, managers, booking
from datetime import date, timedelta , datetime
from app import app, engine
from app.login import User, Role, login_required, login_manager
import datetime
from app.routesBooking import choicemovie
from sqlalchemy.sql.functions import now

@app.route("/statistiche1")
def statistiche1():
    return render_template("statistiche1.html")


#query per sapere il numero di prenotazioni associate ad un genere ed eta' media dei partecipanti
@app.route("/numeroPrenotazioniPerGenere")
def query1():
    
    s = booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).join(movies, movieSchedule.c.idMovie == movies.c.id).join(genres,movies.c.idGenre == genres.c.id)
    queryCount = select([genres.c.description,func.count(booking.c.id).label('numero'),func.avg(booking.c.viewerAge).label('avgAge')]).select_from(s).group_by(genres.c.description)
    
    conn = engine.connect()
    ris1 = conn.execute(queryCount).fetchall()
    print(ris1)
    conn.close()
    return render_template("statGenere.html",numeroPrenotazioni = ris1)

@app.route("/saldoPerFilm")
def query2():
    conn = engine.connect()
    #incasso per film
    s = booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).join(movies, movieSchedule.c.idMovie == movies.c.id)
    querynumeroPrenotazioni = select([movies.c.title,func.sum(movieSchedule.c.price).label('sum')]).select_from(s).group_by(movies.c.title).order_by(movies.c.title)

    ris = conn.execute(querynumeroPrenotazioni).fetchall()
    print(ris)
    conn.close()
    return render_template("saldoFilm.html", saldo = ris)


@app.route("/occupazioneSalaPerFilm",methods=['GET','POST'])
def query3():
    if request.method == 'POST': 
        sala= request.form.get('sale')
        film= request.form.get('film')
        if sala!= 'Seleziona...' and film != 'Seleziona...':
                settimana = date.today() - timedelta(days = 7)
                duesettimane = date.today() - timedelta(days = 14)
                mese = date.today() - timedelta(days = 30)

                conn = engine.connect()
                #numeri di posti prenotati per sala per film
                
                unasettimana = select([func.count(booking.c.id).label('count')]).\
                    select_from(booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).join(movies,movieSchedule.c.idMovie == movies.c.id)).\
                        where(
                            and_(movieSchedule.c.idMovie == film,
                                  movieSchedule.c.theater == sala, movieSchedule.c.dateTime >= settimana)
                            )
                duesettimane = select([func.count(booking.c.id).label('count')]).\
                    select_from(booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).join(movies,movieSchedule.c.idMovie == movies.c.id)).\
                        where(
                            and_(movieSchedule.c.idMovie == film,
                                  movieSchedule.c.theater == sala, movieSchedule.c.dateTime >= duesettimane)
                            )
                unmese = select([func.count(booking.c.id).label('count')]).\
                    select_from(booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).join(movies,movieSchedule.c.idMovie == movies.c.id)).\
                        where(
                            and_(movieSchedule.c.idMovie == film,
                                  movieSchedule.c.theater == sala, movieSchedule.c.dateTime >= mese)
                            )
                ris1 = conn.execute(unasettimana).fetchone()
                ris2 = conn.execute(duesettimane).fetchone()
                ris3 = conn.execute(unmese).fetchone()
                
                print("--------- "'%s')
                print(ris1['count']) #risposta da mandare ad un html
                print(ris2['count']) #risposta da mandare ad un html
                print(ris3['count']) #risposta da mandare ad un html
                
                conn.close()
                return render_template("resultOccupazioneSala.html", sala = sala, settimana = ris1['count'], duesettimane= ris2['count'], mese = ris3['count'])
                
                
                
                
                
                
                
                
            
    s3 = select([theaters])#trovo tutte le sale
    s41 = movieSchedule.join(movies, movieSchedule.c.idMovie== movies.c.id)
    s4 = select([func.distinct(movies.c.id).label('id'),movies.c.title]).select_from(s41).order_by(movies.c.title)#trovo solo i film con prenotazioni mi manca il count distinct 
    conn = engine.connect()
    sale = conn.execute(s3)
    film = conn.execute(s4)
    resp = make_response(render_template("occupazioneSala.html", theaters = sale, movies = film ))
    conn.close()
    return resp

    