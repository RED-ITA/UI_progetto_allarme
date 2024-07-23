from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout


import os
import sys

class MainWindows(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(400, 600)
        self.inizializzaUI()
    
    def inizializzaUI(self):
        centralWidget = QWidget()

        self.layout1 = QHBoxLayout()

        self.l1 = QVBoxLayout()
        self.testo = QLabel()
        self.testo2 = QLabel()
        self.testo.setText("Testo Sopra a sinistra")
        self.testo2.setText("Testo Sotto a sinistra")
        self.l1.addWidget(self.testo)
        self.l1.addWidget(self.testo2)

        self.l2 = QVBoxLayout()
        self.testo3 = QLabel()
        self.testo4 = QLabel()
        self.testo3.setText("Testo Sopra a destra")
        self.testo4.setText("Testo Sotto a destra")
        self.l2.addWidget(self.testo3)
        self.l2.addWidget(self.testo4)
        

        self.layout1.addLayout(self.l1)
        self.layout1.addStretch()
        self.layout1.addLayout(self.l2)

        centralWidget.setLayout(self.layout1)
        self.setCentralWidget(centralWidget)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()

    sys.exit(app.exec())