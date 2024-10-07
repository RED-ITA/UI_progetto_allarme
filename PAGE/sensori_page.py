from PyQt6.QtGui import QColor
from PyQt6.QtCore import QFile, QTextStream, pyqtSignal
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout,
    QWidget, QHBoxLayout, QScrollArea, QPushButton
)
import sys

from API import funzioni as f
from API.DB import API_ui as db_api
from OBJ import OBJ_UI_Sensore as o
from CMP import (
    QPushButtonBadge as q,
    QWidgetSensore as w, 
    QPushButtonNoBadge as qn, 
    )
from API.LOG import log_file

class Sensori_Page(QWidget):

    signal_add_sensor = pyqtSignal()
    signal_edit_sensor = pyqtSignal(int)  # Passa l'ID del sensore da modificare

    def __init__(self, master, header):
        super().__init__()

        self.master = master
        self.master.setWindowTitle("ImpoPage")
        self.header = header
        
        self.main_layout = QVBoxLayout()
        self.init_ui()

        self.setLayout(self.main_layout)
        self.setAutoFillBackground(True)
        self.set_background_color()

    def init_ui(self):
        log_file(100)
        # Imposta le dimensioni della finestra
        screen_geometry = QApplication.primaryScreen().geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()
        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        # Inizializza i sensori
        self.init_sensors()

        # Costruisce l'interfaccia utente
        self.build_ui()

        # Imposta il colore di sfondo e lo stile
        self.set_background_color()

    def init_sensors(self):
        log_file(110)
        # Recupera tutti i sensori dal database
        sensors_data = db_api.get_all_sensori()
        self.lista_sensori = []

        for data in sensors_data:
            # Crea l'oggetto Sensore con i dati dal database
            sensor = o.Sensore(
                SensorePk=data[0],
                Id=data[1],
                Tipo=data[2],
                Data=data[3],
                Stanza=data[4],
                Soglia=data[5],
                Error=data[6],
                Stato=data[7]
            )
            self.lista_sensori.append(sensor)

    def build_ui(self):
        log_file(160)
        # Crea il widget centrale e il layout principale
        self.central_widget = QWidget()
        self.central_widget.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addWidget(self.central_widget)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

         # Pulsante per aggiungere un nuovo sensore
        self.add_sensor_button = qn.QPushButtonBadge(f.get_img("plus.png")) 
        self.add_sensor_button.setFixedSize(51,50)
        self.add_sensor_button.setContentsMargins(20,10,0,50)
        self.add_sensor_button.clicked.connect(self.on_add_sensor_clicked)
        label = QLabel("Aggiungi Sensore")
        label.setObjectName("add")
        
        # Aggiungi il pulsante al layout
        h0 = QHBoxLayout()
        h0.addSpacing(30)
        h0.addWidget(self.add_sensor_button)
        h0.addSpacing(30)
        h0.addWidget(label)
        h0.addStretch()
        self.main_layout.addLayout(h0)

        # Crea le scroll area per sensori attivi e inattivi
        self.create_scroll_areas()

        # Popola le scroll area con i widget dei sensori
        self.populate_scroll_areas()

    def create_scroll_areas(self):
        log_file(170)
        # Scroll area per sensori attivi
        self.area_active = QScrollArea()
        self.area_active.setFixedHeight(300)
        self.area_active.setWidgetResizable(True)

        # Widget e layout per sensori attivi
        self.scroll_content_active = QWidget()
        palette = self.scroll_content_active.palette()
        palette.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.scroll_content_active.setPalette(palette)
        self.h_layout_active = QHBoxLayout(self.scroll_content_active)
        self.h_layout_active.setContentsMargins(30, 0, 0, 0)

        # Imposta il contenuto della scroll area attiva
        self.area_active.setWidget(self.scroll_content_active)

        # Scroll area per sensori inattivi
        self.area_inactive = QScrollArea()
        self.area_inactive.setFixedHeight(300)
        self.area_inactive.setWidgetResizable(True)

        # Widget e layout per sensori inattivi
        self.scroll_content_inactive = QWidget()
        self.h_layout_inactive = QHBoxLayout(self.scroll_content_inactive)
        self.h_layout_inactive.setContentsMargins(30, 0, 0, 0)
        palette = self.scroll_content_inactive.palette()
        palette.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.scroll_content_inactive.setPalette(palette)

        # Imposta il contenuto della scroll area inattiva
        self.area_inactive.setWidget(self.scroll_content_inactive)

        # Aggiunge le scroll area al layout principale con i titoli
        titolo_active = QLabel("Sensori Attivi")
        titolo_active.setObjectName("titolo")
        self.main_layout.addWidget(titolo_active)
        self.main_layout.addWidget(self.area_active)
        self.main_layout.addSpacing(30)
        titolo_deactive = QLabel("Sensori Inattivi")
        titolo_deactive.setObjectName("titolo")
        self.main_layout.addWidget(titolo_deactive)
        self.main_layout.addWidget(self.area_inactive)
        self.main_layout.addStretch()

    def populate_scroll_areas(self):
        log_file(150)
        # Svuota le layout prima di popolarle
        self.clear_layout(self.h_layout_active)
        self.clear_layout(self.h_layout_inactive)

        # Aggiunge i widget dei sensori alle rispettive layout
        for sensore in self.lista_sensori:
            sensor_widget = w.QWidgetSensore(sensore)
            sensor_widget.setObjectName("sensore")
            sensor_widget.signal_parametri.connect(self.on_sensor_clicked)
            sensor_widget.signal_cestino.connect(self.elimina_sensore)
            if sensore.Stato:
                self.h_layout_active.addWidget(sensor_widget)
                self.h_layout_active.addSpacing(30)
            else:
                self.h_layout_inactive.addWidget(sensor_widget)
                self.h_layout_inactive.addSpacing(30)

        # Aggiunge uno spazio elastico alla fine delle layout
        self.h_layout_active.addStretch()
        self.h_layout_inactive.addStretch()

    def clear_layout(self, layout):
        log_file(180)
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def refresh_ui(self):
        log_file(140)
        # Ripopola le scroll area con i sensori aggiornati
        self.populate_scroll_areas()

    def elimina_sensore(self, sensor_pk):
        log_file(120, f"Tentativo di eliminazione del sensore con SensorPk {sensor_pk}")
        # Aggiorna lo stato del sensore nel database
        result = db_api.delete_sensor(sensor_pk)
        if result:
            log_file(2009, f"Sensore {sensor_pk} eliminato con successo.")
        else:
            log_file(2001, f"Errore nell'eliminazione del sensore {sensor_pk}.")
        # Aggiorna la lista dei sensori
        self.init_sensors()
        self.refresh_ui()

    def on_add_sensor_clicked(self):
        log_file(210)
        # Emette un segnale per informare il MainWindows di cambiare pagina
        self.signal_add_sensor.emit()

    def on_sensor_clicked(self, sensor_pk):
        log_file(220, f"Sensor widget con SensorPk {sensor_pk} cliccato")
        # Emette un segnale per informare il MainWindows di aprire la pagina di modifica del sensore
        self.signal_edit_sensor.emit(sensor_pk)

    def set_background_color(self):
        log_file(190)
        # Imposta il colore di sfondo
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(palette)
        self.load_stylesheet()

    def load_stylesheet(self):
        log_file(200)
        # Carica il file di stile
        file = QFile(f.get_style("sensori.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)