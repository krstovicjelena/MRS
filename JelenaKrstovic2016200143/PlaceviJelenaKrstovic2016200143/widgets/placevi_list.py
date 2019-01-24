from PySide2 import QtWidgets
from PySide2 import QtGui
from ..modeli.placevi_model import PlaceviModel
from .dialogs.dodaj_plac import DodajPlac
from .dialogs.pregled_vozila_na_placu import PregledVozilaNaPlacu
from ..sqlite_init import povezivanje_baza



class PlaceviWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        self._conn = povezivanje_baza()
        self._c = self._conn.cursor()

        super().__init__(parent)
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.hbox_layout = QtWidgets.QHBoxLayout()
        self.hbox_layout2 = QtWidgets.QHBoxLayout()
        self.dodaj_plac = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/plus.png"), "Dodaj plac", self)
        self.ukloni_plac = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/minus.png"), "Ukloni plac", self)
        self.pregled_vozila = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/box.png"), "Pregled vozila na placu", self)
        self.osvezi_prikaz = QtWidgets.QPushButton(QtGui.QIcon("resources/icons/arrow-circle-225-left.png"), "Refresh", self)

        self.hbox_layout2.addWidget(self.dodaj_plac)
        self.hbox_layout2.addWidget(self.ukloni_plac)
        self.hbox_layout2.addWidget(self.pregled_vozila)
        self.hbox_layout2.addWidget(self.osvezi_prikaz)

        self.table_view = QtWidgets.QTableView(self)

        self._prikaz_placeva()
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)

        self.dodaj_plac.clicked.connect(self._on_dodaj_plac)
        self.ukloni_plac.clicked.connect(self._on_ukloni_plac)
        self.osvezi_prikaz.clicked.connect(self._prikaz_placeva)
        self.pregled_vozila.clicked.connect(self._on_pregled_vozila)

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

    def _prikaz_placeva(self):
        self.set_model(PlaceviModel())
        return

    def _on_dodaj_plac(self):
        dialog = DodajPlac(self.parent())
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            tmpL = dialog.get_data()

            upit = self._c.execute("INSERT INTO placevi (naziv_placa, tip_placa_id, broj_mesta, broj_zauzetih) VALUES (:naziv , :id, :brMesta , 0)" ,{'naziv' : tmpL['naziv_placa'], 'id' : tmpL['tip_placa_id'], 'brMesta' : tmpL['broj_mesta']} )
            lastID = self._c.lastrowid # zadnji uneti id
            uneti_podaci = dialog.get_data()
            uneti_podaci['plac_id'] = lastID
            uneti_podaci['broj_zauzetih'] = 0
            self._conn.commit()
            self.table_view.model().dodaj(uneti_podaci)
    

    def _on_ukloni_plac(self):
        self.table_view.model().ukloni(self.table_view.selectedIndexes())

   

    def _on_pregled_vozila(self):
        rows = sorted(set(index.row() for index in
                      self.table_view.selectedIndexes())) #dobijamo redni br reda koji je izabrao korisnik
        if len(rows) == 0:
            return
        plac_id = self.table_view.model().get_id_placa(rows[0])
        plac_tip = self.table_view.model().get_tip_placa(rows[0])
        br_mesta = self.table_view.model().get_brojevi_mesta(rows[0])

        dialog = PregledVozilaNaPlacu(self.parent(), plac_id ,br_mesta , plac_tip )

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            brZ_updated = dialog.get_data()
            self.table_view.model().update_brZ(brZ_updated["brZ"], plac_id)
            
        self._prikaz_placeva()
