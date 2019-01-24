from PySide2 import QtCore
import os
import sqlite3
from ..sqlite_init import povezivanje_baza


class VozilaNaPlacuModel(QtCore.QAbstractTableModel):

    def __init__(self, plac_id):
        super().__init__()
        self.this_plac_id = plac_id
        # matrica, redovi su liste, a unutar tih listi se nalaze pojedinacni podaci 
        self._conn = povezivanje_baza()
        self._c = self._conn.cursor()
        self._data = []
        self.ucitaj_podatke_iz_baze()

    def rowCount(self, index):

        return len(self._data)

    def columnCount(self, index):
        return 5 #fiksan broj vracamo

    def data(self, index, role):

        element = self.get_element(index)
        if element is None:
            return None

        if role == QtCore.Qt.DisplayRole:
            return element

    def headerData(self, section, orientation, role):

        if orientation != QtCore.Qt.Vertical:
            if (section == 0) and (role == QtCore.Qt.DisplayRole):
                return "ID vozila"
            elif (section == 1) and (role == QtCore.Qt.DisplayRole):
                return "Marka"
            elif (section == 2) and (role == QtCore.Qt.DisplayRole):
                return "Model"
            elif (section == 3) and (role == QtCore.Qt.DisplayRole):
                return "Registracioni broj"
            elif (section == 4) and (role == QtCore.Qt.DisplayRole):
                return " Tip"

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
#moze da menja samo reg oznaku
       
        if index.column() != 3: 
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        else: 
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable


    def get_element(self, index : QtCore.QModelIndex):

        if index.isValid():
            element = self._data[index.row()][index.column()]
            if element:
                return element
        return None

    def ucitaj_podatke_iz_baze(self):
        upit = self._conn.execute("""
        SELECT vozila_plac_id , marka , model , registracija, vozila.tip, vozila_plac.vozilo_id
        FROM vozila_plac INNER JOIN vozila ON
        vozila_plac.vozilo_id = vozila.vozilo_id
        WHERE plac_id = :plac_id""" ,{'plac_id' : self.this_plac_id})
        self._data = list(upit.fetchall())
        self._conn.commit()
        self._conn.close()

    
    def get_id_vozila(self, index):
        return self._data[index][5]
    def get_model(self, index):
        return self._data[index][1]
    
    def dodaj(self, data : dict):

        self.beginInsertRows(QtCore.QModelIndex(), len(self._data), len(self._data))
        self._data.append([data["vozilo_id"], data["marka"], data["model"],data["registracija"],data["tip"]])
        self.endInsertRows()
   
    def ukloni(self, indices):

        # za na osnovu indeksa, dobijamo njihove redove, posto za jedan red je vezano pet indeksa (za kolone)
        # pravimo skup koji ce dati samo jedinstvene brojeve redova
        # uklanjanje vrsimo od nazad, jer ne zelimo da nam brojevi redova nakon uklanjanja odu van opsega.
        indices = sorted(set(map(lambda x: x.row(), indices)), reverse=True)
        for i in indices:
            self.beginRemoveRows(QtCore.QModelIndex(), i, i)
            del self._data[i]
            self.endRemoveRows()

   

    
