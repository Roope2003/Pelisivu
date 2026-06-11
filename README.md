# Pelisivu
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy julkaisemaan, muokkaamaan ja poistamaan pelin.
- Käyttäjä pystyy lisäämään kuvia pelille.
- Käyttäjä näkee sovellukseen lisätyt pelit.
- Käyttäjä pystyy etsimään pelejä hakusanalla.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja, käyttäjän lisäämät pelit ja mahdolliset arvioinnit muille peleille.
- Käyttäjä pystyy valitsemaan pelille yhden tai useamman genren.
- Käyttäjä pystyy antamaan arviointeja muille peleille.

---

# Asennusohjeet

1. Terminaalissa navigoi siihen kansioon mihin haluat asentaa sovelluksen ja asenna se komennolla:
  `git clone https://github.com/Roope2003/Pelisivu.git`

2.  Käynnistä virtuaaliympäristö komennoilla:
   `python3 -m venv venv` jonka jälkeen `source venv/bin/activate`

3.  Asenna flask komennolla:
   `pip install flask`
4. Kloonaa tietokanta komennolla:
  `sqlite3 database.db < schema.sql`

5. Käynnistä sovellus komenolla:
  `flask run`


---

# Testaus suurella tietomäärällä

`seed.py`-tiedosto sisäältää koodi, joka luo monta käyttäjää, postausta ja arviota. Jokaiselle postaukselle valitaan satunnainen postaaja, jonka jälkeen satunnaisiin postauksiin asetellaan satunnainen määrä arvioita.

Testaillessani huomasin käyttäjäsivujen olevan hitain osa sovellusta. Todennäköisesti koska niissä ei ollut vielä käytössä sivutusta kuten etusivulla. Tämä kuitenkin antoi hyvän mahdollisuuden testata indeksoinnin vaikutusta.

Ennen indeksointia, käyttäjäsivujen lataamisessa meni noin 0,3s, joka oli jo aika jonka ihminen huomaa mutta indeksoinnin jälkeen aika vaikutti laskevan 0,003s mikä on huomattavan suuri muutos.