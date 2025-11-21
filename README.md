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
