from app import app, engine
from sqlalchemy import insert, select, join, delete, outerjoin, bindparam
from flask import  request, flash, make_response, render_template
from app.model import movies, movieSchedule, genres, theaters
from .shared import queryAndTemplate, queryAndFun
from datetime import datetime


#---------------------------------SELECT---------------------------------#

#dopo io dovrei dividere quelle passate da quelle non passate, con due visualizzazioni diverse
@app.route("/futureShowsTime")
def futureEvents():
    #mostro solo i film successivi 
    s = select([movieSchedule.\
            join(movies, movieSchedule.c.idMovie == movies.c.id).\
            outerjoin(genres, genres.c.id == movies.c.idGenre)
        ]).where(movieSchedule.c.dateTime >= datetime.today() )
    return queryAndTemplate(s, "listShowTime.html", otherPar = ["Passata", "/pastShowsTime",""])

@app.route("/pastShowsTime")
def pastEvents():
    s = select([movieSchedule.\
            join(movies, movieSchedule.c.idMovie == movies.c.id).\
            outerjoin(genres, genres.c.id == movies.c.idGenre)
        ]).where(movieSchedule.c.dateTime < datetime.today() )
    return queryAndTemplate(s, "listShowTime.html", otherPar = ["Futura", "/futureShowsTime", "passata"])

@app.route("/listShowsTime")#per compatibilitàà con il codice precedente
def listShowTime():
    #mostro solo i film successivi 
    s = select([movieSchedule.\
            join(movies, movieSchedule.c.idMovie == movies.c.id).\
            outerjoin(genres, genres.c.id == movies.c.idGenre)
        ])
    return queryAndTemplate(s, "listShowTime.html")

#---------------------------------INSERT---------------------------------#
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
