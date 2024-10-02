# In un file separato, ad esempio PAGE/sensor_form_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt6.QtCore import pyqtSignal

class SensorFormPage(QWidget):
    signal_back = pyqtSignal()
    signal_save_sensor = pyqtSignal(dict)  # Passa i dati del sensore come dizionario

    def __init__(self, header):
        super().__init__()
        self.header = header
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout()

        # Esempio di campi del form
        self.id_field = QLineEdit()
        self.tipo_field = QComboBox()
        self.tipo_field.addItems(["Motion", "Magnetic", "Vibration"])
        self.data_field = QLineEdit()
        self.stanza_field = QLineEdit()
        self.soglia_field = QLineEdit()

        # Pulsanti
        self.save_button = QPushButton("Salva")
        self.cancel_button = QPushButton("Annulla")

        # Connetti i pulsanti ai metodi
        self.save_button.clicked.connect(self.on_save_clicked)
        self.cancel_button.clicked.connect(self.on_cancel_clicked)

        # Aggiungi i widget al layout
        self.main_layout.addWidget(QLabel("ID:"))
        self.main_layout.addWidget(self.id_field)
        self.main_layout.addWidget(QLabel("Tipo:"))
        self.main_layout.addWidget(self.tipo_field)
        self.main_layout.addWidget(QLabel("Data:"))
        self.main_layout.addWidget(self.data_field)
        self.main_layout.addWidget(QLabel("Stanza:"))
        self.main_layout.addWidget(self.stanza_field)
        self.main_layout.addWidget(QLabel("Soglia:"))
        self.main_layout.addWidget(self.soglia_field)
        self.main_layout.addWidget(self.save_button)
        self.main_layout.addWidget(self.cancel_button)

        self.setLayout(self.main_layout)

    def on_save_clicked(self):
        # Raccogli i dati e emetti il segnale
        sensor_data = {
            "Id": self.id_field.text(),
            "Tipo": self.tipo_field.currentIndex(),
            "Data": self.data_field.text(),
            "Stanza": self.stanza_field.text(),
            "Soglia": self.soglia_field.text()
        }
        self.signal_save_sensor.emit(sensor_data)

    def on_cancel_clicked(self):
        self.signal_back.emit()

    def load_sensor_data(self, sensor):
        # Carica i dati del sensore nei campi del form per modifica
        self.id_field.setText(str(sensor.Id))
        self.tipo_field.setCurrentIndex(sensor.Tipo)
        self.data_field.setText(sensor.Data)
        self.stanza_field.setText(sensor.Stanza)
        self.soglia_field.setText(str(sensor.Soglia))
