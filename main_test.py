from PyQt6.QtGui import QColor
from PyQt6.QtCore import QFile, QTextStream
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout,
    QWidget, QHBoxLayout, QScrollArea
)
import sys

from API import funzioni as f
from API.DB import API_ui as db_api
from OBJ import OBJ_UI_Sensore as o
from CMP import QWidgetSensore as w
from API.LOG import log_file

class MainWindows(QMainWindow):

    def __init__(self):
        super().__init__()
        log_file(0, "Avvio dell'applicazione MainWindows")
        self.init_ui()

    def init_ui(self):
        log_file(100, "Inizializzazione dell'interfaccia utente")
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
        log_file(110, "Inizializzazione dei sensori")
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
        log_file(160, "Costruzione dell'interfaccia utente")
        # Crea il widget centrale e il layout principale
        self.central_widget = QWidget()
        self.central_widget.setContentsMargins(0, 0, 0, 0)
        self.layout_main = QVBoxLayout(self.central_widget)
        self.layout_main.setSpacing(0)
        self.layout_main.setContentsMargins(0, 0, 0, 0)

        # Crea le scroll area per sensori attivi e inattivi
        self.create_scroll_areas()

        # Popola le scroll area con i widget dei sensori
        self.populate_scroll_areas()

        # Imposta il widget centrale
        self.setCentralWidget(self.central_widget)

    def create_scroll_areas(self):
        log_file(170, "Creazione delle aree di scorrimento per sensori attivi e inattivi")
        # Scroll area per sensori attivi
        self.area_active = QScrollArea()
        self.area_active.setFixedHeight(350)
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
        self.area_inactive.setFixedHeight(350)
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
        self.layout_main.addWidget(titolo_active)
        self.layout_main.addWidget(self.area_active)
        self.layout_main.addSpacing(50)
        titolo_deactive = QLabel("Sensori Inattivi")
        titolo_deactive.setObjectName("titolo")
        self.layout_main.addWidget(titolo_deactive)
        self.layout_main.addWidget(self.area_inactive)
        self.layout_main.addStretch()

    def populate_scroll_areas(self):
        log_file(150, "Popolamento delle aree di scorrimento con i widget dei sensori")
        # Svuota le layout prima di popolarle
        self.clear_layout(self.h_layout_active)
        self.clear_layout(self.h_layout_inactive)

        # Aggiunge i widget dei sensori alle rispettive layout
        for sensore in self.lista_sensori:
            sensor_widget = w.QWidgetSensore(sensore)
            sensor_widget.setObjectName("sensore")
            sensor_widget.signal_parametri.connect(self.apri_parametri)
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
        log_file(180, "Svuotamento del layout")
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def refresh_ui(self):
        log_file(140, "Aggiornamento dell'interfaccia utente")
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

    def apri_parametri(self, sensor_pk):
        log_file(130, f"Apertura della schermata parametri per il sensore {sensor_pk}")
        # Implementa la logica per aprire la schermata dei parametri

    def set_background_color(self):
        log_file(190, "Impostazione del colore di sfondo")
        # Imposta il colore di sfondo
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(palette)
        self.load_stylesheet()

    def load_stylesheet(self):
        log_file(200, "Caricamento del file di stile")
        # Carica il file di stile
        file = QFile(f.get_style("sensori.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()
    sys.exit(app.exec())