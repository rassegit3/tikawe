Planeettatietokanta

Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan tähtiä.
Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan planeettoja tähden ympärillä.
Käyttäjä näkee sovellukseen lisätyt tähdet ja planeetat.
Käyttäjä pystyy etsimään tähtiä ja planeettoja hakusanalla.
Sovelluksessa on käyttäjäsivut, jotka näyttävät käyttäjän lisäämät kohteet.
Käyttäjä pystyy valitsemaan kohteelle yhden tai useamman luokittelun.



Asennus:

Asenna flask-kirjasto:
$ pip install flask


Alusta tietokanta:
$ sqlite3 database.db < schema.sql

Käynnistä:
$ flask run
