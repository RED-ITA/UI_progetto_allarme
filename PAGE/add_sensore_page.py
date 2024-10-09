# In un file separato, ad esempio PAGE/sensor_form_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QInputDialog, QSlider
from PyQt6.QtCore import QFile, QTextStream, pyqtSignal, Qt
from datetime import datetime
from API.LOG import log_file
from API.DB import API_ui as db
from API import funzioni as f

class SensorFormPage(QWidget):
    signal_back = pyqtSignal()
    signal_save_sensor = pyqtSignal(dict)  # Passa i dati del sensore come dizionario

    def __init__(self, header):
        super().__init__()
        self.header = header
        self.stanze_disponibili = []
        self.init_ui()
        self.load_stylesheet()
        #self.reload_stanze()  # Ricarica le stanze disponibili durante l'inizializzazione

    def init_ui(self):
        self.main_layout = QVBoxLayout()
        
        # Esempio di campi del form
        self.id_field = QLineEdit()
        self.id_field.setObjectName("idField")
        self.tipo_field = QComboBox()
        self.tipo_field.setObjectName("tipoField")
        self.tipo_field.addItems(["Motion", "Magnetic", "Vibration"])
        
        # Data field impostato automaticamente alla data odierna e non modificabile
        self.data_field = QLabel()
        self.data_field.setObjectName("dataField")
        self.data_field.setText(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        print(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        # Layout per la sezione delle stanze
        stanza_layout = QHBoxLayout()
        self.stanza_field = QComboBox()
        self.stanza_field.setObjectName("stanzaField")
        self.reload_stanze()
        self.add_stanza_button = QPushButton("Aggiungi Stanza")
        self.add_stanza_button.setObjectName("addStanzaButton")
        self.add_stanza_button.clicked.connect(self.on_add_stanza_clicked)
        self.add_stanza_button.setMaximumWidth(200)
        
        stanza_layout.addWidget(self.stanza_field)
        stanza_layout.addWidget(self.add_stanza_button)
        
        # Barra di scorrimento per la soglia
        self.soglia_slider = QSlider(Qt.Orientation.Horizontal)
        self.soglia_slider.setObjectName("sogliaSlider")
        self.soglia_slider.setRange(0, 100)
        self.soglia_slider.setTickInterval(1)
        self.soglia_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.soglia_slider.valueChanged.connect(self.on_soglia_slider_changed)

        self.soglia_value_label = QLabel("0")  # Mostra il valore corrente della soglia
        self.soglia_value_label.setFixedSize(150,50)
        self.soglia_value_label.setObjectName("sogliaValueLabel")

        soglia_layout = QHBoxLayout()
        soglia_layout.addSpacing(80)
        soglia_layout.addWidget(self.soglia_slider)
        soglia_layout.addWidget(self.soglia_value_label)
        soglia_layout.addSpacing(80)

        # Pulsanti
        self.save_button = QPushButton("Salva")
        self.save_button.setObjectName("saveButton")
        self.cancel_button = QPushButton("Annulla")
        self.cancel_button.setObjectName("cancelButton")

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
        self.main_layout.addLayout(stanza_layout)
        self.main_layout.addWidget(QLabel("Soglia:"))
        self.main_layout.addLayout(soglia_layout)
        self.main_layout.addWidget(self.save_button)
        self.main_layout.addWidget(self.cancel_button)

        self.setLayout(self.main_layout)

    def load_stylesheet(self):
        log_file(200)
        # Carica il file di stile
        file = QFile(f.get_style("add_sensore.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)

    def on_save_clicked(self):
        # Raccogli i dati e emetti il segnale
        sensor_data = {
            "Id": self.id_field.text(),
            "Tipo": self.tipo_field.currentIndex(),
            "Data": self.data_field.text(),
            "Stanza": self.stanza_field.currentText(),
            "Soglia": self.soglia_slider.value()
        }
        self.signal_save_sensor.emit(sensor_data)

    def on_cancel_clicked(self):
        self.signal_back.emit()

    def on_add_stanza_clicked(self):
        # Finestra di dialogo per prendere il nome della nuova stanza
        nome_stanza, ok = QInputDialog.getText(self, "Aggiungi Stanza", "Inserisci il nome della nuova stanza:")
        if ok and nome_stanza:
            # Aggiungi la stanza al database
            if db.add_stanza(nome_stanza):
                log_file(391, f"'{nome_stanza}")
                self.reload_stanze()
            else:
                log_file(392, f" '{nome_stanza}'.")

    def on_soglia_slider_changed(self, value):
        # Aggiorna l'etichetta del valore della soglia quando lo slider viene spostato
        self.soglia_value_label.setText(str(value))

    def load_sensor_data(self, sensor):
        # Carica i dati del sensore nei campi del form per modifica
        self.id_field.setText(str(sensor.Id))
        self.tipo_field.setCurrentIndex(sensor.Tipo)
        self.data_field.setText(sensor.Data)
        self.stanza_field.setCurrentText(sensor.Stanza)
        self.soglia_slider.setValue(sensor.Soglia)

    def reload_stanze(self):
        # Ricarica le stanze dal database e aggiorna la combobox
        self.stanze_disponibili = db.get_all_stanze()
        self.stanza_field.clear()
        if self.stanze_disponibili:
            self.stanza_field.addItems([stanza[0] for stanza in self.stanze_disponibili])
        else:
            self.stanza_field.addItem("Nessuna stanza disponibile")

    def update_ui(self):
        """
        Aggiorna l'interfaccia grafica con gli ultimi valori delle stanze e l'ora corrente.
        """
        # Aggiorna la data e l'ora
        current_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        self.data_field.setText(current_time)
        
        # Ricarica le stanze disponibili
        self.reload_stanze()

        # Log dell'aggiornamento
        log_file(400)

        print(self.stanza_field.itemText(0))