from sqlalchemy import insert, select, func
from app.model import genres, movies, theaters, movieSchedule, booking
from app import app, engineAdmin
from datetime import date
from app.functionForBooking import createIntegerListFromQuery, convertToInt


@app.route("/prova")
def initMovieSchedule():
    N_PROIEZIONI = 1 #numero di proiezioni che voglio inserire
    PREZZO = 5 #prezzo biglietto
    MESE = 12 #mesi di proiezioni
    GIORNO = 28 #giorni di proiezioni
    ANNO = ["2015","2016","2017","2018","2019","2020"] #anni di proiezioni
    ORA = ["09:00:00", "11:30:00", "14:00:00", "16:30:00", "19:00:00", "21:30:00"] #ore di proiezioni
    conn = engineAdmin.connect() 
    movie = select([func.count(movies.c.id)]).\
              select_from(movies)
    N_FILM = convertToInt(str(conn.execute(movie).fetchone()))#numero di idmovie disponibili
    theater = select([theaters.c.id]).\
              select_from(theaters)
    N_SALA = createIntegerListFromQuery(conn.execute(theater).fetchall())#lista con tutte le sale              
    conn.close()
                
    film = 1
    proiezioni = 1

    conn = engineAdmin.connect() 
    for anno in ANNO:
        for mese in range(MESE):
            for giorno in range(GIORNO):
                for ora in ORA:
                    for sala in N_SALA:
                        ins = movieSchedule.insert().\
                        values(dateTime = anno + "-" + str(mese+1) + "-" + str(giorno+1) + " " + ora, price = PREZZO, idMovie = film % N_FILM, theater = sala)
                        conn.execute(ins)
                        film = film + 1
                        if (proiezioni == N_PROIEZIONI):
                            conn.close()
                            return "Finito"
                        proiezioni = proiezioni + 1                  
    return "OK"
                
                
                
                
@app.route("/prova2")
def initBooking():
    N_PRENOTAZIONI = 1
    NOMI = ["Luca", "Giovanni", "Mario", "Lucia", "Anna", "Assunta", "Giorgio", "Davide", "Michele", "Dario", "Valentina", "Sofia", "Daniela", "Gaia"]
    ETA_MIN = 20
    ETA_MAX = 60


booking.insert().\
        values(viewerName = bindparam('viewer'), viewerAge = bindparam('viewerAge'), seatNumber = bindparam('seatNumber'), 
               clientUsername = current_user.get_id(), idmovieSchedule = bindparam('idmovieSchedule'))








@app.route("/__init")
def initializer():
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
    
    
    
    conn.execute(theaters.insert(),[
    {'seatsCapacity': 100},
    {'seatsCapacity': 100},
    {'seatsCapacity': 60},
    {'seatsCapacity': 80},
    {'seatsCapacity': 40},
    {'seatsCapacity': 40},
    ])
    
    
 #   conn.execute(booking.insert(),[
 # #  { 'viewerName': 'A', 'viewerAge': '15', 'seatNumber': 1, 'clientUsername': 1 ,'idmovieShedule' : 1},
 # #  { 'viewerName': 'B', 'viewerAge': '15', 'seatNumber': 2, 'clientUsername': 1 ,'idmovieShedule' : 1},
 # #  { 'viewerName': 'C', 'viewerAge': '15', 'seatNumber': 3, 'clientUsername': 1 ,'idmovieShedule' : 1},
 # #  { 'viewerName': 'D', 'viewerAge': '18', 'seatNumber': 4, 'clientUsername': 1 ,'idmovieShedule' : 1},
 # #  { 'viewerName': 'E', 'viewerAge': '18', 'seatNumber': 5, 'clientUsername': 2 ,'idmovieShedule' : 1},
 # #  { 'viewerName': 'F', 'viewerAge': '60', 'seatNumber': 6, 'clientUsername': 2 ,'idmovieShedule' : 1},
 # #  { 'viewerName': 'G', 'viewerAge': '50', 'seatNumber': 7, 'clientUsername': 2 ,'idmovieShedule' : 1},
 # #  { 'viewerName': 'H', 'viewerAge': '60', 'seatNumber': 8, 'clientUsername': 2 ,'idmovieShedule' : 2},
 # #  { 'viewerName': 'I', 'viewerAge': '45', 'seatNumber': 9, 'clientUsername': 2 ,'idmovieShedule' : 2},
 # #  { 'viewerName': 'L', 'viewerAge': '45', 'seatNumber': 10, 'clientUsername': 3 ,'idmovieShedule' : 2},
 # #  { 'viewerName': 'M', 'viewerAge': '35', 'seatNumber': 11, 'clientUsername': 5 ,'idmovieShedule' : 2},
 # #  { 'viewerName': 'N', 'viewerAge': '35', 'seatNumber': 12, 'clientUsername': 5 ,'idmovieShedule' : 3},
 # #  { 'viewerName': 'O', 'viewerAge': '32', 'seatNumber': 13, 'clientUsername': 3 ,'idmovieShedule' : 3},
 #   { 'viewerName': 'P', 'viewerAge': '27', 'seatNumber': 14, 'clientUsername': 3 ,'idmovieShedule' : 3},
 #   { 'viewerName': 'Q', 'viewerAge': '28', 'seatNumber': 15, 'clientUsername': 3 ,'idmovieShedule' : 3},
 #   { 'viewerName': 'R', 'viewerAge': '27', 'seatNumber': 16, 'clientUsername': 3 ,'idmovieShedule' : 3},
 #   { 'viewerName': 'S', 'viewerAge': '27', 'seatNumber': 17, 'clientUsername': 6 ,'idmovieShedule' : 3},
 #   { 'viewerName': 'T', 'viewerAge': '12', 'seatNumber': 18, 'clientUsername': 6 ,'idmovieShedule' : 3},
 #   { 'viewerName': 'U', 'viewerAge': '12', 'seatNumber': 19, 'clientUsername': 7 ,'idmovieShedule' : 3},
 #   { 'viewerName': 'V', 'viewerAge': '12', 'seatNumber': 20, 'clientUsername': 2 ,'idmovieShedule' : 2},
 #   ])
    
    
    conn.close()
    return "Done"
    
