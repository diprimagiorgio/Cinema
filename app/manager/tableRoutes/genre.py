from app import app
from sqlalchemy import insert, select, delete, bindparam
from flask import  request, flash, render_template, redirect, url_for, make_response
from app.model import genres, movies
from .shared import queryAndTemplate, queryAndFun
import time
from app.shared.login import Role, login_required
from app.engineFunc import choiceEngine
#---------------------------------SELECT---------------------------------#
#DIPRIMA GIORGIO 
@app.route("/listGenres")
@login_required(Role.SUPERVISOR)
def listGenres():
    s = select([genres])
    return queryAndTemplate(s, "/tables/genre/listGenres.html")

#---------------------------------INSERT---------------------------------#
#DIPRIMA GIORGIO 
@app.route("/insertGenre", methods=['GET','POST'])
@login_required(Role.SUPERVISOR)
def insertGenre():
    if request.method == 'POST':
        des = request.form.get('description')
        if des:
            ins = genres.insert().values( description = bindparam('description'))
            flash("Il genere è stato inserito con successo", 'info')
            return queryAndFun(ins, "listGenres", {'description' : des} )
        flash('Devi inserire una descrizione per il genere', 'error')
    return render_template("/tables/genre/insertGenre.html")

#---------------------------------DELETE---------------------------------#
"""
    La cancellazione può avvenire se non ci sono film collegati.
    Se ci sono film collegati il DBMS genererà un errore nella remove
    in quanto viola il vincolo di integrità della foreign key no action.
"""
#DIPRIMA GIORGIO 
@app.route('/removeGenre', methods=['GET','POST'])
@login_required(Role.SUPERVISOR)
def removeGenre():
    if request.method == 'POST':
        id = request.form.get('genre')
        if id:
            #cancella solo se non ci sono film collegati
            conn = choiceEngine()
            #lo faccio dentro un try perchè se ci sono film collegati va in errore perchè condizione sulla chiave esterna
            try:
                rem = genres.delete().\
                    where(genres.c.id == bindparam('id'))
                result = conn.execute(rem,{'id' : id})

                flash('Genere rimosso con successo!', 'info')
                resp = redirect(url_for( 'listGenres'))
            except:
                flash('Il genere ha dei film collegati, sei sicuro di non volerlo modificare?', 'error')
                resp = redirect(url_for('removeGenre')) 
            finally:
                conn.close()
                return resp
            
        flash('Inserire i dati richiesti !', 'error')
    
    sel = select([genres])
    return queryAndTemplate(sel, '/tables/genre/removeGenre.html')
    
#---------------------------------UPDATE---------------------------------#
#DIPRIMA GIORGIO 
@app.route('/selectGenreToUpdate', methods=['GET', 'POST'])
@login_required(Role.SUPERVISOR)
def selectGenreToUpdate():
    if request.method == "POST":
        id = request.form.get('choosed')
        if id:
            sel = select([genres]).\
                where(genres.c.id == bindparam('id'))
            conn = choiceEngine()
            result = conn.execute(sel, {'id' : id}).fetchone()
            conn.close()
            return render_template('/tables/genre/modifyGenre.html',result  = result)
        else:
            flash('Inserire i dati richiesti !', 'error')

    s = select([genres])
    return queryAndTemplate(s, "/tables/genre/updateGenre.html")

#DIPRIMA GIORGIO 
@app.route('/modifyGenre/<genreID>', methods=['POST'])
@login_required(Role.SUPERVISOR)
def modifyGenre(genreID):
    des = request.form.get('description')
    if des: 
        up = genres.update().\
            where(genres.c.id == bindparam('g_id')).\
            values(description = bindparam('description'))
        flash('La modifica è stata salvata!', 'info')
        return queryAndFun(up,'listGenres',  {'g_id' : genreID, 'description' : des} )
    else:
        flash('Inserire i dati richiesti !', 'error')
        return redirect(url_for('selectGenreToUpdate'))
