from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from ...modeli.karte_autobus_model import KarteAutobusModel
from .dodaj_kartu_autobus import DodajKartuUAutobusDialog


class PregledKarataZaAutobusDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, putanja_csv=None, br_mesta=None):
        super().__init__(parent)
        self.this_putanja_csv = putanja_csv
        self.nBrS=None #nov broj slobodnih mesta
        self.this_brM = br_mesta #broj slobodnih i ukupan broj mesta

        self.setWindowTitle("Pregled Rezervacija : "+ self.this_putanja_csv.strip("plugins/garaze/rezervacije/").strip(".csv") )
        self.resize(700, 550)

        self.karte_options_layout = QtWidgets.QHBoxLayout()

        self.dodaj_kartu = QtWidgets.QPushButton(QIcon("resources/icons/plus.png"), "Dodaj Kartu")
        self.ukloni_kartu = QtWidgets.QPushButton(QIcon("resources/icons/minus.png"), "Ukloni Karte")
        self.plugin_karte_layout = QtWidgets.QVBoxLayout()

        self.table_view = QtWidgets.QTableView(self)
        self.prikaz_karata()
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.karte_options_layout.addWidget(self.dodaj_kartu)
        self.karte_options_layout.addWidget(self.ukloni_kartu)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.on_accept)

        self.plugin_karte_layout.addLayout(self.karte_options_layout)
        self.plugin_karte_layout.addWidget(self.table_view)
        self.plugin_karte_layout.addWidget(self.button_box)

        self.dodaj_kartu.clicked.connect(self._on_dodaj_kartu_dialog)
        self.ukloni_kartu.clicked.connect(self._on_ukloni_kartu)

        self.setLayout(self.plugin_karte_layout)

    def on_accept(self):
        self.table_view.model().save_data(self.this_putanja_csv)
        return self.accept()

    def prikaz_karata(self):

        self.set_model(KarteAutobusModel(self.this_putanja_csv))
        return
       

    def set_model(self, model):

        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def _on_dodaj_kartu_dialog(self):
        dialog = DodajKartuUAutobusDialog(self.parent() , self.this_brM )
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            return_dict = dialog.get_data()
            self.table_view.model().add(return_dict)
            self.nBrS = return_dict['nov_br_slobodnih']

    def _on_ukloni_kartu(self):
        rows = sorted(set(index.row() for index in
                      self.table_view.selectedIndexes())) #dobijamo redni br reda koji je izabrao korisnik
        if len(rows) == 0:
            return

        kolicina_karata = self.table_view.model().get_kolicina_karte(rows[0])
        nova_kolicina = int(self.this_brM["sbr"]) + int(kolicina_karata)
        self.this_brM["sbr"] = nova_kolicina
        self.nBrS = nova_kolicina
        self.table_view.model().remove(self.table_view.selectedIndexes())
        return

    def get_data(self):
        return {
            "novBrSlobodnihMesta" : self.nBrS
        }
