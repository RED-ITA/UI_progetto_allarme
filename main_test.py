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

from API.DB.queue_manager import init_db_manager, db_enqueue
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



if __name__ == "__main__":
    db_manager = init_db_manager(f.get_db())  # Sostituisci con il percorso corretto del database
    db.create_db()
    # Avvia il server Flask in un thread separato
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = False  # Termina il thread quando l'app principale si chiude
    flask_thread.start()
    