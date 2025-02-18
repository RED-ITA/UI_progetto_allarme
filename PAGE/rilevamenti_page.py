from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QScrollArea, QPushButton, QLabel, QLineEdit, QDialog, QDialogButtonBox
from PyQt6.QtCore import QFile, QTextStream, QSize, Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPixmap, QIcon

import sys

from API import funzioni as f
from API.DB import API_ui as db_api
from CMP import (
    QPushButtonBadge as q,
    QWidgetSensore as w, 
    QPushButtonNoBadge as qn, 
    )
from API.LOG import log_file
from OBJ import OBJ_UI_Sensore as o

class Rilevamenti_page(QWidget):


    def __init__(self, master, header):
        super().__init__()

        self.master = master
        self.master.setWindowTitle("Stanze e Sensori")
        self.header = header

        self.main_layout = QHBoxLayout()
        
        self.initUI()
        

        self.setLayout(self.main_layout)
        self.setAutoFillBackground(True)
        self.set_background_color()

    def initUI(self):
        log_file(100, "stanze")  # Inizializzazione dell'interfaccia Stanze_Page

        # Scroll area a sinistra con le stanze disponibili
        self.area_ogg = QScrollArea()
        self.area_ogg.setWidgetResizable(True)

        self.scroll_content_stanze = QWidget()
        self.scroll_content_stanze.setObjectName("wid")

        self.v_layout_stanze = QVBoxLayout(self.area_ogg)
        self.v_layout_stanze.setContentsMargins(10, 10, 10, 10)
        self.area_ogg.setWidget(self.scroll_content_stanze)

        h0 = QVBoxLayout()
        titolo_oggi = QLabel("ULITME 24 ORE")
        titolo_oggi.setObjectName("titolo")
        titolo_oggi.setAlignment(Qt.AlignmentFlag.AlignCenter)

        h0.addWidget(titolo_oggi)
        h0.addWidget(self.area_ogg)

        self.main_layout.addLayout(h0)

        
        # Area per i sensori attivi della stanza selezionata
        self.scroll_content_sensori = QWidget()
        self.scroll_content_sensori.setObjectName("wid")
        self.h_layout_sensori = QVBoxLayout(self.scroll_content_sensori)
        self.h_layout_sensori.setContentsMargins(10, 10, 10, 10)
        self.area_all = QScrollArea()
        
        self.area_all.setWidgetResizable(True)
        self.area_all.setWidget(self.scroll_content_sensori)
        
        h1 = QVBoxLayout()
        titolo_all = QLabel("TUTTI I RILEVAMENTI")
        titolo_all.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titolo_all.setObjectName("titolo")

        h1.addWidget(titolo_all)
        h1.addWidget(self.area_all)

        self.main_layout.addLayout(h1)

        

    def clear_layout(self, layout):
        log_file(350)  # Svuotamento del layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def set_background_color(self):
        log_file(360)  # Impostazione del colore di sfondo
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)
        # Carica lo stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        log_file(370)  # Caricamento del file di stile
        file = QFile(f.get_style("rilevamenti.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)