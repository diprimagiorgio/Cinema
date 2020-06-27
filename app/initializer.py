from sqlalchemy import insert
from app.model import genres, movies, theaters, movieSchedule, booking
from app import app, engine
from datetime import date

@app.route("/init")
def initializer():
    conn = engine.connect()
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
        { 'title':'Tolo Tolo','duration': 90, 'idGenre': 5},
        { 'title':'L\'immortale','minimumAge': 13,'duration': 116, 'idGenre': 7},
        { 'title':'Pinocchio','duration': 112, 'idGenre': 1},
        { 'title':'Odio L\'estate','minimumAge': 12,'duration': 110, 'idGenre': 5},
        { 'title':'Il richiamo della foresta','minimumAge': 14,'duration': 100, 'idGenre': 7},
        { 'title':'Dolittle','duration': 106, 'idGenre': 5},
        { 'title':'Bad boys for life','minimumAge': 14,'duration': 113, 'idGenre': 2},
        { 'title':'7 ore per farti innamorare','duration': 112, 'idGenre': 5},
        { 'title':'Sonic','duration': 100, 'idGenre': 1},
        { 'title':'Ultras','minimumAge': 13,'duration': 108, 'idGenre': 7},
        { 'title':'Fast & Furious 9','minimumAge': 14,'duration': 132, 'idGenre': 2},
        { 'title':'Mulan','duration': 115, 'idGenre': 1},
        { 'title':'Rec','minimumAge': 16,'duration': 85, 'idGenre': 13},
        { 'title':'IT capitolo uno','minimumAge': 16,'duration': 135, 'idGenre': 13},
        { 'title':'Suspiria','minimumAge': 13,'duration': 152, 'idGenre': 13},
        { 'title':'Lasciami entrare','minimumAge': 16,'duration': 114, 'idGenre': 13},
        { 'title':'The kid','duration': 112, 'idGenre': 17},
        { 'title':'Deadwood','duration': 110, 'idGenre':17},
        { 'title':'50 sfumature di rosso','minimumAge': 14,'duration': 110, 'idGenre': 9}
        { 'title':'Diego Maradona','duration': 130, 'idGenre': 6}
        { 'title':'Free solo','duration': 140, 'idGenre': 6}
        { 'title':'Terminator','minimumAge': 14,'duration': 128, 'idGenre': 10}
        { 'title':'Man in black international','minimumAge': 14,'duration': 115, 'idGenre': 10}
        { 'title':'Love','minimumAge': 18,'duration': 110, 'idGenre': 9}
    ])
    
    
    
    conn.execute(theaters.insert(),[
    {'seatsCapacity': 100},
    {'seatsCapacity': 100},
    {'seatsCapacity': 60},
    {'seatsCapacity': 80},
    {'seatsCapacity': 30},
    {'seatsCapacity': 40},
    ])
    
    conn.execute(movieSchedule.insert(),[
    {'dateTime': date.today(), 'price': 6.5,'theater':1, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 5,'theater':2, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 5,'theater':3, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 5,'theater':4, 'idMovie': 4},
    {'dateTime': date.today(), 'price': 6.5,'theater':5, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 6.5,'theater':6, 'idMovie': 6},
    {'dateTime': date.today(), 'price': 6.5,'theater':1, 'idMovie': 6},
    {'dateTime': date.today(), 'price': 6.5,'theater':2, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 6.5,'theater':3, 'idMovie': 4},
    {'dateTime': date.today(), 'price': 10,'theater':4, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 10,'theater':5, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 10,'theater':6, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 10,'theater':2, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 6.5,'theater':3, 'idMovie': 4},
    {'dateTime': date.today(), 'price': 6.5,'theater':4, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 6.5,'theater':5, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 6.5,'theater':6, 'idMovie': 6},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 10,'theater':2, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 6.5,'theater':3, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 6.5,'theater':4, 'idMovie': 4},
    {'dateTime': date.today(), 'price': 6.5,'theater':5, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 6.5,'theater':6, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 10,'theater':2, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 6.5,'theater':3, 'idMovie': 4},
    {'dateTime': date.today(), 'price': 6.5,'theater':4, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 6.5,'theater':5, 'idMovie': 6},
    {'dateTime': date.today(), 'price': 6.5,'theater':6, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 10,'theater':2, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 6.5,'theater':3, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 6.5,'theater':4, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 6.5,'theater':5, 'idMovie': 4},
    {'dateTime': date.today(), 'price': 6.5,'theater':6, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 10,'theater':2, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 6.5,'theater':3, 'idMovie': 4},
    {'dateTime': date.today(), 'price': 6.5,'theater':4, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 6.5,'theater':5, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 6.5,'theater':6, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 4},
    {'dateTime': date.today(), 'price': 10,'theater':2, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 6.5,'theater':3, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 6.5,'theater':4, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 6.5,'theater':5, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 6.5,'theater':6, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 10,'theater':2, 'idMovie': 4},
    {'dateTime': date.today(), 'price': 6.5,'theater':3, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 6.5,'theater':4, 'idMovie': 4},
    {'dateTime': date.today(), 'price': 6.5,'theater':5, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 6.5,'theater':6, 'idMovie': 4},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 10,'theater':2, 'idMovie': 6},
    {'dateTime': date.today(), 'price': 6.5,'theater':3, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 6.5,'theater':4, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 6.5,'theater':5, 'idMovie': 5},
    {'dateTime': date.today(), 'price': 6.5,'theater':6, 'idMovie': 1},
    
    
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 11},
    {'dateTime': date.today(), 'price': 10,'theater':2, 'idMovie': 12},
    {'dateTime': date.today(), 'price': 6.5,'theater':3, 'idMovie': 13},
    {'dateTime': date.today(), 'price': 6.5,'theater':4, 'idMovie': 14},
    {'dateTime': date.today(), 'price': 6.5,'theater':5, 'idMovie': 15},
    {'dateTime': date.today(), 'price': 6.5,'theater':6, 'idMovie': 16},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 17},
    {'dateTime': date.today(), 'price': 10,'theater':2, 'idMovie': 18},
    {'dateTime': date.today(), 'price': 6.5,'theater':3, 'idMovie': 19},
    {'dateTime': date.today(), 'price': 6.5,'theater':4, 'idMovie': 20},
    {'dateTime': date.today(), 'price': 6.5,'theater':5, 'idMovie': 21},
    {'dateTime': date.today(), 'price': 6.5,'theater':6, 'idMovie': 22},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 23},
    {'dateTime': date.today(), 'price': 10,'theater':2, 'idMovie': 24},
    {'dateTime': date.today(), 'price': 6.5,'theater':3, 'idMovie': 25},
    {'dateTime': date.today(), 'price': 6.5,'theater':4, 'idMovie': 22},
    {'dateTime': date.today(), 'price': 6.5,'theater':5, 'idMovie': 21},
    {'dateTime': date.today(), 'price': 6.5,'theater':6, 'idMovie': 19},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 23},
    {'dateTime': date.today(), 'price': 10,'theater':2, 'idMovie': 24},
    {'dateTime': date.today(), 'price': 6.5,'theater':3, 'idMovie': 25},
    {'dateTime': date.today(), 'price': 6.5,'theater':4, 'idMovie': 12},
    {'dateTime': date.today(), 'price': 6.5,'theater':5, 'idMovie': 9},
    {'dateTime': date.today(), 'price': 6.5,'theater':6, 'idMovie': 8},
    ])
    
 #   conn.execute(booking.insert(),[
 #   { 'viewerName': 'A', 'viewerAge': '15', 'seatNumber': 1, 'clientUsername': 1 ,'idmovieShedule' : 1},
 #   { 'viewerName': 'B', 'viewerAge': '15', 'seatNumber': 2, 'clientUsername': 1 ,'idmovieShedule' : 1},
 #   { 'viewerName': 'C', 'viewerAge': '15', 'seatNumber': 3, 'clientUsername': 1 ,'idmovieShedule' : 1},
 #   { 'viewerName': 'D', 'viewerAge': '18', 'seatNumber': 4, 'clientUsername': 1 ,'idmovieShedule' : 1},
 #   { 'viewerName': 'E', 'viewerAge': '18', 'seatNumber': 5, 'clientUsername': 2 ,'idmovieShedule' : 1},
 #   { 'viewerName': 'F', 'viewerAge': '60', 'seatNumber': 6, 'clientUsername': 2 ,'idmovieShedule' : 1},
 #   { 'viewerName': 'G', 'viewerAge': '50', 'seatNumber': 7, 'clientUsername': 2 ,'idmovieShedule' : 1},
 #   { 'viewerName': 'H', 'viewerAge': '60', 'seatNumber': 8, 'clientUsername': 2 ,'idmovieShedule' : 2},
 #   { 'viewerName': 'I', 'viewerAge': '45', 'seatNumber': 9, 'clientUsername': 2 ,'idmovieShedule' : 2},
 #   { 'viewerName': 'L', 'viewerAge': '45', 'seatNumber': 10, 'clientUsername': 3 ,'idmovieShedule' : 2},
 #   { 'viewerName': 'M', 'viewerAge': '35', 'seatNumber': 11, 'clientUsername': 5 ,'idmovieShedule' : 2},
 #   { 'viewerName': 'N', 'viewerAge': '35', 'seatNumber': 12, 'clientUsername': 5 ,'idmovieShedule' : 3},
 #   { 'viewerName': 'O', 'viewerAge': '32', 'seatNumber': 13, 'clientUsername': 3 ,'idmovieShedule' : 3},
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
    
