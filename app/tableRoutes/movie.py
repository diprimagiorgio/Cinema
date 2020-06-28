from app import app
from sqlalchemy import insert, select, outerjoin, delete, bindparam, and_
from flask import  request, flash, redirect, url_for, render_template
from app.model import movies, genres, movieSchedule
from .shared import queryAndTemplate, queryAndFun, queryHasResult
from datetime import datetime
from app.login import Role, login_required
from app.engineFunc import choiceEngine

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
#
# TODO opzioni di cancellazione ANDREBBE FATTO CON TRANSACTION PER ATOMICITÀ CON LA SELECT. Penso a vincoloi a livello di db.
# Penso al caso in cui vedo che non c'è nessuna programmazione collegata ma poi ne aggiunge una. Che succede ? 
"""
    Scenari possibili
            - se non ci sono spettacoli collegati posso eliminare
            - se ci fossero spettacoli in passato, metto disabilitato il film, quindi non è più nell'elenco di quelli per la programmazione
            - se ci saranno spettacoli in futuro, non posso cancellare
"""
@app.route('/removeMovie', methods=['POST', 'GET'])
@login_required(Role.SUPERVISOR)
def removeMovie():                  
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
            conn = choiceEngine()
            r1 = conn.execute(sel, {'id' : id}).fetchone()
            sel = select([genres])
            r2 = conn.execute(sel)
            conn.close()
            return render_template("/tables/movie/modifyMovie.html", genres = r2, movie = r1)
        else:
            flash('Inserire i dati richiesti !', 'error')

#TODO da sistemare se non riesco per quel cazzo di id doppio uso il from, il problema è il doppio id, sarebbe meglio usare selectMovie
    s = select([movies.c.id, movies.c.title, movies.c.duration, movies.c.minimumAge, genres.c.description]).\
            where( and_( movies.c.idGenre == genres.c.id, movies.c.available ==True))
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

