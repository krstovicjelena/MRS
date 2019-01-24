from PySide2 import QtWidgets
from PySide2 import QtGui
from ..modeli.autobus_model import AutobusModel
from .dialogs.dodaj_autobus import DodajAutobusDialog
from .dialogs.pregled_karata_za_autobus import PregledKarataZaAutobusDialog
import os

class AutobusWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
    
        super().__init__(parent)
        self.file_path = None
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.hbox_layout2 = QtWidgets.QHBoxLayout()
        self.dodaj_autobus = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/plus.png"), "Dodaj autobus", self)
        self.ukloni_autobus = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/minus.png"), "Ukloni autobus", self)
        self.pregled_rezervacija = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/box.png"), "Pregled rezervacija", self)
        self.ucitaj = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/folder-open.png"), "Ucitaj listu autobusa", self)        

        self.hbox_layout2.addWidget(self.dodaj_autobus)
        self.hbox_layout2.addWidget(self.ukloni_autobus)
        self.hbox_layout2.addWidget(self.pregled_rezervacija)
        self.hbox_layout2.addWidget(self.ucitaj)

        self.table_view = QtWidgets.QTableView(self)
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.dodaj_autobus.clicked.connect(self._on_dodaj_autobus)
        self.ukloni_autobus.clicked.connect(self._on_ukloni_autobus)
        self.ucitaj.clicked.connect(self._on_open)
        
        self.pregled_rezervacija.clicked.connect(self._on_pregled_rezervacija)

        self.vbox_layout.addLayout(self.hbox_layout)
        self.vbox_layout.addLayout(self.hbox_layout2)
        self.vbox_layout.addWidget(self.table_view)

        self.setLayout(self.vbox_layout)

        self.actions_dict = {
            "add": QtWidgets.QAction(QtGui.QIcon("resources/icons/plus.png"), "Dodaj", self)
        }


    def set_model(self, model):
        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

    def _on_dodaj_autobus(self):
        """
        Metoda koja se poziva na klik dugmeta add.
        Otvara dijalog sa formom za kreiranje novog korisnika u imeniku.
        """
        dialog = DodajAutobusDialog(self.parent())
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.table_view.model().add(dialog.get_data())

    def _on_ukloni_autobus(self):
        self.table_view.model().remove(self.table_view.selectedIndexes())


    def _on_open(self):
        """
        Metoda koja se poziva na klik dugmeta open.
        """
        self.file_path = QtWidgets.QFileDialog.getOpenFileName(self, "Open contacts file", ".", "CSV Files (*.csv)")
        self.set_model(AutobusModel(self.file_path[0]))

    def _on_save(self):
      
        self.table_view.model().save_data(self.file_path[0])

    def _on_pregled_rezervacija(self):
        rows = sorted(set(index.row() for index in
                      self.table_view.selectedIndexes())) #dobijamo redni br reda koji je izabrao korisnik
        if len(rows) == 0:
            return
        selected_autobusID = self.table_view.model().get_id_this_autobus(rows[0])
        selected_autobus_br_mesta = self.table_view.model().get_br_mesta_list(rows[0])
        temp_string="plugins/autobusRezervacija/rezervacije/" #putanja gde se nalaze rezervacije

        dialog = PregledKarataZaAutobusDialog(self.parent(), temp_string+selected_autobusID+".csv" ,selected_autobus_br_mesta )

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            r_dict = dialog.get_data()
            if r_dict['novBrSlobodnihMesta'] != None: #nema izmena karata
                self.table_view.model().change_sbr(rows[0], r_dict['novBrSlobodnihMesta'])
                self._on_save()
