from PySide2 import QtWidgets, QtCore, QtGui
from ...sqlite_init import povezivanje_baza

class DodajVoziloNaPlac(QtWidgets.QDialog):

    def __init__(self, parent=None , naziv_placa=None , plac_id=None , brZ=None ,brU=None, p_tip=None):

        super().__init__(parent)
        self.this_naziv_placa = naziv_placa
        self.this_plac_id = plac_id
        self.brZauzetih = brZ
        self.brUkupno = brU
        self.plac_tip = p_tip

        if self.plac_tip == "kamion":
            self.plac_tip = "teretno"

    

        #placevi GET
        self._conn = povezivanje_baza()
        self._c = self._conn.cursor()

        self.vozilaf = self.listanje_baze("SELECT DISTINCT tip  FROM vozila")
        self.vozila = self.fetch_u_listu(self.vozilaf)
        

        self.setWindowTitle("Dodaj vozilo na plac")
        self.resize(300, 200)
        self.vbox_layout = QtWidgets.QVBoxLayout()
        self.form_layout = QtWidgets.QFormLayout()
        self.plac = QtWidgets.QLabel(self)
        self.marka = QtWidgets.QLineEdit(self)
        self.model = QtWidgets.QLineEdit(self)
        self.registracija = QtWidgets.QLineEdit(self)
        self.tip = QtWidgets.QComboBox(self)
        
        self.tip.addItems(self.vozila)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
            | QtWidgets.QDialogButtonBox.Cancel, parent=self)

        self.plac.setText(self.this_naziv_placa)
        self.form_layout.addRow("Plac:", self.plac)
        self.form_layout.addRow("Marka:", self.marka)
        self.form_layout.addRow("Model:", self.model)
        self.form_layout.addRow("Registracija:", self.registracija)
        self.form_layout.addRow("Tip:", self.tip)

        self.vbox_layout.addLayout(self.form_layout)
        self.vbox_layout.addWidget(self.button_box)

        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)

        self.setLayout(self.vbox_layout)

        self.registracija_re = QtCore.QRegExp(r"(^[A-Z]{2}-[0-9]{3,4}-[A-Z]{2}$)", QtCore.Qt.CaseInsensitive)
        self.registracija_validator = QtGui.QRegExpValidator(self.registracija_re)
        self.registracija.setValidator(self.registracija_validator)

    def listanje_baze(self,upit ):
        self._c = self._conn.cursor()
        self._c = self._conn.execute(upit)
        return list(self._c.fetchall())

    def fetch_u_listu(self, fetchl):
        lista = []
        for item in fetchl:
            lista.append(item[0])
        return lista

    def _on_accept(self):
        """
        self.marka = QtWidgets.QLineEdit(self)
        self.model = QtWidgets.QLineEdit(self)
        self.registracija 
        """
        if self.marka.text() == "":
            QtWidgets.QMessageBox.warning(self,
            "Marka Prazno", "Polje marka mora biti popunjeno!", QtWidgets.QMessageBox.Ok)
            return

        if self.model.text() == "":
            QtWidgets.QMessageBox.warning(self,
            "Model Prazno", "Polje model mora biti popunjeno!", QtWidgets.QMessageBox.Ok)
            return

        if self.registracija.text() == "":
            QtWidgets.QMessageBox.warning(self,
            "Registracija Prazno", "Polje registracija mora biti popunjeno!", QtWidgets.QMessageBox.Ok)
            return

        if not self.registracija.hasAcceptableInput():
            QtWidgets.QMessageBox.warning(self, 
            "Neispravna Registracija", "Primer registracije : AA-1234-BB!", QtWidgets.QMessageBox.Ok)
            return
        
        if not (self.plac_tip == self.tip.currentText() ):
            QtWidgets.QMessageBox.warning(self, 
            "Tip Vozila GREŠKA", "Tip vozila ne odgovara tipu placa!", QtWidgets.QMessageBox.Ok)
            return

        if ((int(self.brZauzetih)+1) > int(self.brUkupno) ):
            #GRESKA OVDE
            return 
        self.brZauzetih += 1 #zato sto se dodaju 1 vozila pri jednom dodavanju

        self.accept()
    def get_data(self):

        return {
            "plac_id": self.this_plac_id,
            "marka" : self.marka.text(),
            "model" : self.model.text(),
            "tip": self.plac_tip,
            "registracija" : self.registracija.text(),
            "brZ" : self.brZauzetih
        }