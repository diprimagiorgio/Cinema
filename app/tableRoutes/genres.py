from app import app,engine
from sqlalchemy import insert, select, delete, bindparam
from flask import  request, flash, render_template, redirect, url_for
from app.model import genres, movies
from .shared import queryAndTemplate, queryAndFun, queryHasResult


#---------------------------------SELECT---------------------------------#
#DIPRIMA GIORGIO 
@app.route("/listGenres")
def listGenres():
    s = select([genres])
    return queryAndTemplate(s, "listGenres.html")

#---------------------------------INSERT---------------------------------#
#DIPRIMA GIORGIO 
@app.route("/insertGenre", methods=['GET','POST'])
def insertGenre():
    if request.method == 'POST':
        des = request.form.get('description')
        if des:
            ins = genres.insert().values( description = bindparam('description'))
            flash("Il genere è stato inserito con successo", 'info')
            return queryAndFun(ins, "listGenres", {'description' : des} )
        flash('Devi inserire una descrizione per il genere', 'error')
    return render_template("insertGenre.html")

#---------------------------------DELETE---------------------------------#
"""
    La cancellazione può avvenire se
            - non ci sono film collegati
    Ci sono due i casi in cui posso accorgermi che c'è un film collegato:
        - dopo la select se questa ha risultati, quindi per un inserimento precedente o
        - dopo che io ho finito la select, generando un errore nella remove
            in quanto viola il vincolo di integrità della foreign key no action.
            In questo caso un altro utente ha effettuato un inserimento dopo l'esecuzione della select
"""
#TODO   posso usare le funzioni in shared e cambiare la firma permettendo di passare anche una connessione
#DIPRIMA GIORGIO 
@app.route('/removeGenre', methods=['GET','POST'])
def removeGenre():
    if request.method == 'POST':
        id = request.form.get('genre')
        if id:
            #cancella solo se non ci sono film collegati -> qui dovrei fare ua transazione per atomicità dell'operazione
            conn = engine.connect()
            trans = conn.begin()
            try:
                sel = select([movies]).\
                    where( movies.c.idGenre == bindparam('id'))
                
                result = conn.execute(sel,  {'id' : id}).fetchone()

                if result:         #se ci sono film collegati mando errore
                   raise
                
                rem = genres.delete().\
                    where(genres.c.id == bindparam('id'))
                
                result = conn.execute(rem,{'id' : id})
                trans.commit()

                flash('Genere rimosso con successo!', 'info')
    
                resp = redirect(url_for( 'listGenres'))
                
            except:
                flash('Il genere ha dei film collegati, sei sicuro di non volerlo modificare?', 'error')
                trans.rollback()
                resp = redirect(url_for('removeGenre'))
            finally:
                conn.close()
                return resp
            
        flash('Inserire i dati richiesti !', 'error')
    
    sel = select([genres])
    return queryAndTemplate(sel, 'removeGenre.html')
    
#---------------------------------UPDATE---------------------------------#
#DIPRIMA GIORGIO 
@app.route('/selectGenreToUpdate', methods=['GET', 'POST'])
def selectGenreToUpdate():
    if request.method == "POST":
        id = request.form.get('choosed')
        if id:
            sel = select([genres]).\
                where(genres.c.id == bindparam('id'))
                
                #TODO forse si potrebbe mettere in shared
          
            conn = engine.connect()
            result = conn.execute(sel, {'id' : id}).fetchone()
            conn.close()
      
            return render_template('modifyGenre.html',genre  = result)
        else:
            flash('Inserire i dati richiesti !', 'error')

    s = select([genres])
    return queryAndTemplate(s, "updateGenre.html")

#DIPRIMA GIORGIO 
@app.route('/modifyGenre/<genreID>', methods=['POST'])
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
