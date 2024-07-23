from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow 


import os
import sys

class MainWindows(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(400, 600)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()

    sys.exit(app.exec())