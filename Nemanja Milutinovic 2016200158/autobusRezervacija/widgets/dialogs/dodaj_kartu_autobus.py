from PySide2 import QtWidgets, QtCore, QtGui
import csv

class DodajKartuUAutobusDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, brM=None):

        super().__init__(parent)

        self.brM = brM  

        self.setWindowTitle("Dodaj rezervaciju")
        self.resize(250, 180)
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.ime = QtWidgets.QLineEdit(self)

        self.broj_combobox = QtWidgets.QComboBox(self)

        
        self.broj_karata=['1','2','3','4','5']
        self.broj_combobox.addItems(self.broj_karata)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        
        self.form_layout.addRow("Ime i prezime:", self.ime)
        self.form_layout.addRow("Broja karata:", self.broj_combobox)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    

    def _on_accept(self):
        if self.ime.text() == "": #provera da li je prazno ime
            QtWidgets.QMessageBox.warning(self,
            "Ime provera", "Ime mora biti popunjeno!", QtWidgets.QMessageBox.Ok)
            return
        izabran_br_karata = int(self.broj_combobox.currentText())
        ubr = int(self.brM["ubr"])
        sbr = int(self.brM["sbr"])
        nov_br_slobodnoh =  sbr - izabran_br_karata
        if nov_br_slobodnoh < 0: #znaci da nema dovoljno mesta
            QtWidgets.QMessageBox.warning(self,
            "Broj karata", "Autobus nema dovoljno mesta za izabran broj karata!", QtWidgets.QMessageBox.Ok)
            return
        #ako je sve ok, nema greske
        self.brM["sbr"] = nov_br_slobodnoh
        self.accept()

    def get_data(self):

        return {
            "ime":self.ime.text(),
            "broj": self.broj_combobox.currentText(),
            "nov_br_slobodnih" : self.brM["sbr"]
        }