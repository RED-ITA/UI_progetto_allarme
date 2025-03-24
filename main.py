
from PyQt6.QtGui import  QColor
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer
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
from API.DB.API_ui import aggiungi_forzatura, update_activity_shutdown
from OBJ import OBJ_UI_Sensore as o

from CMP import header as h 
from PAGE import (
     add_sensore_page as add_sensore,
     home_page as home, 
     impostazioni_page as impo , 
     stanze_page as stanze,
     sensori_page as sensori, 
     tastierino_dialog as tastierino,
     rilevamenti_page as rilevamenti
)
import threading
import time
from websocket import WebSocketApp
import json 
import subprocess
import websocket  # pip install websocket-client

class WebSocketListener(QThread):
    # Segnale emesso al ricevere una notifica
    notification_signal = pyqtSignal(str)
    
    def __init__(self, url, parent=None):
        super(WebSocketListener, self).__init__(parent)
        self.url = url
        self.ws = None
        self.running = True
        
    def run(self):
        # Abilita il trace per maggiori informazioni (opzionale)
        websocket.enableTrace(True)
        # Inizializza la connessione includendo l'header Origin
        
        
        # run_forever è bloccante: il thread rimane in ascolto fino a quando self.running è True
        while self.running:
            try:
                self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
                self.ws.on_open = self.on_open

                self.ws.run_forever()
            except Exception as e:
                print("Errore nella connessione WebSocket:", e)

            #time.sleep(2)
    
    def on_message(self, ws, message):
        print("Messaggio ricevuto:", message)
        # Emissione del segnale con il messaggio ricevuto
        self.notification_signal.emit(message)
    
    def on_error(self, ws, error):
        print("Errore:", error)
    
    def on_close(self, ws, close_status_code, close_msg):
        print("Connessione WebSocket chiusa:", close_status_code, close_msg)
    
    def on_open(self, ws):
        print("Connessione aperta al WebSocket.")
    
    def stop(self):
        self.running = False
        if self.ws:
            self.ws.close()
            
class MainWindows(QMainWindow):
    signal_sensor_data_loaded = pyqtSignal(o.Sensore, int)  # Passa i dati del sensore e la sensor_pk
    signal_sensor_saved = pyqtSignal(bool)  # Segnale per indicare il completamento del salvataggio del sensore

    def __init__(self, flask_thread):
        # Dentro la classe Sensori_Page
        super().__init__()
        

        log.setup_logger()
        # db_manager = init_db_manager(f.get_db)  # Sostituisci con il percorso corretto del database
        self.start_websocket_listener()


        self.setWindowTitle("ALLARME APP")
        screen_geometry = QApplication.primaryScreen().geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()


        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        
        self.create_layout()
        self.inizializzaUI()
        self.flask_thread = flask_thread
        print("Il thread Flask è vivo?", self.flask_thread.is_alive())


         # Avvia un QTimer che verifica periodicamente se il thread Flask è vivo
        #self.thread_check_timer = QTimer(self)
        #self.thread_check_timer.timeout.connect(self.check_flask_thread_alive)
        #self.thread_check_timer.start(2000)  # ogni 2 secondi


    def start_websocket_listener(self): 
        # URL del WebSocket (modifica se necessario)
        ws_url = "ws://127.0.0.1:5001/process_to_ui_update"
        self.listener = WebSocketListener(ws_url)
        self.listener.notification_signal.connect(self.handle_update)
        self.listener.start()

    def check_flask_thread_alive(self):
        """Verifica se il thread Flask è ancora vivo."""
        if self.flask_thread.is_alive():
            print("Il thread Flask è ancora vivo.")
        else:
            print("Il thread Flask è morto!")
            # Se desideri fare qualcosa in caso di thread morto, fallo qui
            # Ad esempio: avviare un nuovo thread, mostrare un messaggio all'utente, ecc.

    def handle_update(self, data):
        print("Il thread Flask è vivo?", self.flask_thread.is_alive())
        # Aggiorna la UI o gestisci i dati in modo thread-safe
        print("lettura")
        self.lettura_valori()
        self.senso_page.init_sensors()
        self.senso_page.refresh_ui()
        # Inserisci il codice per aggiornare la UI o i componenti qui


    def lettura_valori(self):
        ris = controllo_valori()
        if ris == 1:
            print("allarme")
            self.home_page.allarme()


    def closeEvent(self, event):
        # Chiamata a db_stop prima di chiudere l'applicazione
        # db_stop()
        log.log_file(2701, "Chiusura dell'applicazione gestita correttamente")
        # Continua con l'evento di chiusura standard
        self.listener.stop()
        self.listener.wait()
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

            # PAGINA index 6 - Pagina dei rilevamenti
            self.rilevamenti = rilevamenti.Rilevamenti_page(self, self.header)
            self.main_layout.addWidget(self.rilevamenti)
            

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
        update_activity_shutdown()
        self.home_page.disattiva_passato()
        self.change_page(0)

    def tastierino_err(self):
        print("errore")
        aggiungi_forzatura()   
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
        print(stato)
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
        self.handle_sensor_saved(future)

    def handle_sensor_saved(self, future):
        try:
            result = future
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
        
        
def start_sqlite_web(db_path, port=8080):
    """
    Avvia il server sqlite-web per visualizzare il database.
    Assicurati di avere sqlite-web installato (pip install sqlite-web).
    """
    try:
        # Avvia sqlite-web come sottoprocesso
        subprocess.Popen(["sqlite_web", db_path, "--port", str(port)])
        print(f"sqlite-web avviato su http://localhost:{port} per il DB: {db_path}")
    except Exception as e:
        print(f"Errore nell'avvio di sqlite-web: {e}")





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
   
    
    db_path = f.get_db()  
    start_sqlite_web(db_path, port=8080)

    app = QApplication(sys.argv)
    window = MainWindows(flask_thread)
    window.show()

    #app.aboutToQuit.connect(db_stop)


    sys.exit(app.exec())
   
