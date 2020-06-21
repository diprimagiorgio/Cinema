from sqlalchemy import  select, bindparam

from app.model import clients, managers
from app import app, engine

#solo per test poi si può eliminare
@app.route("/pay/<id_cl>/<amount>")
def paga(id_cl, amount):
    if(pay(id_cl, amount)):
        return "Pagamento è andato a buon fine"
    else:
        return "Pagamento FALLITO"

"""
    Devo prendere un amount da un cliente e trasferirlo all'amministartore
"""
#Diprima Giorgio
def pay(id, amount):
    conn = engine.connect()
    trans = conn.begin()
    try:
      
        #Se il credito non è sufficiente il db manda un errore per il check
        #rimuovo il credito dall'utente
        u_cl = clients.update().\
                    where(clients.c.id == bindparam('id_cl')).\
                    values( credit =  clients.c.credit - float(amount) )

        conn.execute(u_cl, {'id_cl' : id})
        #selezione dell'id del manager
        s_mn = select([managers]).\
                where(managers.c.admin == True)
        result = conn.execute(s_mn).fetchone()
        #decremento il bilancio dell'amministratore
        u_mn = managers.update().\
                where(managers.c.id == result['id']).\
                values( financialReport = result['financialReport'] + float(amount) )
        conn.execute(u_mn)

        trans.commit()
        resp = True
    except:
        trans.rollback()
        resp = False
    finally:
        conn.close()
        trans.close()
        return resp