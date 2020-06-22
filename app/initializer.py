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
        { 'title':'uno','minimumAge': 13,'duration': 120., 'idGenre': 1},
        { 'title':'due','minimumAge': 13,'duration': 120., 'idGenre': 1},
        { 'title':'tre','minimumAge': 13,'duration': 120., 'idGenre': 1},
        { 'title':'quattro','minimumAge': 12,'duration': 60., 'idGenre': 1},
        { 'title':'cinque','minimumAge': 12,'duration': 60., 'idGenre': 7},
        { 'title':'sei','minimumAge': 12,'duration': 180., 'idGenre': 7},
        { 'title':'sette','minimumAge': 12,'duration': 180., 'idGenre': 7},
        { 'title':'otto','minimumAge': 12,'duration': 180., 'idGenre': 7},
        { 'title':'nove','minimumAge': 18,'duration': 160., 'idGenre': 1},
        { 'title':'dieci','minimumAge': 18,'duration': 240., 'idGenre': 7},
        { 'title':'undici','minimumAge': 18,'duration': 90., 'idGenre': 7},
        { 'title':'dodici','minimumAge': 18,'duration': 90., 'idGenre': 1},
        { 'title':'tredici','minimumAge': 18,'duration': 90., 'idGenre': 7},
        { 'title':'quattordici','minimumAge': 12,'duration': 90., 'idGenre': 13},
        { 'title':'quindici','minimumAge': 12,'duration': 120., 'idGenre': 13},
        { 'title':'sedici','minimumAge': 12,'duration': 120., 'idGenre': 13},
        { 'title':'diciasette','minimumAge': 12,'duration': 120., 'idGenre': 7},
        { 'title':'diciotto','minimumAge': 12,'duration': 150., 'idGenre': 13},
        { 'title':'diciannove','minimumAge': 12,'duration': 150., 'idGenre':13},
        { 'title':'venti','minimumAge': 12,'duration': 120., 'idGenre': 13}
    ])
    
    
    
    conn.execute(theaters.insert(),[
    {'seatsCapacity': 100},
    {'seatsCapacity': 100},
    {'seatsCapacity': 50},
    ])
    
    conn.execute(movieSchedule.insert(),[
    {'dateTime': date.today(), 'price': 6.5,'theater':1, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 5,'theater':1, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 5,'theater':1, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 5,'theater':1, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 6.5,'theater':1, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 6.5,'theater':1, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 6.5,'theater':1, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 6.5,'theater':1, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 6.5,'theater':1, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 3},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 10,'theater':1, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 6.5,'theater':1, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 6.5,'theater':1, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 6.5,'theater':1, 'idMovie': 2},
    {'dateTime': date.today(), 'price': 6.5,'theater':2, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 6.5,'theater':2, 'idMovie': 1},
    {'dateTime': date.today(), 'price': 6.5,'theater':2, 'idMovie': 1},
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
    
