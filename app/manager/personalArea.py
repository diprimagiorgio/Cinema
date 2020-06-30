from flask import  render_template
from sqlalchemy import select
from app.model import managers
from app import app
from app.shared.login import Role, login_required
from app.engineFunc import choiceEngine

#Giorgio Diprima
@app.route('/dataBase')
@login_required(Role.SUPERVISOR)
def dataBase():
    return render_template("/tables/menuTable.html")
    
#Giorgio Diprima
@app.route('/financialReport')
@login_required(Role.ADMIN)
def financialReport():
    sel = select([managers]).\
            where( managers.c.admin == True)
    conn = choiceEngine()
    res = conn.execute(sel).fetchone()
    conn.close()
    return render_template("/manager/admin/financialReport.html", result = res)
