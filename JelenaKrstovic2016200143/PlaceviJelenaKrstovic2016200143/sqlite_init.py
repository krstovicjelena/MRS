import sqlite3
def povezivanje_baza():
    return sqlite3.connect('plugins/PlaceviJelenaKrstovic2016200143/plac.db')
