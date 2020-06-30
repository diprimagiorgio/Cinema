from flask import redirect, render_template, request, make_response, url_for, flash
from sqlalchemy import select, join, and_, func ,bindparam, between
from app.model import users, movies, genres, movieSchedule, theaters, clients, managers, booking
import datetime
from datetime import date, timedelta
from app import app
from app.shared.login import User, Role, login_required, login_manager
import datetime
from app.user.routesBooking import choicemovie
from app.engineFunc import choiceEngine
from sqlalchemy.sql.functions import now

@app.route("/statistiche1")
@login_required(Role.SUPERVISOR)
def statistiche1():
    return render_template("/manager/statistiche/statistiche1.html")

#--------------------------------------------------------------------------------------------------
#query per sapere il numero di prenotazioni associate ad ogni genere ed eta' media degli spettatori
@app.route("/numeroPrenotazioniPerGenere")
@login_required(Role.SUPERVISOR)
def query1():
    
    s = booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).\
        join(movies, movieSchedule.c.idMovie == movies.c.id).join(genres,movies.c.idGenre == genres.c.id)
    queryCount = select([genres.c.description,func.count(booking.c.id).label('numero'),func.avg(booking.c.viewerAge).label('avgAge')]).\
        select_from(s).group_by(genres.c.description)
    
    conn = choiceEngine()
    ris1 = conn.execute(queryCount).fetchall()
    conn.close()
    return render_template("/manager/statistiche/statGenere.html",numeroPrenotazioni = ris1)

#----------------------------------------------------------------------------------------------------
#query che mi va ad indicare il saldo per ogni film
@app.route("/saldoPerFilm")
@login_required(Role.SUPERVISOR)
def query2():
    conn = choiceEngine()
    #incasso per film
    s = booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).\
        join(movies, movieSchedule.c.idMovie == movies.c.id)
        
    querynumeroPrenotazioni = select([movies.c.title,func.sum(movieSchedule.c.price).label('sum')]).\
        select_from(s).\
        group_by(movies.c.title).\
        order_by(movies.c.title)

    ris = conn.execute(querynumeroPrenotazioni).fetchall()
    conn.close()
    return render_template("/manager/statistiche/saldoFilm.html", saldo = ris)

#-----------------------------------------------------------------------------------------------------------------
#Dato un film ed una sala scelta tra quelli disponibili mi calcola il numero di prenotazioni totali per quel film in quella sala 
#con tre archi di tempo differenti, nell'ultima settimana , nelle ultime due settimane, nell'ultimo mese.
# da sistemare aggiungere between 
@app.route("/occupazioneSalaPerFilm",methods=['GET','POST'])
@login_required(Role.SUPERVISOR)
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
                unasettimana = select([func.count(booking.c.id).label('count')]).\
                    select_from(booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).\
                        join(movies,movieSchedule.c.idMovie == movies.c.id)).\
                        where(
                            and_(movieSchedule.c.idMovie == bindparam('film'),#controlla che funzioni bene la clausola where , datetime.now()???
                                  movieSchedule.c.theater == bindparam('sala'), movieSchedule.c.dateTime.between(bindparam('tempo'),datetime.datetime.now())))
                
                titolo = select([movies]).where(movies.c.id == film)
                ristitolo = conn.execute(titolo).fetchone()
                ris1 = conn.execute(unasettimana,{'sala': sala, 'film': film, 'tempo': settimana}).fetchone()
                ris2 = conn.execute(unasettimana,{'sala': sala, 'film': film, 'tempo': duesettimane}).fetchone()
                ris3 = conn.execute(unasettimana,{'sala': sala, 'film': film, 'tempo': mese}).fetchone()
                
                
                
                conn.close()
                return render_template("/manager/statistiche/resultOccupazioneSala.html", sala = sala,\
                        film = ristitolo['title'], settimana = ris1['count'],\
                        duesettimane= ris2['count'], mese = ris3['count'])
                
    #mi servono per visualizzare le possibili scelte tra film e sale        
    s3 = select([theaters])#trovo tutte le sale
    s41 = movieSchedule.join(movies, movieSchedule.c.idMovie== movies.c.id)
    #trovo solo i film con prenotazioni, mi serve il distinct perche non voglio doppioni 
    s4 = select([func.distinct(movies.c.id).label('id'),movies.c.title]).select_from(s41).order_by(movies.c.title)
    conn = choiceEngine()
    sale = conn.execute(s3)
    film = conn.execute(s4)
    resp = make_response(render_template("/manager/statistiche/occupazioneSala.html", theaters = sale, movies = film ))
    conn.close()
    return resp
    
#Giosuè Zannini
@app.route("/occupazioneSala",methods=['GET','POST'])
@login_required(Role.SUPERVISOR)
def occupazioneSala():
    if request.method == 'POST':
        perc = request.form.get('percentuale')
        if perc != 0:
            conn = choiceEngine()
            query = select([movies.c.id, movies.c.title]).\
                        where(~exists(select([movieSchedule.join(theaters, movieSchedule.c.theater == theaters.c.id)]).\
                              where(and_(movies.c.id == movieSchedule.c.idMovie, 
                                        ((theaters.c.seatsCapacity / 100) * bindparam('perc')) < (select([func.count(booking.c.id)])).\
                                  where(booking.c.idmovieSchedule == movieSchedule.c.id)))))
            movie = conn.execute(query,{'perc' : perc})
            resp = make_response(render_template("/manager/statistiche/occupazioneSalaPercentualeResult.html", movie = movie, perc = perc))
            conn.close()
            return resp
        flash("Selezionare un valore dal menù a tendina", "error")
    return render_template("/manager/statistiche/occupazioneSalaPercentuale.html")
    
    