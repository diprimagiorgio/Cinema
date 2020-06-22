from app import app, engine
from sqlalchemy import insert, select, outerjoin, delete, bindparam
from flask import  request, flash, redirect, url_for, render_template
from app.model import movies, genres, movieSchedule
from .shared import queryAndTemplate, queryAndFun, queryHasResult
from datetime import datetime
from app.login import Role, login_required

#---------------------------------SELECT---------------------------------#
selectMovies = s = select([movies.\
            join(genres, genres.c.id == movies.c.idGenre)
        ]).\
            where( movies.c.available == True )
#è sufficiente fare una join perchè tutti i film hanno un genere collegato
@app.route("/listMovies")       
@login_required(Role.SUPERVISOR)
def listMovies():
    return queryAndTemplate(selectMovies, "/tables/movie/listMovies.html")

#---------------------------------INSERT---------------------------------#
@app.route("/insertMovie", methods=['GET','POST'])
@login_required(Role.SUPERVISOR)
def insertMovie():
    if request.method == 'POST':
        title = request.form.get("title")
        age = request.form.get("age")
        duration = request.form.get("duration")
        genre = request.form.get("genre")
        if age == '':
            age = 0
        if title  and duration and genre:
            ins = movies.insert().\
                values(title = bindparam('title') , minimumAge = bindparam('minimumAge'), duration = bindparam('duration'), idGenre = bindparam('idGenre'))
            flash("Movie insert with success", 'info')
            return queryAndFun(ins, 'listMovies', {'title' : title, 'minimumAge': age, 'duration' : duration, 'idGenre' : genre} )
        flash("Dati mancanti", 'error')
    s = select([genres])
    return queryAndTemplate(s,"/tables/movie/insertMovie.html")

#---------------------------------DELETE---------------------------------#
# ho deciso di fare il controllo se il film è nel db o meno.
# Anche se non è nel db io segnalo che l'ho tolto. Ma non rombo l'integrità del db
#
#riflettendo cancellare un movie schedule vuol film con associati un movie schedule vuol dire, anche cancellare il 
# movieSchedule associato ma questo è associato a delle prenotazioni, se cancello anche quelle
#divrei anche restituirei i soldi....
# TODO opzioni di cancellazione TUTTO DA SISTEMARE
"""
Faccio come con le sale 
    Io posso cancellare un film se
            - se non ci sono spettacoli collegati posso eliminare
            - se ci fossero spettacoli in passato, metto disabilitato il film
            - se ci saranno spettacoli in futuro, non posso cancellare
"""
@app.route('/removeMovie', methods=['POST', 'GET'])
@login_required(Role.SUPERVISOR)
def removeMovie():                  #dovrei controllare che non ci siano date in programmazione
    if request.method == 'POST':
        id = request.form.get('id')
        if id:
            #verifico se ci sono spettacoli collegati
            sel = select([movieSchedule]).\
                    where( movieSchedule.c.idMovie == bindparam('id'))
            if queryHasResult(sel, {'id' : id}):
            #verifico se gli spettacoli collegati sono futuri
                sel = select([movieSchedule]).\
                        where( 
                            and_(
                                movieSchedule.c.idMovie == bindparam('id'),
                                movieSchedule.c.dateTime >= datetime.today()
                            )
                        )
                if queryHasResult(sel, {'id' : id}):
                    #non posso cancellare
                    flash(  """Non si può rimuovere il film perchè ci sono proiezioni non ancora andate in onda.\n
                                Riassegna le proiezioni ad un altro film. """, 'error')
                else:    
                    #devo mettere non disponibile
                    up = movies.update().\
                        where(movies.c.id == bindparam('t_id')).\
                        values(available = False)
                    flash("Film DISABILITATO!", 'info')
                    return queryAndFun(up, 'listMovies', {'t_id' : id})
            else:
                #posso cancellarlo
                rm = movies.delete().\
                    where(movies.c.id == bindparam('id'))
                flash("Film rimossa!", 'info')
                return queryAndFun(rm, 'listMovies', {'id' : id})
        












    #        if opz == '1':
    #            sel = select([movieSchedule]).\
    #                where(movieSchedule.c.idMovie == bindparam('id'))
    #            if queryHasResult(sel, {'id' : id}):         # ci sono film programmati
    #                flash('Ci sono spettacoli colleagti a questo film, cambiare impostazione cancellazione', 'error')
    #                return redirect(url_for('removeMovie'))
    #        elif opz == '2':
    #            sel = select([movieSchedule]).\
    #                where(
    #                    and_( movieSchedule.c.idMovie == bindparam('id'),
    #                          movieSchedule.c.dateTime >= datetime.today()
    #                    )
    #                )
    #            if queryHasResult(sel, {'id' : id}):         # ci sono film programmati per il futuro
    #                flash('Ci sono spettacoli colleagti a questo film FUTURI, cambiare impostazione cancellazione', 'error')
    #                return redirect(url_for('removeMovie'))
#
    #        rem = movies.delete().\
    #            where(movies.c.id == bindparam('id'))
    #        flash("Il film è stato rimosso", 'info')                
    #        return queryAndFun(rem, 'listMovies', {'id' : id})
        else:    
            flash('Inserisci tutti i dati richiesti', 'error')

    s = select([movies])
    return queryAndTemplate(s, '/tables/movie/removeMovie.html')
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
            return render_template("/tables/movie/modifyMovie.html", genres = r2, movie = r1)
        else:
            flash('Inserire i dati richiesti !', 'error')
#potrei fare solo movies?
    s = select([movies.c.id, movies.c.title, movies.c.duration, movies.c.minimumAge, genres.c.description]).\
            where( movies.c.idGenre == genres.c.id)
    return queryAndTemplate(s, "/tables/movie/updateMovie.html")

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

