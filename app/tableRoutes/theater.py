from app import app, engine
from sqlalchemy import insert, select, delete, and_, bindparam
from flask import  request, flash, make_response, render_template, redirect, url_for
from app.model import theaters, movieSchedule
from .shared import queryAndTemplate, queryHasResult, queryAndFun
from datetime import datetime
import time
from sqlalchemy.orm import Session
from app.login import Role, login_required


#---------------------------------SELECT---------------------------------#
def selectTheaters():
    s = select([theaters]).where(theaters.c.available == True)
    conn = engine.connect()
    result = conn.execute(s)
    conn.close()
    return result

@app.route("/listTheaters")
@login_required(Role.SUPERVISOR)
def listTheaters():
    res = selectTheaters()
    return render_template("/tables/theater/listTheaters.html", result = res)

#---------------------------------INSERT---------------------------------#
#mi sembra non vada un cazzo
@app.route("/insertTheater", methods=['GET', 'POST'])
@login_required(Role.SUPERVISOR)
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
                #time.sleep(30)
                session.execute(
                            theaters.insert().\
                                values(id = bindparam('id'), seatsCapacity = bindparam('capacity')),
                            { 'id' : id, 'capacity' : capacity}

                        )
                session.commit()
                flash("Sala inserita!",'info' )
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
    return render_template("/tables/theater/insertTheater.html")

#---------------------------------DELETE---------------------------------#

"""
    Ci sono tre opzioni per la cancellazione e viene scelta dell'utente:
            1. Cancella se spettacoli collegati sono solo passati -> quindi la metto non disponibile (Per l'utente è come fosse)
            2. Se ci sono spettacoli collegati FUTURI rifiuta la cancellazione
            3. Se NON ci sono spettacoli collegati posso eliminarlo
"""

@app.route("/removeTheater", methods=['GET', 'POST'])
@login_required(Role.SUPERVISOR)
def removeTheater():
    if request.method == 'POST':
        id = request.form.get("id")
        if id :
            #verifico se ci sono spettacoli collegati
            sel = select([movieSchedule]).\
                    where( movieSchedule.c.theater == bindparam('id'))
            
            if queryHasResult(sel, {'id' : id}):
                #verifico se gli spettacoli collegati sono futuri
                sel = select([movieSchedule]).\
                        where( 
                            and_(
                                movieSchedule.c.theater == bindparam('id'),
                                movieSchedule.c.dateTime >= datetime.today()#prima avevo now ma today è senza timezone
                            )
                        )
                
                if queryHasResult(sel, {'id' : id}):
                    #non posso cancellare
                    flash(  """Non si può rimuovere la sala {} perchè ci sono proiezioni non ancora andate in onda.\n
                                Riassegna le proiezioni ad un altra sala. """.format(id), 'error')
                else:    
                    #devo mettere non disponibile
                    up = theaters.update().\
                        where(theaters.c.id == bindparam('t_id')).\
                        values(available = False)
                    flash("Sala rimossa!", 'info')
                    return queryAndFun(up, 'listTheaters', {'t_id' : id})
            else:
                #posso cancellarlo
                rm = theaters.delete().\
                    where(theaters.c.id == bindparam('id'))
                flash("Sala rimossa!", 'info')
                return queryAndFun(rm, 'listTheaters', {'id' : id})

        else:
            flash('You have to insert the value to remove', 'error')
    result = selectTheaters()    
    return render_template("/tables/theater/removeTheater.html", result = result)
#---------------------------------UPDATE---------------------------------#

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
                
                #TODO forse si potrebbe mettere in shared
          
            conn = engine.connect()
            result = conn.execute(sel, {'id' : id}).fetchone()
            conn.close()
      
            return render_template('/tables/theater/modifyTheater.html',theater  = result)
        else:
            flash('Inserire i dati richiesti !', 'error')

    result = selectTheaters()    
    return render_template("/tables/theater/updateTheater.html", result = result)

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


