from app import app, engine
from sqlalchemy import insert, select, delete, and_, bindparam
from flask import  request, flash, make_response, render_template, redirect, url_for
from app.model import theaters, movieSchedule
from .shared import queryAndTemplate, queryHasResult, queryAndFun
from datetime import datetime
import time
from sqlalchemy.orm import Session


#---------------------------------SELECT---------------------------------#
@app.route("/listTheaters")
def listTheaters():
    s = select([theaters])
    return queryAndTemplate(s, "listTheaters.html")

#---------------------------------INSERT---------------------------------#
#mi sembra non vada un cazzo
@app.route("/insertTheater", methods=['GET', 'POST'])
def insertTheater():
    if request.method == 'POST':
        capacity = request.form.get("capacity")
        id = request.form.get('id')
        if capacity and id :#verifico che mi abbiano passato i parametri e che non siano già registrate sale con lo stesso id
            
            conn = engine.connect()
            session = Session(bind=engine)
            session.connection(execution_options={'isolation_level': 'SERIALIZABLE'})
            try:
                s = select([theaters]).\
                    where(theaters.c.id == bindparam('id'))
                result = session.execute(s,  {'id' : id}).fetchone()
                if result:
                   raise
                time.sleep(60)
                session.execute(
                            theaters.insert().\
                                values(id = bindparam('id'), seatsCapacity = bindparam('capacity')),
                            { 'id' : id, 'capacity' : capacity}

                        )
                session.commit()
                flash("Theater insert with success!",'info' )
                resp = redirect(url_for( 'listTheaters'))
            except:
                flash('La sala numero {} è già salvata!'.format(id), 'error')
                
                resp = redirect(url_for('insertTheater'))
            finally:
                conn.close()
                session.close()
                return resp

        else:
            flash("Dati mancanti",'error')
    return render_template("insertTheater.html")

#---------------------------------DELETE---------------------------------#

"""
Non permetto la cancellazione di sale con spettacoli collegati e non ancora andati in onda

    Ci sono tre opzioni per la cancellazione e viene scelta dell'utente:
            1. Cancella se spettacoli collegati sono solo passati -> quindi in movie schedule avrò null sul theater di riferimento
            2. Se ci sono spettacoli collegati FUTURI rifiuta l'aggiornamento
            3. Se NON ci sono spettacoli collegati posso eliminarlo
"""

#eseguo la verifica con una transazione per avere l'atomicità delle operazioni select and delete
def checkAndDeleteConnectedShow(q, arg, strErr):
    conn = engine.connect()
    trans = conn.begin()
    result = conn.execute(q, arg).fetchone()
    if result:
        trans.commit()
        conn.close()
        flash(strErr, 'error')
        return redirect(url_for('removeTheater'))
    else:
        rm = theaters.delete().\
            where(theaters.c.id == bindparam('id'))
        conn.execute(rm, arg)
        trans.commit()
        conn.close()
        flash('The theater {} has been removed with success'.format(arg['id']), 'info')
        return redirect(url_for('listTheaters'))
    

@app.route("/removeTheater", methods=['GET', 'POST'])
def removeTheater():
    if request.method == 'POST':
        id = request.form.get("id")
        option = request.form.get("option")
        if id and option:                  
            if option == '2':
                #verifico se ci sono spettacoli collegati
                sel = select([movieSchedule]).\
                    where( movieSchedule.c.theater == bindparam('id'))
                strErr = """Non si può rimuovere la sala {} perchè ci sono spettacoli collegati.\n
                    Per eliminare scegliere un altra opzione o cancellare le programmazi. """.format(id)
                return checkAndDeleteConnectedShow(sel, {'id' : id}, strErr )
            elif option == '1':
                # verifico se ci sono spettacoli non ancra andati in onda
                sel = select([movieSchedule]).\
                    where(
                        and_(movieSchedule.c.dateTime >= datetime.today(), 
                            movieSchedule.c.theater == bindparam('id')
                        )
                    )
                strErr =  """Non si può rimuovere la sala {} perchè ci sono programmazioni non ancora andate in onda.\n
                             Cancella le programmazi o riassegnale prima ad un altra sala. """.format(id)   
                return checkAndDeleteConnectedShow(sel, {'id' : id}, strErr)           
        else:
            flash('You have to insert the value to remove', 'error')
    s = select([theaters])    
    return queryAndTemplate(s, "removeTheater.html")
#---------------------------------UPDATE---------------------------------#

@app.route('/selectTheaterToUpdate', methods=['GET', 'POST'])
def selectTheaterToUpdate():
    if request.method == "POST":
        id = request.form.get('choosed')
        if id:
            sel = select([theaters]).\
                where(theaters.c.id == bindparam('id'))
                
                #TODO forse si potrebbe mettere in shared
          
            conn = engine.connect()
            result = conn.execute(sel, {'id' : id}).fetchone()
            conn.close()
      
            return render_template('modifyTheater.html',theater  = result)
        else:
            flash('Inserire i dati richiesti !', 'error')

    s = select([theaters])
    return queryAndTemplate(s, "updateTheater.html")

@app.route('/modifyTheater/<theaterID>', methods=['POST'])
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


