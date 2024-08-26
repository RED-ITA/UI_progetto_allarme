from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QApplication, QLabel
from PyQt6.QtCore import QFile, QTextStream, QSize
from PyQt6.QtGui import QColor, QPalette

import sys

from API import funzioni as f
from CMP import QPushButtonBadge as q


class Home_Page(QWidget):

    def __init__(self, master):
        super().__init__()

        self.master = master
        self.master.setWindowTitle("HomePage")
        
        self.initUI()

        self.setAutoFillBackground(True)
        self.set_background_color()

    def initUI(self):
        # Initialize the UI elements
        self.layout1 = QVBoxLayout()

        self.prima_riga = QHBoxLayout()
        self.h1 = QHBoxLayout()
        self.h2 = QHBoxLayout()

        self.add_buttons_to_layout()

        self.setLayout(self.layout1)

    def add_buttons_to_layout(self):
        size_ico = int(self.get_icon_size() / 2)

        # Navigation bar
        self.sos = q.QPushButtonBadge("sos.png")
        self.sos.setFixedSize(size_ico, size_ico)

        # Ora
        v = QVBoxLayout()
        data = QLabel("Giorno N Mese")
        ora = QLabel("HH : MM")
        v.addWidget(data)
        v.addWidget(ora)

        self.layout_pagina = QHBoxLayout()
        self.home_button = q.QPushButtonBadge("home.png")
        self.home_button.setFixedSize(size_ico, size_ico)
        label = QLabel("Home")

        self.layout_pagina.setSpacing(0)
        self.layout_pagina.addWidget(label)
        self.layout_pagina.addWidget(self.home_button)

        self.prima_riga.addSpacing(self.get_icon_size())
        self.prima_riga.addWidget(self.sos)
        self.prima_riga.addLayout(v)
        self.prima_riga.addLayout(self.layout_pagina)
        self.prima_riga.addSpacing(self.get_icon_size())

        self.h1.addSpacing(int(self.master.width() * 0.2))

        # First row
        self.warning_button = q.QPushButtonBadge("warning.png")
        self.warning_button.setFixedSize(size_ico, size_ico)
        self.warning_button.clicked.connect(self.warning)
        self.h1.addWidget(self.warning_button)

        self.settings_button = q.QPushButtonBadge("settings.png")
        self.settings_button.setFixedSize(size_ico, size_ico)
        self.settings_button.clicked.connect(self.impostazioni)
        self.h1.addWidget(self.settings_button)

        self.sensors_button = q.QPushButtonBadge("eye.png")
        self.sensors_button.setFixedSize(size_ico, size_ico)
        self.sensors_button.clicked.connect(self.sensori)
        self.h1.addWidget(self.sensors_button)

        self.h1.addSpacing(int(self.master.width() * 0.2))

        self.h2.addSpacing(int(self.master.width() * 0.2))

        # Second row
        self.rooms_button = q.QPushButtonBadge("home.png")
        self.rooms_button.setFixedSize(size_ico, size_ico)
        self.rooms_button.clicked.connect(self.stanze)
        self.h2.addWidget(self.rooms_button)

        self.activate_button = q.QPushButtonBadge("bell_orange.png")
        self.activate_button.setFixedSize(size_ico, size_ico)
        self.activate_button.clicked.connect(self.attiva)
        self.h2.addWidget(self.activate_button)

        self.deactivate_button = q.QPushButtonBadge("bell_slash_red.png")
        self.deactivate_button.setFixedSize(size_ico, size_ico)
        self.deactivate_button.clicked.connect(self.disattiva)
        self.deactivate_button.setVisible(False)
        self.h2.addWidget(self.deactivate_button)

        self.detections_button = q.QPushButtonBadge("bell_badge.png")
        self.detections_button.setFixedSize(size_ico, size_ico)
        self.detections_button.clicked.connect(self.rilevamenti)
        self.h2.addWidget(self.detections_button)

        self.h2.addSpacing(int(self.master.width() * 0.2))

        self.layout1.addLayout(self.prima_riga)
        self.layout1.addLayout(self.h1)
        self.layout1.addLayout(self.h2)

    def get_icon_size(self):
        # Calculate icon size based on application window width
        return int(self.master.width() * 0.1)

    def resizeEvent(self, event):
        # Update icon size when application window size changes
        self.update_icon_size()
        super().resizeEvent(event)

    def update_icon_size(self):
        size_ico = self.get_icon_size()
        for button in [self.warning_button, self.settings_button, self.sensors_button, 
                       self.rooms_button, self.activate_button, self.deactivate_button, 
                       self.detections_button, self.sos, self.home_button]:
            button.setFixedSize(size_ico, size_ico)

    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)
        # Load the stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        file = QFile(f.get_style("home.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)

    def warning(self):
        print("anomalie")
        
    def impostazioni(self):
        print("impostazioni")
        
    def sensori(self):
        print("sensori")

    def stanze(self):
        print("stanze")
        
    def attiva(self):
        print("attiva")
        self.activate_button.setVisible(False)
        self.deactivate_button.setVisible(True)

    def disattiva(self):
        print("disattiva")
        self.deactivate_button.setVisible(False)
        self.activate_button.setVisible(True)
        
    def rilevamenti(self):
        print("rilevamenti")
