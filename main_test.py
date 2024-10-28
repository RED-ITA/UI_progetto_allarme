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
from API.DB.API_ui import QueueProcessor
from OBJ import OBJ_UI_Sensore as o
from CMP import QWidgetSensore as w
from API.LOG import log_file
from PAGE import loading_page as ld, stanze_page as sensori

import os

from CMP import header as h 






class MainWindows(QMainWindow):

    def __init__(self):
        self.queue_processor = QueueProcessor()
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
        self.home_page = sensori.Stanze_Page(self, header=self.header)
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