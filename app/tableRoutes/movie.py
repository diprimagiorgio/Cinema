from app import app, engine
from sqlalchemy import insert, select, outerjoin, delete, bindparam
from flask import  request, flash, redirect, url_for, render_template
from app.model import movies, genres, movieSchedule
from .shared import queryAndTemplate, queryAndFun, queryHasResult
from datetime import datetime

#---------------------------------SELECT---------------------------------#
#avevo messo outerjoin per i null adesso non dovrei più metterli
#faccio una left join perchè voglio tutti i film anche quelli che non hanno un genere corrispondente
@app.route("/listMovies")       
def listMovies():
    s = select([movies.\
            join(genres, genres.c.id == movies.c.idGenre)
        ])
    return queryAndTemplate(s, "listMovies.html")

#---------------------------------INSERT---------------------------------#
@app.route("/insertMovie", methods=['GET','POST'])
def insertMovie():
    if request.method == 'POST':
        title = request.form.get("title")
        age = request.form.get("age")
        duration = request.form.get("duration")
        genre = request.form.get("genre")
        if title and age and duration and genre:
            ins = movies.insert().\
                values(title = bindparam('title') , minimumAge = bindparam('minimumAge'), duration = bindparam('duration'), idGenre = bindparam('idGenre'))
            flash("Movie insert with success", 'info')
            return queryAndFun(ins, 'listMovies', {'title' : title, 'minimumAge': age, 'duration' : duration, 'idGenre' : genre} )
        flash("Dati mancanti", 'error')
    s = select([genres])
    return queryAndTemplate(s,"insertMovie.html")

#---------------------------------DELETE---------------------------------#
# ho deciso di fare il controllo se il film è nel db o meno.
# Anche se non è nel db io segnalo che l'ho tolto. Ma non rombo l'integrità del db
#
#riflettendo cancellare un movie schedule vuol film con associati un movie schedule vuol dire, anche cancellare il 
# movieSchedule associato ma questo è associato a delle prenotazioni, se cancello anche quelle
#divrei anche restituirei i soldi....
# TODO opzioni di cancellazione TUTTO DA SISTEMARE
""" 
    Io posso cancellare un film se
            - se non ci sono spettacoli collegati
            - se ci fossero spettacoli in passato, però a quel punto cosa devo mettere sul film ?? Secondo me non è possibile
            - se ci saranno spettacoli in futuro, però a quel punto dovrei anche chiamare la cancellazione del movie schedule associato.
                magari il quale mi dicese si può cancellare uno spettacolo o meno, quindi forse sarebbe meglio prima implementare
"""
@app.route('/removeMovie', methods=['POST', 'GET'])
def removeMovie():                  #dovrei controllare che non ci siano date in programmazione
    if request.method == 'POST':
        id = request.form.get('id')
        opz = request.form.get('option')
        if id and opz:
            if opz == '1':
                sel = select([movieSchedule]).\
                    where(movieSchedule.c.idMovie == bindparam('id'))
                if queryHasResult(sel, {'id' : id}):         # ci sono film programmati
                    flash('Ci sono spettacoli colleagti a questo film, cambiare impostazione cancellazione', 'error')
                    return redirect(url_for('removeMovie'))
            elif opz == '2':
                sel = select([movieSchedule]).\
                    where(
                        and_( movieSchedule.c.idMovie == bindparam('id'),
                              movieSchedule.c.dateTime >= datetime.today()
                        )
                    )
                if queryHasResult(sel, {'id' : id}):         # ci sono film programmati per il futuro
                    flash('Ci sono spettacoli colleagti a questo film FUTURI, cambiare impostazione cancellazione', 'error')
                    return redirect(url_for('removeMovie'))

            rem = movies.delete().\
                where(movies.c.id == bindparam('id'))
            flash("Il film è stato rimosso", 'info')                
            return queryAndFun(rem, 'listMovies', {'id' : id})
        else:    
            flash('Inserisci tutti i dati richiesti', 'error')

    s = select([movies])
    return queryAndTemplate(s, 'removeMovie.html')
#---------------------------------UPDATE---------------------------------#
@app.route('/selectMovieToUpdate', methods=['GET', 'POST'])
def selectMovieToUpdate():
    if request.method == 'POST':
        id = request.form.get('choosed')
        if id:
            sel = select([movies]).\
                where(movies.c.id == bindparam('id'))
            conn = engine.connect()
            r1 = conn.execute(sel, {'id' : id}).fetchone()
            sel = select([genres])
            r2 = conn.execute(sel)
            conn.close()
            return render_template("modifyMovie.html", genres = r2, movie = r1)
        else:
            flash('Inserire i dati richiesti !', 'error')

    s = select([movies.c.id, movies.c.title, movies.c.duration, movies.c.minimumAge, genres.c.description]).\
            where( movies.c.idGenre == genres.c.id)
    return queryAndTemplate(s, "updateMovie.html")

@app.route('/modifyMovie/<movieID>', methods=['POST'])
def modifyMovie(movieID):
    title = request.form.get("title")
    age = request.form.get("age")
    duration = request.form.get("duration")
    genre = request.form.get("genre")
    if title and age and duration and genre:
        ins = movies.update().\
            where(movies.c.id == bindparam('m_id')).\
            values(title = bindparam('title') , minimumAge = bindparam('minimumAge'), duration = bindparam('duration'), idGenre = bindparam('idGenre'))
        flash("Movie insert with success", 'info')
        return queryAndFun(ins, 'listMovies',
            {'m_id' : movieID, 'title' : title, 'minimumAge': age, 'duration' : duration, 'idGenre' : genre} )
    flash("Dati mancanti", 'error')

