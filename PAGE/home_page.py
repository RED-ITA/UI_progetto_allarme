from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, QPushButton, QSizePolicy
from PyQt6.QtCore import Qt, QFile, QTextStream
from PyQt6.QtGui import QColor, QPalette

import os
import sys

from API import funzioni as f
from CMP import QPushButtonBadge as q


class Home_Page(QWidget):

    
    def __init__(self, master):
        super().__init__()

        self.master = master
        self.master.setWindowTitle("HomePage")
        
        self.intiUI()

        self.setAutoFillBackground(True)
        self.set_background_color()
    
    def intiUI(self):
        #funzine della grafica 
        layout_inziale = QVBoxLayout()
        
        pulsante1 = q.QPushButtonBadge(image_path="calendar.png", badge_text=None, parent=self, color="f1f1f1")
        pulsante1.setFixedSize(300,300)

        pulsante2 = q.QPushButtonBadge(image_path="home.png", badge_text=None, parent=self, color="f1f1f1")
        pulsante2.setFixedSize(300,300)

        pulsante1.setBadgeText("1")
        layout_inziale.addStretch()
        layout_inziale.addWidget(pulsante1)
        layout_inziale.addStretch()
        layout_inziale.addWidget(pulsante2)
        layout_inziale.addStretch()

        self.setLayout(layout_inziale)


    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241,241,241))
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
