# Pylint-raportti

Pylint antaa seuraavan raportin sovelluksesta:
```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:19:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:28:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:34:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:38:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:47:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:58:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:67:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:86:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:95:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:104:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:118:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:122:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:141:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:156:8: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
app.py:141:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:164:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:173:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:178:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:207:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:228:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module items
items.py:1:0: C0114: Missing module docstring (missing-module-docstring)
items.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:7:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:12:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:16:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:22:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:41:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:45:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:51:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:56:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:65:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:69:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:79:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:84:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:88:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:98:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:102:0: C0116: Missing function or method docstring (missing-function-docstring)
items.py:107:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)

------------------------------------------------------------------
Your code has been rated at 8.03/10 (previous run: 0.00/10, +8.03)


```


## Docstring-ilmoitukset

Pylint ilmoittaa paljon  puuttuvista dockstringeistä mutta on päätetty ettei dockstringejä tarvita

## Tarpeeton else

Pylint ilmoittaa muutamasta turhasta elsestä returnien jälkeen mutta nähdään niiden parantavan koodin luettavuutta, joten on päätetty pitää ne

## Puuttuva palautusarvo

Pylint ilmoittaa puuttuvista palautearvoista mutta ilmoitukset liittyät pariin  funktioon jotka käsittelevät metodeja  ``` GET ``` ja ``` POST ```.
Vaikka teknisesti olisi mahdollista että funktiot voisivat saada jonkin muun metodin kuin ``` GET ``` tai ``` POST ```, niin ei kuitenkaan ole mahdollista käytännössä sillä funktion dekoraattori estää sen tapahtumasta.



## Vaarallinen oletusarvo

Pylint ilmoittaa vaarallisesta oletusarvosta parissa funktiossa.
esim:
```db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)```

viittaa funktioon:
``` def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
```
mutta se ei aiheuta vaaraa sillä vaikka lista jaetaan muiden samanlaisten funktioiden kanssa, mikään niistä ei muokkaa sitä joten ongelmaa ei synny.

## Muuttujan nimi
Pylint ilmoittaa muuttujan vääränlaisesta muuttujan nimestä:
```config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)```

Muuttujan nimeä ei ole vaihdettu syystä että se ei ole ohjelman logiikkaa vaan konfiguraatio arvo.





