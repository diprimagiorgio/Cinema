from app import app
from sqlalchemy import insert, select, delete, and_, bindparam
from flask import  request, flash, make_response, render_template, redirect, url_for
from app.model import theaters, movieSchedule
from .shared import queryAndTemplate, queryHasResult, queryAndFun
from datetime import datetime
import time
from app.shared.login import Role, login_required
from app.engineFunc import choiceEngine

#file di Diprima Giorgio

#---------------------------------SELECT---------------------------------#
def selectTheaters():
    s = select([theaters]).where(theaters.c.available == True)
    conn = choiceEngine()
    result = conn.execute(s)
    conn.close()
    return result
    
selectTheaters =  select([theaters]).where(theaters.c.available == True)

@app.route("/listTheaters")
@login_required(Role.SUPERVISOR)
def listTheaters():
    return queryAndTemplate(selectTheaters, "/tables/theater/listTheaters.html")

#---------------------------------INSERT---------------------------------#
#devo verificare che non esiste una sala uguale
@app.route("/insertTheater", methods=['GET', 'POST'])
@login_required(Role.SUPERVISOR)
def insertTheater():
    if request.method == 'POST':
        capacity = request.form.get("capacity")
        id = request.form.get('id')
        if capacity and id :#verifico che mi abbiano passato i parametri e che non siano già registrate sale con lo stesso id
           
            conn = choiceEngine()
            #lo faccio dentro un try perchè se ci sono già sale con la stessa PK va in errore
            try:
                ins  = theaters.insert().\
                            values(id = bindparam('id'), seatsCapacity = bindparam('capacity'))
                result = conn.execute(ins,{ 'id' : id, 'capacity' : capacity})

                flash('Genere sala inserita con successo!', 'info')
                resp = redirect(url_for( 'listTheaters'))
            except:
                flash('La sala numero {} è già salvata!'.format(id), 'error')
                resp = redirect(url_for('insertTheater'))
            finally:
                conn.close()
                return resp
        else:
            flash("Dati mancanti",'error')
    return render_template("/tables/theater/insertTheater.html")

#---------------------------------DELETE---------------------------------#

"""
    Ci sono tre opzioni per la cancellazione e viene scelta dell'utente:
            1. Cancella se spettacoli collegati sono solo passati -> quindi la metto non disponibile. Non è più possible mettere nuove programmazioni in quella sala
            2. Se ci sono spettacoli collegati FUTURI rifiuta la cancellazione
            3. Se NON ci sono spettacoli collegati posso eliminarlo
"""

@app.route("/removeTheater", methods=['GET', 'POST'])
@login_required(Role.SUPERVISOR)
def removeTheater():
    if request.method == 'POST':
        id = request.form.get("id")
        if id :

            conn = engine.connect()
            conn = conn.execution_options( isolation_level="SERIALIZABLE" )
            trans = conn.begin()
            try:
                #verifico se ci sono spettacoli collegati
                sel = select([movieSchedule]).\
                        where( movieSchedule.c.theater == bindparam('id'))
                if queryHasResult(sel, {'id' : id}, conn = conn):
                    #verifico se gli spettacoli collegati sono futuri
                    sel = select([movieSchedule]).\
                            where( 
                                and_(
                                    movieSchedule.c.theater == bindparam('id'),
                                    movieSchedule.c.dateTime >= datetime.today()
                                )
                            )
                    if queryHasResult(sel, {'id' : id}, conn = conn):
                        #non posso cancellare
                        flash(  """Non si può rimuovere la sala {} perchè ci sono proiezioni non ancora andate in onda.\n
                                    Riassegna le proiezioni ad un altra sala. """.format(id), 'error')
                    else:    
 #                       time.sleep(10)
                        #devo mettere non disponibile
                        up = theaters.update().\
                            where(theaters.c.id == bindparam('t_id')).\
                            values(available = False)
                        flash("Sala DISATTIVATA!", 'info')
                        
                        conn.execute(up, {'t_id' : id} )
                        trans.commit()
                        ret = redirect(url_for('listTheaters'))    
                else:
#                    time.sleep(10)
                    #posso cancellarlo
                    rm = theaters.delete().\
                        where(theaters.c.id == bindparam('id'))
                    flash("Sala rimossa!", 'info')
                    conn.execute(rm, {'id' : id} )
                    trans.commit()

                    ret = redirect(url_for('listTheaters'))    
            except:
                trans.rollback()
                resp = redirect(url_for('removeTheater'))    
            finally:
                conn.close()
                trans.close()

        else:
            flash('You have to insert the value to remove', 'error')
    return queryAndTemplate(selectTheaters, "/tables/theater/removeTheater.html")

#---------------------------------UPDATE---------------------------------#

#elenca tutte le sale disponibili. Poi l'utente seleziona quella che vuole modificare e vene indirizzato in modifyTheater
@app.route('/selectTheaterToUpdate', methods=['GET', 'POST'])
@login_required(Role.SUPERVISOR)
def selectTheaterToUpdate():
    if request.method == "POST":
        id = request.form.get('choosed')
        if id:
            #per poter stampare i dati nella pagina
            sel = select([theaters]).\
                where(
                    and_(
                        theaters.c.id == bindparam('id'),
                        theaters.c.available == True
                    )              
                )
            conn = choiceEngine()
            result = conn.execute(sel, {'id' : id}).fetchone()
            conn.close()
      
            return render_template('/tables/theater/modifyTheater.html',theater  = result)
        else:
            flash('Inserire i dati richiesti !', 'error')

    return queryAndTemplate(selectTheaters, "/tables/theater/updateTheater.html")

    

@app.route('/modifyTheater/<theaterID>', methods=['POST'])
@login_required(Role.SUPERVISOR)
def modifyTheater(theaterID):
    cap = request.form.get('capacity')
    if cap: 
        up = theaters.update().\
            where(theaters.c.id == bindparam('t_id')).\
            values(seatsCapacity = bindparam('capacity'))
        flash('La modifica è stata salvata!', 'info')
        return queryAndFun(up,'listTheaters',  {'t_id' : theaterID, 'capacity' : cap} )
    else:
        flash('Inserire i dati richiesti !', 'error')
        return redirect(url_for('selectTheaterToUpdate'))


