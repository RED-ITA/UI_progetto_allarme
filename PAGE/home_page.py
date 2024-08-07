
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

        self.buttons = []
        self.create_buttons()
        self.add_buttons_to_layout()

        self.setLayout(self.layout1)

    def create_buttons(self):
        # Create QPushButtonBadge instances
        icons = ["warning.png", "settings.png", "eye.png", "home.png", "bell_orange.png", "bell_badge.png"]
        for icon in icons:
            button = q.QPushButtonBadge(icon)
            self.buttons.append(button)

    def add_buttons_to_layout(self):
        size_ico = int(self.get_icon_size() / 2)

        #navigation bar
        self.sos = q.QPushButtonBadge("sos.png")
        self.sos.setFixedSize(size_ico, size_ico)

        #ora
        v = QVBoxLayout()
        data = QLabel("Giorno N Mese")
        ora = QLabel("HH : MM")
        v.addWidget(data)
        v.addWidget(ora)

        self.layout_pagina = QHBoxLayout()
        badge = q.QPushButtonBadge("home.png")
        badge.setFixedSize(size_ico, size_ico)
        label = QLabel("Home")

        self.layout_pagina.setSpacing(0)
        self.layout_pagina.addWidget(label)
        self.layout_pagina.addWidget(badge)

        self.prima_riga.addSpacing(self.get_icon_size())
        self.prima_riga.addWidget(self.sos)
        self.prima_riga.addLayout(v)
        self.prima_riga.addLayout(self.layout_pagina)
        self.prima_riga.addSpacing(self.get_icon_size())

        self.h1.addSpacing(int(self.master.width() * 0.2))
        # First row
        for button in self.buttons[:3]:
            button.setFixedSize(size_ico, size_ico)
            self.h1.addWidget(button)
        self.h1.addSpacing(int(self.master.width() * 0.2))

        self.h2.addSpacing(int(self.master.width() * 0.2))
        # Second row
        for button in self.buttons[3:]:
            button.setFixedSize(size_ico, size_ico)
            self.h2.addWidget(button)
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
        for button in self.buttons:
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