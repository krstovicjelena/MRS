from PySide2 import QtCore
import os
import sqlite3
from ..sqlite_init import povezivanje_baza


class PlaceviModel(QtCore.QAbstractTableModel):

    def __init__(self):
        super().__init__()
        # matrica, redovi su liste, a unutar tih listi se nalaze pojedinacni podaci o korisniku iz imenika
        self._conn = povezivanje_baza()
        self._c = self._conn.cursor()
        self._data = []
        self.ucitaj_podatke_iz_baze()

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 5 #fiksan br vracamo

    def data(self, index, role):
        element = self.get_element(index)
        if element is None:
            return None

        if role == QtCore.Qt.DisplayRole:
            return element

    def headerData(self, section, orientation, role):
        if orientation != QtCore.Qt.Vertical:
            if (section == 0) and (role == QtCore.Qt.DisplayRole):
                return "ID placa"
            elif (section == 1) and (role == QtCore.Qt.DisplayRole):
                return "Naziv placa"
            elif (section == 2) and (role == QtCore.Qt.DisplayRole):
                return "Tip placa"
            elif (section == 3) and (role == QtCore.Qt.DisplayRole):
                return "Ukupan broj mesta"
            elif (section == 4) and (role == QtCore.Qt.DisplayRole):
                return "Broj zauzetih mesta"

    def setData(self, index, value, role):
        try:
            if value == "":
                return False
            self._data[index.row()][index.column()] = value
            self.dataChanged()
            return True
        except:
            return False

    def flags(self, index):
        # ne damo da menja datum rodjenja (primera radi)
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        # sve ostale podatke korisnik moze da menja

    def get_element(self, index : QtCore.QModelIndex):
        if index.isValid():
            element = self._data[index.row()][index.column()]
            if element:
                return element
        return None

    def ucitaj_podatke_iz_baze(self):
        upit = self._conn.execute(""" SELECT plac_id, naziv_placa, tip, broj_mesta, broj_zauzetih FROM placevi INNER JOIN tip_placa ON placevi.tip_placa_id = tip_placa.tip_placa_id;""")
        self._data = list(upit.fetchall())
        self._conn.commit()

    
    def get_brojevi_mesta(self, index):
        return { 
                "brZ"      :    self._data[index][4],
                "ukupno"   :    self._data[index][3]
                }
    
    def get_id_placa(self, index):
        return self._data[index][0]
    
    def get_tip_placa(self, index):
        return self._data[index][2]
    
    def dodaj(self, data : dict):
        self.beginInsertRows(QtCore.QModelIndex(), len(self._data), len(self._data))
        
        upit = self._conn.execute(""" SELECT tip FROM tip_placa where tip_placa_id=:idHere;""", {'idHere':data['tip_placa_id'] })
        upitTipPlaca = list(upit.fetchall())
        self._conn.commit()
        ######
        self._data.append([data['plac_id'], data['naziv_placa'], upitTipPlaca[0][0], data['broj_mesta'], data['broj_zauzetih']])
        self.endInsertRows()


    def ukloni(self, indices):
        # za na osnovu indeksa, dobijamo njihove redove, posto za jedan red je vezano pet indeksa (za kolone)
        # pravimo skup koji ce dati samo jedinstvene brojeve redova
        # uklanjanje vrsimo od nazad, jer ne zelimo da nam brojevi redova nakon uklanjanja odu van opsega.
        indices = sorted(set(map(lambda x: x.row(), indices)), reverse=True)
        for i in indices:
           
            id = self.get_id_placa(i)
            upit = self._conn.execute("""DELETE FROM placevi WHERE plac_id = :ID""" , {'ID' : id} )
            self._conn.commit()
            upit = self._conn.execute("""DELETE FROM vozila_plac WHERE plac_id = :ID""" , {'ID' : id} )
            self._conn.commit()
            
            self.beginRemoveRows(QtCore.QModelIndex(), i, i)
            del self._data[i]
            self.endRemoveRows()

    def update_brZ(self, brZ_updated=None, plac_id=None):
        upit = self._conn.execute("""UPDATE placevi SET broj_zauzetih = :brZ WHERE plac_id = :pID;""" , {'brZ' : int(brZ_updated) , 'pID':plac_id } )
        self._conn.commit()
        return

   

    
