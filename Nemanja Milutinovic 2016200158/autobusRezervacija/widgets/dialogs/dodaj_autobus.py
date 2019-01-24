from PySide2 import QtWidgets, QtCore, QtGui

class DodajAutobusDialog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Dodaj garazu")

        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.id_autobusa = QtWidgets.QLineEdit(self)
        self.linija = QtWidgets.QComboBox(self)
        self.br_mesta = QtWidgets.QLineEdit(self)
        tmpList = ["Beograd-Novi Sad","Beograd-Nis","Beograd-Subotica"]
        #stavljamo vrednosti u tip hale dropdown
        self.linija.addItems(tmpList)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.form_layout.addRow("IDautobusa:", self.id_autobusa)
        self.form_layout.addRow("Linija:", self.linija)
        self.form_layout.addRow("Ukupan broj mesta:", self.br_mesta)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

    def _on_accept(self):
        if self.id_autobusa.text() == "":
            QtWidgets.QMessageBox.warning(self,
            "Provera Sifre", "Sifra mora biti popunjena!", QtWidgets.QMessageBox.Ok)
            return
        if self.br_mesta.text().lstrip("0").strip() == "":
            QtWidgets.QMessageBox.warning(self,
            "Provera ukupnog br mesta", "Ukupan broj mesta ne sme biti prazan!", QtWidgets.QMessageBox.Ok)
            return

        temp_input = self.br_mesta.text().lstrip("0").strip()
        if self.provera_vrednosti(temp_input):
            temp_input = int(temp_input)
            lenInt = len(str(temp_input))
            if temp_input <= 0:
                QtWidgets.QMessageBox.warning(self,
                "Ukupan Broj Mesta", "Broj Mesta mora biti veci od nule!", QtWidgets.QMessageBox.Ok)
                return
        else:
            QtWidgets.QMessageBox.warning(self,
            "Ukupan Broj Mesta2", "Morate uneti brojčanu vrednost!", QtWidgets.QMessageBox.Ok)
            return


        self.accept()
    def get_data(self):
        return {
            "id": self.id_autobusa.text(),
            "linija": self.linija.currentText(),
            "ubr": self.br_mesta.text().lstrip("0").strip(),
            "sbr": self.br_mesta.text().lstrip("0").strip()
        }

    def provera_vrednosti(self, input):
        try:
            num = int(input)
        except ValueError:
            return False
        return True
