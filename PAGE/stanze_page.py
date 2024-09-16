from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QApplication, QLabel
from PyQt6.QtCore import QFile, QTextStream, QSize, Qt, QTimer, QTime
from PyQt6.QtGui import QColor, QPalette

import sys

from API import funzioni as f
from CMP import QPushButtonBadge as q


class Stanze_Page(QWidget):

    def __init__(self, master, header):
        super().__init__()

        self.master = master
        self.master.setWindowTitle("ImpoPage")
        self.header = header
        

        self.main_layout = QVBoxLayout()
        self.initUI()

        self.setLayout(self.main_layout)
        self.setAutoFillBackground(True)
        self.set_background_color()

    def initUI(self):
        self.main_layout.addStretch()

    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)
        # Load the stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        file = QFile(f.get_style("impo.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)