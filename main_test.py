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
        self.resize(400, 600)
        self.inizializzaUI()
    
    def inizializzaUI(self):

        self.main_layout = QStackedWidget()

        home_page = home.Home_Page(self)
        self.main_layout.addWidget(home_page)

        self.setCentralWidget(self.main_layout)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()

    sys.exit(app.exec())