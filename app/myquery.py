from app import app
from sqlalchemy import insert, select, delete, bindparam, func
from flask import  request, flash, render_template, redirect, url_for

from app.model import genres, movies
from .shared import queryAndTemplate, queryAndFun, queryHasResult
import time
from app.login import Role, login_required
from app.engineFunc import choiceEngine
from flask_login import current_user
#genere preferito
"""
    CREATE VIEW "countGenre" AS 
        SELECT c.id AS id , m."idGenre", COUNT(m."idGenre") AS prenotazioni
        FROM (((clients c LEFT JOIN booking b ON c.id = b."clientUsername")
                LEFT JOIN "movieSchedule" ms ON ms.id = b."idmovieSchedule")
                LEFT JOIN Movies m ON m.id = ms."idMovie")
        GROUP BY c.id, m."idGenre"

   
                        
    SELECT *
    FROM countGenre cg
    WHERE cg.id = CURRENTUSER AND 
        cg.prenotazioni  = (SELECT MAX( cg2.prenotazioni )
                               FROM countGenre cg2
                               WHERE cg.id = cg2.id  )
    
"""
@app.route("/prova")
def foo():
    view = text(
    """
    CREATE VIEW "countGenre" AS 
        SELECT c.id AS id , m."idGenre", COUNT(m."idGenre") AS prenotazioni
        FROM (((clients c LEFT JOIN booking b ON c.id = b."clientUsername")
                LEFT JOIN "movieSchedule" ms ON ms.id = b."idmovieSchedule")
                LEFT JOIN Movies m ON m.id = ms."idMovie")
        GROUP BY c.id, m."idGenre"

    """
    )
 #   countGenre = CreateView('countGenre', 
 #       select([clients.c.id.label("id"), movies.c.idGenre.label("genredescription"), fun.count(movie.c.genre.id).label("prenotazioni")]).\
 #           select_from(clients.join(booking, clinets.c.id == booking.c.))
 #   
 #   )
    sel = select([countGenre.label("cg")]).\
        where(
            and_(
                cg.c.id == current_user.get_id(),
                cg.c.id == (
                        select([ func.max(countGenre.c.prenotazioni) ]).\
                            select_from(countGenre.label("cg2"))
                            where( cg.c.id = cg2.c.id )
                        )
            )
        )
    conn = choiceEngine()
    result = conn.execute(view)
    result = conn.execute(sel)



    conn.close()


# Per ogni tipologia di film trovare trovare il cliente con più prenotazioni
