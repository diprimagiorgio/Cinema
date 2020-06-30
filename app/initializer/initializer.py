from sqlalchemy import insert, select, func
from app.model import genres, movies, theaters, movieSchedule, booking, clients, users, managers
from app import app, engineAdmin
from datetime import date
from app.user.functionForBooking import createIntegerListFromQuery, convertToInt
from random import randint



def initUser():
    UTENTI_INSERITI= 15
    CREDITI = [20, 30, 40, 55, 60, 75]
    NOMI = ["Luca", "Giovanni", "Mario", "Lucia", "Anna", "Assunta", "Giorgio", "Davide", "Michele", "Dario", "Valentina", "Sofia", "Daniela", "Gaia"]
    COGNOMI = ["Rossi", "Sartori", "Bedin", "Rigon", "Casarotto", "Pavan", "Zanatta", "Scarpa", "Costantini", "Carraro"]
    MAX_ANNO = 2000
    nome = cognome = credito = 0
    anno = MAX_ANNO - UTENTI_INSERITI
    for i in range(UTENTI_INSERITI):
        conn = engineAdmin.connect()
        email = NOMI[nome % len(NOMI)] + str(i) + "@gmail.it"
        insuser = users.insert().values(name = NOMI[nome % len(NOMI)], surname = COGNOMI[cognome % len(COGNOMI)], 
                                    email = email, password = 1)  
        conn.execute(insuser)
        query = select([users.c.id]).where(users.c.email == email)
        ris = convertToInt(str(conn.execute(query).fetchone()))
        insclients= clients.insert().values(id = ris, birthDate = str(anno) + "-03-12", credit= CREDITI[credito % len(CREDITI)])  
        conn.execute(insclients)
        conn.close()
        nome = nome + 1
        cognome = cognome + 1
        credito = credito + 1
        anno = anno + 1

        
def initManager():
    MANAGER_INSERITI= 5
    NOMI = ["Luca", "Giovanni", "Mario", "Lucia", "Anna", "Assunta", "Giorgio", "Davide", "Michele", "Dario", "Valentina", "Sofia", "Daniela", "Gaia"]
    COGNOMI = ["Rossi", "Sartori", "Bedin", "Rigon", "Casarotto", "Pavan", "Zanatta", "Scarpa", "Costantini", "Carraro"]
    nome = cognome = 0
    for i in range(MANAGER_INSERITI):
        conn = engineAdmin.connect()
        email = COGNOMI[cognome % len(COGNOMI)] + str(i) + "@ilMolo.it"
        insuser = users.insert().values(name = NOMI[nome % len(NOMI)], surname = COGNOMI[cognome % len(COGNOMI)], 
                                    email = email, password = 1)  
        conn.execute(insuser)
        query = select([users.c.id]).where(users.c.email == email)
        ris = convertToInt(str(conn.execute(query).fetchone()))
        insmanagers= managers.insert().values(id = ris, admin = False, financialReport=None)  
        conn.execute(insmanagers)
        conn.close()
        nome = nome + 1
        cognome = cognome + 1

def initAdmin():
    ins = users.insert().values(name="Admin", surname ="Admin", email ="admin@admin.com", password = "secret")    
    
    conn = engineAdmin.connect()
    conn.execute(ins)

    query = select([users]).where(users.c.email == "admin@admin.com")#mi serve per ritrovarmi l'ID corretto
    ris = conn.execute(query).fetchone()

    ins = managers.insert().values(id = ris.id , admin = True , financialReport=0)
    conn.execute(ins)
    conn.close()


def initSchedule():
    PREZZO = 5 #prezzo biglietto
    MESE = ["6", "7"] #mesi di proiezioni
    GIORNO = 28 #giorni di proiezioni
    ANNO = ["2020"] #anni di proiezioni
    ORA = ["14:00:00", "16:30:00", "19:00:00"] #ore di proiezioni
    conn = engineAdmin.connect() 
    movie = select([func.count(movies.c.id)]).\
              select_from(movies)
    N_FILM = convertToInt(str(conn.execute(movie).fetchone()))#numero di idmovie disponibili
    theater = select([theaters.c.id]).\
              select_from(theaters)
    N_SALA = createIntegerListFromQuery(conn.execute(theater).fetchall())#lista con tutte le sale              
    conn.close()         
    film = 0
    giorno = 0
    conn = engineAdmin.connect() 
    for anno in ANNO:
        for mese in MESE:
            if(mese == "7"):
                GIORNO = 7
                giorno = 0
            while giorno <= GIORNO:
                giorno = giorno + 2           
                for ora in ORA:
                    for sala in N_SALA:
                        ins = movieSchedule.insert().\
                        values(dateTime = anno + "-" + mese + "-" + str(giorno) + " " + ora, price = PREZZO, idMovie = (film % N_FILM) + 1, theater = sala)
                        conn.execute(ins)
                        film = film + 1   
    conn.close()
                
                
                
