from PyQt6.QtGui import  QColor
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QStackedWidget

import os
import sys

from API import funzioni as f

from CMP import header as h 
from PAGE import home_page as home, impostazioni_page as impo 

class MainWindows(QMainWindow):

    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("ALLARME APP")
        screen_geometry = QApplication.primaryScreen().geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()


        self.setGeometry(0, 0, self.screen_width, self.screen_height)
        
        self.create_layout()
        self.inizializzaUI()
        
    def create_layout(self):
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
        
        self.super_layout.addWidget(self.main_layout)

        wid.setLayout(self.super_layout)
        self.setCentralWidget(wid)

        wid.setAutoFillBackground(True)
        self.set_background_color()
    
    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)
        
    def inizializzaUI(self):
        self.main_layout.setCurrentIndex(0) # parte dall widget 0 
        self.header.set_tipo(0)

    def change_page(self, index):
        self.main_layout.setCurrentIndex(index)
        if index == 0:
            self.header.set_tipo(0)
            


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()

    sys.exit(app.exec())