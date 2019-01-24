from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtGui import QIcon
from PySide2.QtCore import Qt
from ...modeli.vozila_na_placu_model import VozilaNaPlacuModel
from .dodaj_vozilo_na_plac import DodajVoziloNaPlac
from ...sqlite_init import povezivanje_baza

class PregledVozilaNaPlacu(QtWidgets.QDialog):

    def __init__(self, parent=None, plac_id=None, br_mesta_na_placu=None , plac_tip=None):
        super().__init__(parent)
        self.this_plac_id= plac_id
        self.plac_tip = plac_tip

        self._conn = povezivanje_baza()
        self._c = self._conn.cursor()
        result = self._conn.execute("SELECT naziv_placa FROM placevi WHERE plac_id =:id" ,{'id' : self.this_plac_id} )
        self.plac_naziv = list(result.fetchall())
        self.plac_naziv = self.plac_naziv[0]
        self._conn.commit()

        self.brZauzetih = br_mesta_na_placu["brZ"]
        self.brUkupno = br_mesta_na_placu["ukupno"]



        self.setWindowTitle("Pregled vozila na placu:  " + self.plac_naziv[0] )
        self.resize(800, 600)

        self.vozila_opcije = QtWidgets.QHBoxLayout()

        self.dodaj_vozilo = QtWidgets.QPushButton(QIcon("resources/icons/plus.png"), "Dodaj vozilo")
        self.ukloni_vozilo = QtWidgets.QPushButton(QIcon("resources/icons/minus.png"), "Ukloni vozilo")
        self.vozila_layout = QtWidgets.QVBoxLayout()

        self.table_view = QtWidgets.QTableView(self)
        self._prikaz_vozila_na_placu()
        self.table_view.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.vozila_opcije.addWidget(self.dodaj_vozilo)
        self.vozila_opcije.addWidget(self.ukloni_vozilo)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.on_accept)

        self.vozila_layout.addLayout(self.vozila_opcije)
        self.vozila_layout.addWidget(self.table_view)
        self.vozila_layout.addWidget(self.button_box)

        self.dodaj_vozilo.clicked.connect(self._on_dodaj_vozilo_dialog)
        self.ukloni_vozilo.clicked.connect(self._on_ukloni_vozilo)

        self.setLayout(self.vozila_layout)

    def on_accept(self):

        return self.accept()

    def _prikaz_vozila_na_placu(self):
        self.set_model(VozilaNaPlacuModel(self.this_plac_id))
        return

    def set_model(self, model):

        self.table_view.setModel(model)
        self.table_view.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def _on_dodaj_vozilo_dialog(self):
        dialog = DodajVoziloNaPlac(self.parent() , self.plac_naziv[0], self.this_plac_id ,self.brZauzetih, self.brUkupno, self.plac_tip )
        # znaci da je neko odabrao potvrdni odgovor na dijalog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
           
            lista = dialog.get_data()                                                                 
            self._c.execute("INSERT INTO vozila (marka, model, registracija, tip) VALUES (:tmp1, :tmp2, :tmp3, :tmp4)" ,{'tmp1' : lista['marka'], 'tmp2' : lista['model'] , 'tmp3' : lista['registracija'], 'tmp4' : lista['tip']})
            self._conn.commit()

            lista['vozilo_id'] = self._c.lastrowid
            
            self._c.execute("INSERT INTO vozila_plac (vozilo_id, plac_id) VALUES (:pID , :rhID)" ,{'pID' : lista['vozilo_id'], 'rhID' : lista['plac_id']} )
            self._conn.commit()
            
            self.brZauzetih = lista["brZ"]
            self._prikaz_vozila_na_placu()

    def _on_ukloni_vozilo(self):
        rows = sorted(set(index.row() for index in
                      self.table_view.selectedIndexes())) #dobijamo redni br reda koji je izabrao korisnik
        if len(rows) == 0:
            return
        vid = self.table_view.model().get_id_vozila(rows[0])
    
        upit = self._conn.execute("SELECT broj_zauzetih FROM placevi WHERE plac_id =:id" ,{'id' : self.this_plac_id} )
        brZazuzetihMesta = list(upit.fetchall())
        brZazuzetihMesta = brZazuzetihMesta[0][0]
        self._conn.commit()
        self._c = self._conn.execute("DELETE FROM vozila_plac WHERE vozilo_id =:vid AND plac_id =:id" ,{'vid' : vid, 'id' : self.this_plac_id})
        self._conn.commit()

        nov_br_zauzetih_mesta = brZazuzetihMesta - 1
        self._conn.execute("UPDATE placevi SET broj_zauzetih = :brZ WHERE plac_id = :id" ,{'brZ' : nov_br_zauzetih_mesta, 'id' : self.this_plac_id})
        self._conn.commit()

        self._prikaz_vozila_na_placu()
        self.brZauzetih -= 1
        return


    def get_data(self):
        return {
            "brZ" : self.brZauzetih
        }