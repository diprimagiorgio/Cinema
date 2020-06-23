from flask import redirect, render_template, request, make_response, url_for, flash
from flask_login import current_user
from sqlalchemy import insert, select, join, bindparam, desc, func
from app import app, engine
from app.login import login_required, Role
from app.model import movies, genres, movieSchedule, theaters, booking, users, clients
from app.functionForBooking import createIntegerListFromQuery





#Giosuè Zannini
@app.route('/verifyMovie', methods = ['POST', 'GET'])
@login_required(Role.SUPERVISOR)
def verifymovie():
    if request.method == 'POST':
        choice = request.form.get("choice") #idmovieSchedule
        if choice:
            return redirect(url_for("verifyBook", idmovieSchedule = choice))
        else:
            flash('Effettuare una scelta', 'error')
    query = select([movieSchedule.c.id, movieSchedule.c.dateTime, movies.c.title, genres.c.description, movies.c.duration, movies.c.minimumAge, movieSchedule.c.theater, movieSchedule.c.price, theaters.c.seatsCapacity, func.count(booking.c.id).label("count")]).\
            select_from(movieSchedule.join(movies, movieSchedule.c.idMovie == movies.c.id).\
            join(genres, movies.c.idGenre == genres.c.id).join(theaters, theaters.c.id == movieSchedule.c.theater).\
            join(booking, booking.c.idmovieSchedule == movieSchedule.c.id, isouter = True)).\
            order_by(desc(movieSchedule.c.dateTime)).\
            group_by(movieSchedule.c.id, movieSchedule.c.dateTime, movies.c.title, genres.c.description, movies.c.duration, movies.c.minimumAge, movieSchedule.c.theater, movieSchedule.c.price, theaters.c.seatsCapacity)
    conn = engine.connect()
    result = conn.execute(query)
    resp = make_response(render_template("/manager/shared/verifyMovie.html", result = result))
    conn.close()
    return resp




#Giosuè Zannini
@app.route('/verifyBook/<int:idmovieSchedule>')
@login_required(Role.SUPERVISOR)
def verifyBook(idmovieSchedule):
    conn = engine.connect()
    queryTheater = select([theaters.c.id, theaters.c.seatsCapacity]).\
                   select_from(theaters.join(movieSchedule, theaters.c.id == movieSchedule.c.theater)).\
                   where(movieSchedule.c.id == bindparam('idmovieSchedule'))
    #mi ritorna il numero della sala e la capienza 
    infoTheater = conn.execute(queryTheater, {'idmovieSchedule' : idmovieSchedule}).fetchone()
    #mi ritorna i posti già prenotati
    queryBooking = select([booking.c.seatNumber]).\
                   select_from(booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id)).\
                   where(movieSchedule.c.id == bindparam('idmovieSchedule'))
    #mi torna una lista di interi contenenti i posti occupati
    seatsOccuped = createIntegerListFromQuery(conn.execute(queryBooking, {'idmovieSchedule' : idmovieSchedule}))
    resp = make_response(render_template("/manager/shared/verifyBook.html", infoTheater = infoTheater, seatsOccuped = seatsOccuped, idmovieSchedule = idmovieSchedule))
    conn.close()
    return resp