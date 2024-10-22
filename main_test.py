from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt, QRunnable, QThreadPool, pyqtSignal, QObject, QTextStream, QFile
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout,
    QWidget, QHBoxLayout, QScrollArea, QPushButton, QStackedWidget
)
import sys
import time 
from API import funzioni as f
from API.DB import API_ui as db_api
from OBJ import OBJ_UI_Sensore as o
from CMP import QWidgetSensore as w
from API.LOG import log_file
from PAGE import loading_page as ld

import os

from CMP import header as h 


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)

class Task(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = WorkerSignals()

    def run(self):
        try:
            # Simula un task che richiede del tempo (es. operazione sul database)
            time.sleep(5)  # Sostituisci con la tua funzione bloccante
            self.signals.finished.emit()  # Task completato con successo
        except Exception as e:
            self.signals.error.emit(str(e))  # In caso di errore


class MainWindow(QWidget):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.thread_pool = QThreadPool()  # QThreadPool per gestire i thread
        self.init_ui()

    def init_ui(self):
        # Layout principale
        
        self.setWindowTitle("PyQt6 Schermata di Caricamento Dinamica")
        # Pulsante per avviare il task
        self.button = QPushButton("Avvia Task Lungo", self)
        self.button.clicked.connect(self.start_long_task)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.set_background_color()
        self.load_stylesheet()

    def start_long_task(self):
        self.master.loading_p()
        # Mostra la schermata di caricamento

        # Esegui il task in modo asincrono
        task = Task()
        task.signals.finished.connect(self.on_task_finished)
        task.signals.error.connect(self.on_task_error)

        # Avvia il task usando il thread pool
        self.thread_pool.start(task)

    def on_task_finished(self):
        self.master.loading_e()
        # Chiudi la schermata di caricamento e riabilita il pulsante

    def on_task_error(self, error_message):
        # Gestisci eventuali errori, chiudi la schermata di caricamento e riabilita il pulsante
        self.master.loading_e()
        print(f"Errore durante l'esecuzione del task: {error_message}")

    def set_background_color(self):
        
        # Imposta il colore di sfondo
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(palette)
        self.load_stylesheet()

    def load_stylesheet(self):
       
        # Carica il file di stile
        file = QFile(f.get_style("sensori.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)



class MainWindows(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("ALLARME APP")
        screen_geometry = QApplication.primaryScreen().geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()


        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        
        self.create_layout()
        
        self.set_background_color()
        self.load_stylesheet()

    def create_layout(self):
        
        wid = QWidget()
        self.super_layout = QVBoxLayout()
        self.super_layout.setContentsMargins(0,0,0,0)
        self.main_layout = QStackedWidget()

        self.header = h.Header(self)
        self.super_layout.addWidget(self.header)
        
        # PAGINA index 0
        self.home_page = MainWindow(self)
        self.main_layout.addWidget(self.home_page)

        # PAGINA index 1
        self.loading_page = ld.LoadingScreen()
        self.main_layout.addWidget( self.loading_page)


        self.super_layout.addWidget(self.main_layout)
        wid.setLayout(self.super_layout)
        self.setCentralWidget(wid)


    def loading_p(self):
        self.main_layout.setCurrentIndex(1)

    def loading_e(self):
        self.main_layout.setCurrentIndex(0)

    def set_background_color(self):
        
        # Imposta il colore di sfondo
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(palette)
        self.load_stylesheet()

    def load_stylesheet(self):
       
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