from app import app, engine
from flask import redirect, render_template, make_response, url_for

#def queryHasResult(q):
#    conn = engine.connect()
#    result = conn.execute(q).fetchone()
#    conn.close()
#    return True if result else False

def queryHasResult(q, args = None):
    conn = engine.connect()
    if args:
        result = conn.execute(q, args).fetchone()
    else:
        result = conn.execute(q).fetchone()
    conn.close()
    return True if result else False


def queryAndTemplate(s, htmlTemplate, otherPar=""):
    conn = engine.connect()
    result = conn.execute(s)
    resp = make_response(render_template(htmlTemplate, result = result, par = otherPar))
    conn.close()
    return resp
#
#def queryAndFun(s, nameFun):
#    conn = engine.connect()
#    result = conn.execute(s)
#    conn.close()
#    return redirect(url_for(nameFun))

def queryAndFun(s, nameFun, args = None):
    conn = engine.connect()
    if args:
        result = conn.execute(s,args)
    else:
        result = conn.execute(s)

    conn.close()
    return redirect(url_for(nameFun))