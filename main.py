from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, pyqtSignal, QMetaObject, Q_ARG, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QStackedWidget

import os
import sys

from API import funzioni as f, LOG as log
from API.DB import (
    API_generale as db, 
    API_ui as db_api,
)
from OBJ import OBJ_UI_Sensore as o

from CMP import header as h 
from PAGE import (
     add_sensore_page as add_sensore,
     home_page as home, 
     impostazioni_page as impo , 
     stanze_page as stanze,
     sensori_page as sensori, 
     tastierino_dialog as tastierino,
     loading_page as loading
)
import threading

class MainWindows(QMainWindow):
    signal_sensor_data_loaded = pyqtSignal(o.Sensore, int)  # Passa i dati del sensore e la sensor_pk
    signal_sensor_saved = pyqtSignal(bool)  # Segnale per indicare il completamento del salvataggio del sensore

    def __init__(self):
        db.create_db()
        super().__init__()
        log.setup_logger()
        
        self.setWindowTitle("ALLARME APP")
        screen_geometry = QApplication.primaryScreen().geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        
        self.create_layout()
        self.inizializzaUI()
        
    def create_layout(self):
        try:
            wid = QWidget()
            self.super_layout = QVBoxLayout()
            self.super_layout.setContentsMargins(0,0,0,0)

            self.main_layout = QStackedWidget()

            self.header = h.Header(self)
            self.super_layout.addWidget(self.header)
            
            # PAGINA di caricamento (index 0)
            self.loading_page = loading.LoadingScreen()
            self.main_layout.addWidget(self.loading_page)

            # PAGINA index 1
            self.home_page = home.Home_Page(self, self.header)
            self.main_layout.addWidget(self.home_page)

            # PAGINA index 2
            impo_page = impo.Impostazioni_Page(self, self.header)
            self.main_layout.addWidget(impo_page)

            # PAGINA index 3
            self.senso_page = sensori.Sensori_Page(self, self.header)
            self.main_layout.addWidget(self.senso_page)

            # Connetti i segnali di senso_page
            self.senso_page.signal_add_sensor.connect(self.open_add_sensor_page)
            self.senso_page.signal_edit_sensor.connect(self.open_edit_sensor_page)

            # PAGINA index 4
            stanze_page = stanze.Stanze_Page(self, self.header)
            self.main_layout.addWidget(stanze_page)

            # PAGINA index 5 - Pagina del form del sensore
            self.sensor_form_page = add_sensore.SensorFormPage(self.header)
            self.main_layout.addWidget(self.sensor_form_page)

            # PAGINA index 6 - Pagina del tastierino
            self.tastierino_form_page = tastierino.Tastierino(self, self.header)
            self.main_layout.addWidget(self.tastierino_form_page)

            # Connetti i segnali del form del sensore
            self.sensor_form_page.signal_back.connect(self.back_to_sensors_page)
            self.sensor_form_page.signal_save_sensor.connect(self.save_sensor_data)
            self.signal_sensor_saved.connect(self.handle_sensor_saved_ui_update)
            self.signal_sensor_data_loaded.connect(self.on_sensors_loaded)

            self.super_layout.addWidget(self.main_layout)

            wid.setLayout(self.super_layout)
            self.setCentralWidget(wid)

            wid.setAutoFillBackground(True)
            self.set_background_color()
            log.log_file(0, "caricate pagine")
        except Exception as e: 
            log.log_file(404, e)

    def tastierino_pass(self):
        print("passato")
        self.home_page.disattiva_passato()
        self.change_page(1)

    def tastierino_err(self):
        print("errore")
        self.change_page(1)
    
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)
        
    def inizializzaUI(self):
        try:
            self.main_layout.setCurrentIndex(0)  # parte dalla pagina di caricamento
            self.header.set_tipo(0)
            # Carica tutte le pagine in background
            threading.Thread(target=self._load_pages, daemon=True).start()
            log.log_file(0, "settata la pagina iniziale")
        except Exception as e: 
            log.log_file(404, e)

    def _load_pages(self):
        # Simula il caricamento di risorse pesanti
        import time
        time.sleep(3)  # Simula il caricamento
        QTimer.singleShot(0, lambda: self.change_page(1))  # Passa alla home una volta caricate le altre pagine

    def change_page(self, index):
        self.main_layout.setCurrentIndex(index)
        if index == 1:
            self.header.set_tipo(0)

    def open_add_sensor_page(self):
        # Modifica l'header se necessario
        self.header.set_tipo(4)  # Supponendo che il tipo 4 modifichi l'header
        # Pulisci i campi del form
        self.sensor_form_page.id_field.clear()
        self.sensor_form_page.tipo_field.setCurrentIndex(0)
        self.sensor_form_page.data_field.clear()
        self.sensor_form_page.stanza_field.clear()
        self.sensor_form_page.update_ui()
        # Imposta una variabile per indicare che stiamo aggiungendo un nuovo sensore
        self.sensor_form_page.edit_mode = False
        # Cambia pagina
        self.main_layout.setCurrentIndex(5)  # L'indice della pagina del form del sensore

    def open_edit_sensor_page(self, sensor_pk):
        # Modifica l'header se necessario
        self.header.set_tipo(5)  # Supponendo che il tipo 5 modifichi l'header
        # Carica i dati del sensore
        future = db_api.get_sensor_by_pk(sensor_pk)
        future.add_done_callback(lambda fut: self.handle_sensor_loaded(fut, sensor_pk))

    def handle_sensor_loaded(self, future, sensor_pk):
        self._log_thread_info("handle_loadedSensor_completata")
        try:
            risult = future.result()
            QMetaObject.invokeMethod(self, "signal_sensor_data_loaded.emit", Qt.ConnectionType.QueuedConnection, Q_ARG(o.Sensore, risult), Q_ARG(int, sensor_pk))
            log.log_file(1000, f"Sensor loaded: {risult}")
        except Exception as e:
            log.log_file(404, f"{e}")

    def on_sensors_loaded(self, result, sensor_pk):
        # Carica i dati del sensore nella form di modifica
        self.sensor_form_page.load_sensor_data(result)
        # Imposta la modalità di modifica
        self.sensor_form_page.edit_mode = True
        # Passa la primary key del sensore alla pagina di modifica
        self.sensor_form_page.sensor_pk = sensor_pk
        # Cambia pagina
        self.main_layout.setCurrentIndex(5)

    def back_to_sensors_page(self):
        # Torna alla pagina dei sensori
        self.header.set_tipo(3)
        self.main_layout.setCurrentIndex(3)

    def save_sensor_data(self, sensor_data):
        future = db_api.edit_sensor(self.sensor_form_page.sensor_pk, (
            sensor_data['Id'],
            sensor_data['Tipo'],
            sensor_data['Data'],
            sensor_data['Stanza'],
            sensor_data['Soglia'],
            0  # Error field, set to 0 by default
        )) if self.sensor_form_page.edit_mode else db_api.add_sensor((
            sensor_data['Id'],
            sensor_data['Tipo'],
            sensor_data['Data'],
            sensor_data['Stanza'],
            sensor_data['Soglia'],
            0  # Error field, set to 0 by default
        ))
        future.add_done_callback(lambda fut: self.handle_sensor_saved(fut))

    def handle_sensor_saved(self, future):
        try:
            result = future.result()
            success = bool(result)
            QMetaObject.invokeMethod(self, "signal_sensor_saved.emit", Qt.ConnectionType.QueuedConnection, Q_ARG(bool, success))
        except Exception as e:
            log.log_file(404, f"{e}")
            QMetaObject.invokeMethod(self, "signal_sensor_saved.emit", Qt.ConnectionType.QueuedConnection, Q_ARG(bool, False))

    def handle_sensor_saved_ui_update(self, success):
        if success:
            log.log_file(2007 if self.sensor_form_page.edit_mode else 2005, "Sensore modificato con successo." if self.sensor_form_page.edit_mode else "Nuovo sensore aggiunto con successo.")
        else:
            log.log_file(2001, "Errore nella modifica del sensore." if self.sensor_form_page.edit_mode else "Errore nell'aggiunta del nuovo sensore.")
        # Torna alla pagina dei sensori e aggiorna la lista
        self.back_to_sensors_page()
        # Aggiorna la pagina dei sensori
        self.senso_page.init_sensors()
        self.senso_page.refresh_ui()
            
    def _log_thread_info(self, function_name):
        """Log thread information for diagnostics."""
        current_thread = threading.current_thread()
        log.log_file(1000, f"DEBUG THREAD | {function_name} eseguito su thread: {current_thread.name} (ID: {current_thread.ident})")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()

    sys.exit(app.exec())
