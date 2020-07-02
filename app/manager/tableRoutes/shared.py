from app import app
from flask import redirect, render_template, make_response, url_for
from app.engineFunc import choiceEngine, engineAdmin

#file Diprima Giorgio


def queryHasResult(q, args = None):
    conn = choiceEngine()
    if args:
        result = conn.execute(q, args).fetchone()
    else:
        result = conn.execute(q).fetchone()
    conn.close()
    return True if result else False

def queryHasResultWithConnection(q,  conn , args = None):
    if args:
        result = conn.execute(q, args).fetchone()
    else:
        result = conn.execute(q).fetchone()
    return True if result else False

def queryAndTemplate(s, htmlTemplate, otherPar=""):
    conn = choiceEngine()
    result = conn.execute(s)
    resp = make_response(render_template(htmlTemplate, result = result, par = otherPar))
    conn.close()
    return resp

def queryAndFun(s, nameFun, args = None):
    conn = choiceEngine()
    if args:
        result = conn.execute(s,args)
    else:
        result = conn.execute(s)

    conn.close()
    return redirect(url_for(nameFun))