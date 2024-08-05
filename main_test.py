from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QStackedWidget


import os
import sys

from API import funzioni as f


from PAGE import home_page as home

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
        self.main_layout = QStackedWidget()
        
        #PAGINA 0
        home_page = home.Home_Page(self)
        self.main_layout.addWidget(home_page)
        
        #PAGINA 1
        
        self.setCentralWidget(self.main_layout)
        
        
    def inizializzaUI(self):

        
        self.main_layout.setCurrentIndex(0) # parte dall widget 0 

        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()

    sys.exit(app.exec())