def initBooking():
    PREZZO = 5
    NOMI = ["Luca", "Giovanni", "Mario", "Lucia", "Anna", "Assunta", "Giorgio", "Davide", "Michele", "Dario", "Valentina", "Sofia", "Daniela", "Gaia"]
    ETA_MIN = 18
    ETA_MAX = 85
    RIEMPIMENTO_SALA=[-40, -30, -22]
    conn = engineAdmin.connect() 
    query = select([func.count(movieSchedule.c.id)]).\
              select_from(movieSchedule)
    N_SCHEDULE = convertToInt(str(conn.execute(query).fetchone()))#numero di programmazioni totali
    query = select([clients.c.id]).\
              select_from(clients.join(users, clients.c.id == users.c.id))
    UTENTI = createIntegerListFromQuery(conn.execute(query).fetchall())#lista con tutti i clienti
    conn.close()
    riempi = -1
    nome = 0
    utente = 0
    soldi = 0
    for schedule in range(N_SCHEDULE):
        riempi = riempi + 1
        conn = engineAdmin.connect()
        query = select([theaters.c.seatsCapacity]).\
                     select_from(theaters.join(movieSchedule, movieSchedule.c.theater == theaters.c.id)).\
                     where(movieSchedule.c.id == (schedule + 1))
        totalSeats = convertToInt(str(conn.execute(query).fetchone()))#numero di posti nella sala
        conn.close()
        conn = engineAdmin.connect() 
        for seat in range(totalSeats + RIEMPIMENTO_SALA[riempi % len(RIEMPIMENTO_SALA)]):
            ins = (booking.insert().\
                    values(viewerName = NOMI[nome % len(NOMI)], viewerAge = randint(ETA_MIN, ETA_MAX), seatNumber = seat + 1, 
                    clientUsername = UTENTI[utente % len(UTENTI)], idmovieSchedule = schedule + 1))
            conn.execute(ins)
            nome = nome + 1
            utente = utente + 1
            soldi = soldi + PREZZO
        conn.close()
    conn = engineAdmin.connect()
     #selezione dell'id del manager
    s_mn = select([managers]).\
            where(managers.c.admin == True)
    result = conn.execute(s_mn).fetchone()
    #incremento il bilancio dell'amministratore
    u_mn = managers.update().\
            where(managers.c.id == result['id']).\
            values( financialReport = result['financialReport'] + float(soldi))
    conn.execute(u_mn)
    conn.close()   
            
        
def initGenre():
    conn = engineAdmin.connect()
    conn.execute(genres.insert(),[
        {'description': 'Animazione'},
        {'description': 'Azione'},
        {'description': 'Avventura'},
        {'description': 'Biografico'},
        {'description': 'Commedia'},
        {'description': 'Documentario'},
        {'description': 'Drammatico'},
        {'description': 'Pornografico'},
        {'description': 'Erotico'},
        { 'description': 'Fantascienza'},
        { 'description': 'Fantasy'},
        { 'description': 'Guerra'},
        { 'description': 'Horror'},
        { 'description': 'Musical'},
        { 'description': 'Storico'},
        { 'description': 'Thriller'},
        { 'description': 'Western'}
    ])
    conn.close()
    
    
def initMovie():
    conn = engineAdmin.connect()
    conn.execute(movies.insert(),[
        { 'title':'Tolo Tolo','minimumAge': 0,'duration': 90, 'idGenre': 5},
        { 'title':'L\'immortale','minimumAge': 13,'duration': 116, 'idGenre': 7},
        { 'title':'Pinocchio','minimumAge': 0,'duration': 112, 'idGenre': 1},
        { 'title':'Odio L\'estate','minimumAge': 12,'duration': 110, 'idGenre': 5},
        { 'title':'Il richiamo della foresta','minimumAge': 14,'duration': 100, 'idGenre': 7},
        { 'title':'Dolittle','minimumAge': 0,'duration': 106, 'idGenre': 5},
        { 'title':'Bad boys for life','minimumAge': 14,'duration': 113, 'idGenre': 2},
        { 'title':'7 ore per farti innamorare','minimumAge': 0,'duration': 112, 'idGenre': 5},
        { 'title':'Sonic','minimumAge': 0,'duration': 100, 'idGenre': 1},
        { 'title':'Ultras','minimumAge': 13,'duration': 108, 'idGenre': 7},
        { 'title':'Fast & Furious 9','minimumAge': 14,'duration': 132, 'idGenre': 2},
        { 'title':'Mulan','minimumAge': 0,'duration': 115, 'idGenre': 1},
        { 'title':'Rec','minimumAge': 16,'duration': 85, 'idGenre': 13},
        { 'title':'IT capitolo uno','minimumAge': 16,'duration': 135, 'idGenre': 13},
        { 'title':'Suspiria','minimumAge': 13,'duration': 112, 'idGenre': 13},
        { 'title':'Lasciami entrare','minimumAge': 16,'duration': 114, 'idGenre': 13},
        { 'title':'The kid','minimumAge': 0,'duration': 112, 'idGenre': 17},
        { 'title':'Deadwood','minimumAge': 0,'duration': 110, 'idGenre':17},
        { 'title':'50 sfumature di rosso','minimumAge': 14,'duration': 110, 'idGenre': 9},
        { 'title':'Diego Maradona','minimumAge': 0,'duration': 130, 'idGenre': 6},
        { 'title':'Free solo','minimumAge': 0,'duration': 140, 'idGenre': 6},
        { 'title':'Terminator','minimumAge': 14,'duration': 128, 'idGenre': 10},
        { 'title':'Man in black international','minimumAge': 14,'duration': 115, 'idGenre': 10},
        { 'title':'Love','minimumAge': 18,'duration': 110, 'idGenre': 9}
    ])
    conn.close()
  
         
def initTheater():
    conn = engineAdmin.connect()
    conn.execute(theaters.insert(),[
        {'seatsCapacity': 80},
        {'seatsCapacity': 60},
        {'seatsCapacity': 80},
        {'seatsCapacity': 40}
    ])
    conn.close()
    


def initializer():
    initAdmin()
    initManager()
    initUser()
    initGenre()
    initTheater()
    initMovie()
    initSchedule()
    initBooking()
    return "Done"
    
