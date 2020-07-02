from flask import  render_template, make_response, request, flash, redirect
from flask_login import LoginManager, UserMixin, current_user, login_user
from sqlalchemy import select, func
from app.model import clients, users, booking, movieSchedule, movies, genres
from app import app
from app.shared.login import Role, login_required
from app.engineFunc import choiceEngine



#Luca Bizzotto
@app.route("/accountInfo")
@login_required(Role.CLIENT)

def account_info() :
    conn = choiceEngine()
    join = users.join(clients, users.c.id == clients.c.id)
    query = select([users,clients]).select_from(join).where(users.c.id == current_user.get_id())
    u = conn.execute(query)          #ritorna none se non contiene nessuna riga    
    resp = make_response(render_template("/user/logged/accountInfo.html", infoPersonali = u))
    conn.close()
    return resp

#Luca Bizzotto
@app.route("/updateCredit",methods = ['GET','POST'])
@login_required(Role.CLIENT)

def change1():
    if request.method == 'POST':
        money = request.form.get("import")
        conn = choiceEngine()
        base = select([clients]).where(clients.c.id == current_user.get_id())
        ris = conn.execute(base).fetchone()
        if float(money) < 0 :
            #non si accettano ricariche negative
            flash("Non puoi inserire valori negativi!",'error')
            return redirect("/updateCredit")
        query = clients.update().values(credit = float(money) + float(ris.credit)).where(clients.c.id == current_user.get_id())
        flash("Ricarica avvenuta con successo!",'info' )
        conn.execute(query)
        conn.close()
        return redirect("/updateCredit")
    else:
        return render_template("/user/logged/updateCredit.html")
    
#mi permette di visualizzare per il cliente loggato il numero di film prenotati per genere
@app.route("/numeroFilmPrenotatiPerGenere")
@login_required(Role.CLIENT)
def soldispesi():
    conn = choiceEngine()
    
    ris = select([func.count(booking.c.id).label('count'),genres.c.description]).\
        select_from(
            booking.join(movieSchedule, booking.c.idmovieSchedule == movieSchedule.c.id).\
            join(movies, movieSchedule.c.idMovie == movies.c.id).\
            join(genres, movies.c.idGenre == genres.c.id)).\
        where(current_user.get_id()== booking.c.clientUsername).\
        group_by(movies.c.idGenre,genres.c.description).\
        order_by(func.count(booking.c.id).desc())
        
    y = conn.execute(ris).fetchall()
    
    conn.close()
    return render_template("/user/logged/visualizzazioni.html", fav= y)