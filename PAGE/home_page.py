from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QApplication, QLabel
from PyQt6.QtCore import QFile, QTextStream, QSize, Qt, QTimer, QTime
from PyQt6.QtGui import QColor, QPalette

import sys

from API import funzioni as f
from CMP import QPushButtonBadge as q


class Home_Page(QWidget):

    def __init__(self, master, header):
        super().__init__()

        self.master = master
        self.master.setWindowTitle("HomePage")
        
    
        self.header = header
        self.initUI()

        self.setAutoFillBackground(True)
        self.set_background_color()

    def initUI(self):
        # Initialize the UI elements
        self.layout1 = QVBoxLayout()
        
        self.h1 = QHBoxLayout()
        self.h2 = QHBoxLayout()
        self.add_buttons_to_layout()

        self.setLayout(self.layout1)

        # Force update layout to ensure visibility
        self.layout1.update()
        self.layout1.activate()


    def add_buttons_to_layout(self):
        size_ico = int(self.get_icon_size() / 2)


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
        self.rooms_button = q.QPushButtonBadge("rooms.png")
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

        
        self.layout1.addLayout(self.h1)
        self.layout1.addLayout(self.h2)


    def get_icon_size(self):
        # Calculate icon size based on application window width
        return int((self.master.width() * 0.1) )

    def resizeEvent(self, event):
        # Update icon size when application window size changes
        self.update_icon_size()
        super().resizeEvent(event)

    def update_icon_size(self):
       
        size_ico = int(self.get_icon_size())
        for button in [self.warning_button, self.settings_button, self.sensors_button, 
                       self.rooms_button, self.activate_button, self.deactivate_button, 
                       self.detections_button]:
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

    #def features(self):
    #    print("magic")
        
    def impostazioni(self):
        print("impostazioni")
        self.header.set_tipo(1)
        self.master.change_page(1)
        
    def sensori(self):
        print("sensori")
        self.header.set_tipo(2)
        self.master.change_page(2)

    def stanze(self):
        print("stanze")
        self.header.set_tipo(3)
        self.master.change_page(3)
        
    def attiva(self):
        print("attiva")
        self.activate_button.setVisible(False)
        self.deactivate_button.setVisible(True)

    def disattiva(self):
        print("disattiva-tentativo")
        self.master.tastierino_form_page.reset_ui()
        self.master.change_page(5)

    def disattiva_passato(self):
        self.deactivate_button.setVisible(False)
        self.activate_button.setVisible(True)
        
    def rilevamenti(self):
        print("rilevamenti")