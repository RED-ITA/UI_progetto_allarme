from PyQt6.QtGui import  QColor
from PyQt6.QtCore import Qt, pyqtSignal, QThread
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QStackedWidget

import os
import sys

from API import funzioni as f, LOG as log
from API.DB import (
    API_generale as db, 
    API_ui as db_api,
)
from API.DB.web_server import run_flask_app

from API.DB.queue_manager import init_db_manager
from API.DB.API_bg import controllo_valori
from OBJ import OBJ_UI_Sensore as o

from CMP import header as h 
from PAGE import (
     add_sensore_page as add_sensore,
     home_page as home, 
     impostazioni_page as impo , 
     stanze_page as stanze,
     sensori_page as sensori, 
     tastierino_dialog as tastierino
)
import threading
import time
from websocket import WebSocketApp
import json 

class WebSocketListener(QThread):
    # Segnali PyQt
    update_received = pyqtSignal(dict)
    update_sending = pyqtSignal(int, str)
    
    def __init__(self):
        super().__init__()
        self.ws = None
        # Quando altri componenti emettono "update_sending",
        # questo slot invierà il messaggio al server WebSocket.
        self.update_sending.connect(self.send_update_to_api)

    def on_open(self, ws):
        print("Connessione WebSocket aperta")

    def on_message(self, ws, message):
        print("Messaggio ricevuto dal server:", message)
        
        # Se il server invia JSON, parse l’eventuale JSON:
        # Esempio generico: data = json.loads(message)
        # e poi emetti un segnale con i dati
        try:
            data = json.loads(message)
            self.update_received.emit(data)
        except json.JSONDecodeError:
            # Se non è JSON, fai altre gestione
            # oppure invia come stringa
            self.update_received.emit({"raw": message})

    def on_error(self, ws, error):
        print("Errore WebSocket:", error)

    def on_close(self, ws, close_status_code, close_msg):
        print("Connessione WebSocket chiusa")

    def run(self):
        # Inizializza la WebSocketApp puntando all'endpoint del tuo server
        self.ws = WebSocketApp(
            "ws://localhost:5001/ui_to_process_update",  # <--- URl WebSocket (non http)
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        # run_forever() si blocca finché la connessione è attiva.
        # Viene eseguito nel contesto di questo QThread, quindi non bloccherà la UI.
        self.ws.run_forever()

    def send_update_to_api(self, sensor_id, tipo):
        """
        Metodo connesso allo signal `update_sending`, 
        che invia un messaggio WebSocket al server.
        """
        if self.ws:
            # Costruiamo un JSON da inviare (struttura a piacere)
            msg_dict = {
                "id": sensor_id,
                "tipo": tipo
            }
            # Convertilo in stringa
            message = json.dumps(msg_dict)

            # Manda il messaggio via WebSocket
            try:
                self.ws.send(message)
                print("Messaggio inviato al server:", message)
            except Exception as e:
                print("Errore inviando messaggio WS:", e)

class MainWindows(QMainWindow):
    signal_sensor_data_loaded = pyqtSignal(o.Sensore, int)  # Passa i dati del sensore e la sensor_pk
    signal_sensor_saved = pyqtSignal(bool)  # Segnale per indicare il completamento del salvataggio del sensore

    def __init__(self):
        # Dentro la classe Sensori_Page
        super().__init__()
        

        log.setup_logger()
        # db_manager = init_db_manager(f.get_db)  # Sostituisci con il percorso corretto del database

        self.listener = WebSocketListener()

        # Collega il segnale update_received al metodo handle_update
        self.listener.update_received.connect(self.handle_update)

        self.listener.start()

        # self.listener.update_sending.emit(1, "del") #delete
        # self.listener.update_sending.emit(1, "mod") #modificato

        self.setWindowTitle("ALLARME APP")
        screen_geometry = QApplication.primaryScreen().geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()


        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        
        self.create_layout()
        self.inizializzaUI()

    def handle_update(self, data):
        # Aggiorna la UI o gestisci i dati in modo thread-safe
        self.lettura_valori()
        self.senso_page.init_sensors()
        self.senso_page.refresh_ui()
        # Inserisci il codice per aggiornare la UI o i componenti qui


    def lettura_valori(self):
        controllo_valori()


    def closeEvent(self, event):
        # Chiamata a db_stop prima di chiudere l'applicazione
        # db_stop()
        log.log_file(2701, "Chiusura dell'applicazione gestita correttamente")
        # Continua con l'evento di chiusura standard
        event.accept()
        
    def create_layout(self):
        try:
            wid = QWidget()
            self.super_layout = QVBoxLayout()
            self.super_layout.setContentsMargins(0,0,0,0)

            self.main_layout = QStackedWidget()

            self.header = h.Header(self)
            self.super_layout.addWidget(self.header)
            
            # PAGINA index 0
            self.home_page = home.Home_Page(self, self.header)
            self.main_layout.addWidget(self.home_page)

            # PAGINA index 1
            impo_page = impo.Impostazioni_Page(self, self.header)
            self.main_layout.addWidget(impo_page)

            # PAGINA index 2
            self.senso_page = sensori.Sensori_Page(self, self.header)
            self.main_layout.addWidget(self.senso_page)

            # Connetti i segnali di senso_page
            self.senso_page.signal_add_sensor.connect(self.open_add_sensor_page)
            self.senso_page.signal_edit_sensor.connect(self.open_edit_sensor_page)

            # PAGINA index 3
            stanze_page = stanze.Stanze_Page(self, self.header)
            self.main_layout.addWidget(stanze_page)

            # PAGINA index 4 - Pagina del form del sensore
            self.sensor_form_page = add_sensore.SensorFormPage(self.header)
            self.main_layout.addWidget(self.sensor_form_page)

            # PAGINA index 5 - Pagina del tastierino
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
            log.log_file(0, "cariacate pagine")
        except Exception as e: 
            log.log_file(404, e)

    def tastierino_pass(self):
        print("passato")
        self.home_page.disattiva_passato()
        self.change_page(0)

    def tastierino_err(self):
        print("errore")
        self.change_page(0)
    
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
        risult = db_api.get_sensor_by_pk(sensor_pk)
        
        self.signal_sensor_data_loaded.emit(risult, sensor_pk)
        log.log_file(1000, f"Sensor loaded: {risult}")
        # Chiama la funzione on_sensors_loaded con il risultato e sensor_pk
        
    def on_sensors_loaded(self, result, sensor_pk):
        # Carica i dati del sensore nella form di modifica
        self.sensor_form_page.load_sensor_data(result)
        # Imposta la modalità di modifica
        self.sensor_form_page.edit_mode = True
        # Passa la primary key del sensore alla pagina di modifica
        self.sensor_form_page.sensor_pk = sensor_pk
        # Cambia pagina
        self.main_layout.setCurrentIndex(4)

    def back_to_sensors_page(self):
        # Torna alla pagina dei sensori
        self.header.set_tipo(3)
        self.main_layout.setCurrentIndex(2)

    def save_sensor_data(self, sensor_data):
        if sensor_data['Stanza'] != "":
            stato = 1
        else:
            stato = 0
        future = db_api.edit_sensor(self.sensor_form_page.sensor_pk, (
            sensor_data['Tipo'],
            sensor_data['Data'],
            sensor_data['Stanza'],
            sensor_data['Soglia'],
            stato  # Error field, set to 0 by default
        )) if self.sensor_form_page.edit_mode else db_api.add_sensor((
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
            
            self.signal_sensor_saved.emit(success)
        except Exception as e:
            log.log_file(404, f"{e}")
            self.signal_sensor_saved.emit(False)

    def handle_sensor_saved_ui_update(self, success):
        if success:
            self.listener.update_sending.emit(self.sensor_form_page.sensor_pk, "mod") #modificato
            log.log_file(2007 if self.sensor_form_page.edit_mode else 2005, "Sensore modificato con successo." if self.sensor_form_page.edit_mode else "Nuovo sensore aggiunto con successo.")
        else:
            log.log_file(2001, "Errore nella modifica del sensore." if self.sensor_form_page.edit_mode else "Errore nell'aggiunta del nuovo sensore.")
        # Torna alla pagina dei sensori e aggiorna la lista
        self.back_to_sensors_page()
        # Aggiorna la pagina dei sensori
        self.senso_page.init_sensors()
        self.senso_page.refresh_ui()
            
    def eliminalo(self, id):
        self.listener.update_sending.emit(id, "del") #delete
    
    def _log_thread_info(self, function_name):
        """Log thread information for diagnostics."""
        current_thread = threading.current_thread()
        log.log_file(1000, f"DEBUG THREAD | {function_name} eseguito su thread: {current_thread.name} (ID: {current_thread.ident})")
        
        


if __name__ == "__main__":
    db.create_db()
    # Avvia il server Flask in un thread separato
    db_manager = init_db_manager(f.get_db())  # Sostituisci con il percorso corretto del database
    db.create_db()
    # Avvia il server Flask in un thread separato
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = False  # Termina il thread quando l'app principale si chiude
    flask_thread.start()
    

    time.sleep(10)

    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()

    #app.aboutToQuit.connect(db_stop)


    sys.exit(app.exec())
   
