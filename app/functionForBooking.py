from flask import make_response, render_template
from app import app, engine
import time 
from threading import Thread 




temporaryBooking = {} #mi tiene traccia dei posti in fase di prenotazione, come chiave si usa il numero della sala
timeOutBooking = {} #mi tiene traccia del time out per la prenotazione di ogni utente (thread utente), come chiave si usa id utente


#----------------------------Funzioni varie

 #converte stringa in int
def convertToInt(s):
    val = ''
    for i in range(len(s)):
        if '0' <= s[i] <= '9':
            val = val + s[i]
    if val == '':
        val = '0'
    return int(val)     

 #crea una lista da una query
def createIntegerListFromQuery(iter):
    l = []
    for u in iter:
        l.append(convertToInt(str(u)))
    return l

 #trasforma una stringa tupla in una lista di interi
def createIntegerListFromString(string):
    l = []
    val = ''
    for i in range(len(string)):
        if '0' <= string[i] <= '9':
            val = val + string[i]
        elif string[i] == ',':
            l.append(int(val))
            val = ''
    l.append(int(val))
    return l

 #torna true nel caso in cui ci sia l'elemento dentro alla lista
def searchInList(l, elem):
    check = False
    for x in l:
        if x == elem:
            check = True
    return check



#----------------------------Funzioni per la lista temporanea

 #rimuove la lista dei posti del singolo utente
def removeElemInTemporaryList(listOfBooking, idmovieSchedule):
    for elem in listOfBooking:
        temporaryBooking[idmovieSchedule].remove(elem)  

 #se la chiave non è presente aggiungila
def KeyIsInTemporaryList(idmovieSchedule):
    if not (idmovieSchedule in temporaryBooking):
        temporaryBooking[idmovieSchedule] = []

 #se la lista dell'utente non ha nulla in comune aggiungila e ritorna true, altrimenti torna false
def isNotInTemporaryList(idmovieSchedule, listOfBooking):
    check = True
    for elem in temporaryBooking[idmovieSchedule]: #controlla se c'è già qualcuno che sta prenotando questi posti
        if searchInList(listOfBooking, elem):
            check = False
    if check: #se nessuno sta prenotando questi posti aggiungili alla lista temporanea
        temporaryBooking[idmovieSchedule].extend(listOfBooking)
    return check

 #aggiunge alla lista la lista temporanea
def addTemporaryListInList(idmovieSchedule, l):
    l.extend(temporaryBooking[idmovieSchedule])
    
    
      
#----------------------------Funzioni per il thread timer

class TimerForBooking(Thread):
    def __init__(self, idmovieSchedule, listOfBooking, current_user, time):
        Thread.__init__(self)
        self.stop = False
        self.idmovieSchedule = idmovieSchedule
        self.listOfBooking = listOfBooking
        self.time = time
        self.current_user = current_user
        
    def kill(self):
        self.stop = True
    
    def run(self):
        s = 1
        while s <= self.time:
            time.sleep(1)
            s += 1    
            if self.stop:
                break
        if not self.stop:    
            removeElemInTemporaryList(self.listOfBooking, self.idmovieSchedule)
        (timeOutBooking.get(self.current_user))[1] = False # metto a false il bool del thread
        
 #crea nel dizionario la chiave con current user con elemento il thread timer e fa lo start      
def startTimer(idmovieSchedule, listOfBooking, time, current_user):
    timeOutBooking[current_user] = [TimerForBooking(idmovieSchedule, listOfBooking, current_user, time), True]
    (timeOutBooking.get(current_user)[0]).start()

 #controlla lo stato del thread, se è ancora attivo lo blocco e torno true altrimenti torno false
def timerIsAlive(current_user):
    alive = False
    if timeOutBooking.get(current_user)[1]: # in caso sia true
        alive = True
        (timeOutBooking.get(current_user)[0]).kill()
        (timeOutBooking.get(current_user)[0]).join()
    timeOutBooking.pop(current_user)
    return alive
 #verifica se c'è già una prenotazione in corso per questo utente
def timerBookingInProgress(current_user):
    if timeOutBooking.get(current_user):
        return timeOutBooking.get(current_user)[1]
    return False
