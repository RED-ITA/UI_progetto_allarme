from PyQt6.QtGui import  QColor
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QStackedWidget

import os
import sys

from API import funzioni as f, LOG as log
from API.DB import (
    API_generale as db, 
    API_ui as db_api,
)

from CMP import header as h 
from PAGE import (
     add_sensore_page as add_sensore,
     home_page as home, 
     impostazioni_page as impo , 
     stanze_page as stanze,
     sensori_page as sensori, 
     tastierino_dialog as tastierino
)

class MainWindows(QMainWindow):

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
            
            # PAGINA index 0
            home_page = home.Home_Page(self, self.header)
            self.main_layout.addWidget(home_page)

            # PAGINA index 1
            impo_page = impo.Impostazioni_Page(self, self.header)
            self.main_layout.addWidget(impo_page)

            # PAGINA index 2
            senso_page = sensori.Sensori_Page(self, self.header)
            self.main_layout.addWidget(senso_page)

            # Connetti i segnali di senso_page
            senso_page.signal_add_sensor.connect(self.open_add_sensor_page)
            senso_page.signal_edit_sensor.connect(self.open_edit_sensor_page)

            # PAGINA index 3
            stanze_page = stanze.Stanze_Page(self, self.header)
            self.main_layout.addWidget(stanze_page)

            # PAGINA index 4 - Pagina del form del sensore
            self.sensor_form_page = add_sensore.SensorFormPage(self.header)
            self.main_layout.addWidget(self.sensor_form_page)

            # Connetti i segnali del form del sensore
            self.sensor_form_page.signal_back.connect(self.back_to_sensors_page)
            self.sensor_form_page.signal_save_sensor.connect(self.save_sensor_data)

            self.super_layout.addWidget(self.main_layout)

            wid.setLayout(self.super_layout)
            self.setCentralWidget(wid)

            wid.setAutoFillBackground(True)
            self.set_background_color()
            log.log_file(0, "cariacate pagine")
        except Exception as e: 
            log.log_file(404, e)
    
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)
        
    def inizializzaUI(self):
        try:
            self.main_layout.setCurrentIndex(0) # parte dall widget 0 
            self.header.set_tipo(0)
            log.log_file(0, "settata la pagina inizale")
        except Exception as e: 
            log.log_file(404, e)

    def change_page(self, index):
        self.main_layout.setCurrentIndex(index)
        if index == 0:
            self.header.set_tipo(0)

    def open_add_sensor_page(self):
        # Modifica l'header se necessario
        self.header.set_tipo(4)  # Supponendo che il tipo 1 modifichi l'header
        # Pulisci i campi del form
        self.sensor_form_page.id_field.clear()
        self.sensor_form_page.tipo_field.setCurrentIndex(0)
        self.sensor_form_page.data_field.clear()
        self.sensor_form_page.stanza_field.clear()
        self.sensor_form_page.update_ui()
        # Imposta una variabile per indicare che stiamo aggiungendo un nuovo sensore
        self.sensor_form_page.edit_mode = False
        # Cambia pagina
        self.main_layout.setCurrentIndex(4)  # L'indice della pagina del form del sensore

    def open_edit_sensor_page(self, sensor_pk):
        # Modifica l'header se necessario
        self.header.set_tipo(5)  # Supponendo che il tipo 1 modifichi l'header
        # Carica i dati del sensore
        sensor = db_api.get_sensor_by_pk(sensor_pk)
        self.sensor_form_page.load_sensor_data(sensor)
        # Imposta una variabile per indicare che stiamo modificando un sensore esistente
        self.sensor_form_page.edit_mode = True
        self.sensor_form_page.sensor_pk = sensor_pk
        # Cambia pagina
        self.main_layout.setCurrentIndex(4)

    def back_to_sensors_page(self):
        # Torna alla pagina dei sensori
        self.header.set_tipo(3)
        self.main_layout.setCurrentIndex(2)

    def save_sensor_data(self, sensor_data):
        if self.sensor_form_page.edit_mode:
            # Modifica sensore esistente
            sensor_pk = self.sensor_form_page.sensor_pk
            result = db_api.edit_sensor(sensor_pk, (
                sensor_data['Id'],
                sensor_data['Tipo'],
                sensor_data['Data'],
                sensor_data['Stanza'],
                sensor_data['Soglia'],
                0  # Error field, set to 0 by default
            ))
            if result:
                log.log_file(2007, f"Sensore {sensor_pk} modificato con successo.")
            else:
                log.log_file(2001, f"Errore nella modifica del sensore {sensor_pk}.")
        else:
            # Aggiungi nuovo sensore
            result = db_api.add_sensor((
                sensor_data['Id'],
                sensor_data['Tipo'],
                sensor_data['Data'],
                sensor_data['Stanza'],
                sensor_data['Soglia'],
                0  # Error field, set to 0 by default
            ))
            if result:
                log.log_file(2005, "Nuovo sensore aggiunto con successo.")
            else:
                log.log_file(2001, "Errore nell'aggiunta del nuovo sensore.")
        # Torna alla pagina dei sensori e aggiorna la lista
        self.back_to_sensors_page()
        # Aggiorna la pagina dei sensori
        senso_page = self.main_layout.widget(2)
        senso_page.init_sensors()
        senso_page.refresh_ui()
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()

    sys.exit(app.exec())