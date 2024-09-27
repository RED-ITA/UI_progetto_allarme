from PyQt6.QtGui import  QColor
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QStackedWidget

import os
import sys

from API import funzioni as f, LOG as log

from CMP import header as h 
from PAGE import (
     home_page as home, 
     impostazioni_page as impo , 
     stanze_page as stanze,
     sensori_page as sensori, 
     tastierino_dialog as tastierino
)

class MainWindows(QMainWindow):

    def __init__(self):
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
            #PAGINA index 0
            home_page = home.Home_Page(self, self.header)
            self.main_layout.addWidget(home_page)

            #PAGINA index 1
            impo_page = impo.Impostazioni_Page(self, self.header)
            self.main_layout.addWidget(impo_page)

            #PAGINA index 2
            senso_page = sensori.Sensori_Page(self, self.header)
            self.main_layout.addWidget(senso_page)

            #PAGINA index 3
            stanze_page = stanze.Stanze_Page(self, self.header)
            self.main_layout.addWidget(stanze_page)

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
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()

    sys.exit(app.exec())