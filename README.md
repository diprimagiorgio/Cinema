# Cinema il molo

Questa applicazione serve a gestire le prenotazioni, lo storico ed il database di un cinema. Offre inoltre la possibilità di vedere delle statistiche sulle prenotazini

## Per cominciare
Quest istruzioni permettono l'istallazione del progetto in locale con l'obbiettivo di testarne il funzionamento

### Prerequisiti
hai bisogno di installare postgres e  per installarlo è sufficiente

```
Non lo so
```
hai bisogno di avere un ambiente Python funzionante

```
Non so nemmeno questo
```

poi magari anche altro

```
Che non so
```

### Installazione
Queste sono le istruzioni step by step utili per l'istallazione, prima di avviarel'applicazione

Entra nel  terminale

Entra con l'utente superUser, di default è postgres, se è stato cambiato usare il superUser

```console
user@user:~$ sudo -i -u postgres
```
Una volta entrati

Entra dentro il programma psql

```console
postgres@user:~$ psql
```

Crea un utente che sarà l'amministratore del database, e il proprietario. Assicurati di non avere già un utente con il nome admin_ilmolo

```console
postgres=# CREATE USER admin_ilmolo WITH PASSWORD ‘secret’ CREATEDB CREATEROLE; 
```
Apri un altro terminale. Quindi crea il database cinemaIlMolo

```console
user@user:~$  createdb -h localhost -U admin_ilmolo -W "cinemaIlMolo" 
```

Se sei arrivato fin qui, hai installato con successo tutto il necessario. Adesso è necessario avviare il programma. Proseguire con le istruzioni del paragrafo primo avvio

## Eseguire primo avvio
 
Avviare l'enviroment
```console
user@user:~$ source "<percorso>/Cinema/venv/bin/activate" 
```
Aprire la cartella app all'interno del progetto, e selezionare il file d'avvio, qundi avviare l'app
```console
user@user:~/<percorso>/Cinema/app$ export FLASK_APP=__init__.py; flask run 
```
Aprire nel nel browser,  il funzionamento è garantito solo con chrome,  http://127.0.0.1:5000/init .
Verranno quindi eseguite tutte le operazioni necessarie per il primo avvio. 
## Per avvi successivi

Per gli avvi successivi è necessario rieseguire i primi due punti del paragafro primo avvio, quindi visitare  http://127.0.0.1:5000/



## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Il web framework usato
* [SQLAlchemy](https://www.sqlalchemy.org/) - Libreria per interfacciarsi al database
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/) - Libreria per autenticazione


## Versionamento

Abbiamo utilizzato [GitKraken](www.gitkraken.com) per il versionamento. Per vedere tutte le versioni vedere  [tags on this repository](https://github.com/your/project/tags) (disponibile solo dopo la discussuione per motivi legati al regolamento). 

## Autori


* **Luca Bizzotto** - *Area Cliente e Statistiche[mamager]* 
* **Giorgio Diprima** - *Area Manager, pagamento[clienet] e README* 
* **Giosuè Zannini** - *Area prenotazioni[cliente] e riepilogo prenotazioni[manager]* 
