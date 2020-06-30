from flask import  render_template, make_response, request, flash, redirect
from flask_login import LoginManager, UserMixin, current_user, login_user
from sqlalchemy import select, func
from app.model import clients, users
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