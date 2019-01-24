from PySide2 import QtWidgets, QtCore, QtGui
from ...sqlite_init import povezivanje_baza

class DodajPlac(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        #tipovi placeva
        self._conn = povezivanje_baza()
        self._c = self._conn.cursor()
        self._c = self._conn.execute("SELECT tip, tip_placa_id FROM tip_placa" )
        self.placevi = list(self._c.fetchall())
        self._conn.commit()
        listaPlaceva = []
        for item in self.placevi:
            listaPlaceva.append(item[0])
        self.tip_placa_id  = "" #izabrana plac
      

        self.setWindowTitle("Dodaj vozilo na plac")

        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.naziv_placa = QtWidgets.QLineEdit(self)
        self.tip_placa = QtWidgets.QComboBox(self)
        self.br_mesta = QtWidgets.QLineEdit(self)

        self.tip_placa.addItems(listaPlaceva)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.form_layout.addRow("Naziv placa:", self.naziv_placa)
        self.form_layout.addRow("Tip placa:", self.tip_placa)
        self.form_layout.addRow("Ukupan broj mesta:", self.br_mesta)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)
    
    def provera_broja(self, input):
        try:
            num = int(input)
        except ValueError:
            return False
        return True

    def _on_accept(self):
        if self.naziv_placa.text() == "":
            QtWidgets.QMessageBox.warning(self,"Provera naziva placa", "Naziva placa mora biti popunjen!", QtWidgets.QMessageBox.Ok)
            return
        if self.br_mesta.text().lstrip("0").strip() == "":
            QtWidgets.QMessageBox.warning(self,"Provera ukupnog broja mesta", "Ukupan broj mesta mora biti popunjen!", QtWidgets.QMessageBox.Ok)
            return

        uneti_broj = self.br_mesta.text().lstrip("0").strip()
        if self.provera_broja(uneti_broj):
            uneti_broj = int(uneti_broj)
            duzina = len(str(uneti_broj))
            if uneti_broj <= 0:
                QtWidgets.QMessageBox.warning(self,"Ukupan broj mesta", "Broj mesta mora biti pozitivan broj!", QtWidgets.QMessageBox.Ok)
                return
        else:
            QtWidgets.QMessageBox.warning(self,"Ukupan broj mesta druga provera", "Morate uneti brojnu vrednost!", QtWidgets.QMessageBox.Ok)
            return

        izabranINDEX = self.tip_placa.currentIndex()
        self.tip_placa_id  = self.placevi[izabranINDEX][1]

        self.accept()
    def get_data(self):
        
        return {
            "naziv_placa": self.naziv_placa.text(),
            "tip_placa_id": self.tip_placa_id,
            "broj_mesta": self.br_mesta.text().lstrip("0").strip()
        }

   
