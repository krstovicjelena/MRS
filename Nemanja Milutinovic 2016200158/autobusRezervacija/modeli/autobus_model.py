from PySide2 import QtCore
import os
import csv


class AutobusModel(QtCore.QAbstractTableModel):

    def __init__(self, path=""):
        super().__init__()
        # matrica, redovi su liste, a unutar tih listi se nalaze pojedinacni podaci o garazama firme
        self._data = []
        self.load_data(path)
        self.save_data(path)

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return 4 #fiksan br vracamo

    def data(self, index, role):
        element = self.get_element(index)
        if element is None:
            return None

        if role == QtCore.Qt.DisplayRole:
            return element

    def headerData(self, section, orientation, role):
        if orientation != QtCore.Qt.Vertical:
            if (section == 0) and (role == QtCore.Qt.DisplayRole):
                return "ID autobusa"
            elif (section == 1) and (role == QtCore.Qt.DisplayRole):
                return "Linija"
            elif (section == 2) and (role == QtCore.Qt.DisplayRole):
                return "Ukupan broj mesta"
            elif (section == 3) and (role == QtCore.Qt.DisplayRole):
                return "Broj slobodnih mesta"
           

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
    
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        

    def get_element(self, index : QtCore.QModelIndex):
        if index.isValid():
            element = self._data[index.row()][index.column()]
            if element:
                return element
        return None

    def remove(self, indices):
         # za na osnovu indeksa, dobijamo njihove redove, posto za jedan red je vezano pet indeksa (za kolone)
        # pravimo skup koji ce dati samo jedinstvene brojeve redova
        # uklanjanje vrsimo od nazad, jer ne zelimo da nam brojevi redova nakon uklanjanja odu van opsega.
        indices = sorted(set(map(lambda x: x.row(), indices)), reverse=True)
        for i in indices:
            self.beginRemoveRows(QtCore.QModelIndex(), i, i)
            del self._data[i]
            self.endRemoveRows()
    
    def add(self, data : dict):
        """
        Dodaje novog korisnika (red matrice) u model.
        Pomocna metoda nase klase.

        :param data: indeks elementa modela.
        :type data: dict -- podaci o novom korisniku.
        """
        self.beginInsertRows(QtCore.QModelIndex(), len(self._data), len(self._data))
        self._data.append([data["id"], data["linija"], data["ubr"], data["sbr"]])
        self.endInsertRows()
    def load_data(self, path=""):
        """
        Ucitava podatke iz CSV datoteke na zadatoj path putanji uz pomoc CSV reader-a.
        Pomocna metoda nase klase.

        :param path: putanja do CSV datoteke.
        :type path: str
        """
        with open(path, "r", encoding="utf-8") as fp:
            self._data = list(csv.reader(fp, dialect=csv.unix_dialect))

    def save_data(self, path=""):
        """
        Zapisuje podatke iz modela u datoteku na zadatoj path putanji uz pomoc CSV writer-a.
        Pomocna metoda nase klase.

        :param path: putanja do CSV datoteke.
        :type path: str
        """
        with open(path, "w", encoding="utf-8") as fp:
            writer = csv.writer(fp, dialect=csv.unix_dialect)
            for row in self._data:
                writer.writerow(row)

    def get_id_this_autobus(self, index):
        return self._data[index][0]
    def get_br_mesta_list(self, index):
        return {
            'ubr' : self._data[index][2]    ,
            'sbr' : self._data[index][3]
        }
    def change_sbr(self, index, newSbr):
        self._data[index][3] = newSbr

