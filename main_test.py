from PyQt6.QtGui import  QColor
from PyQt6.QtCore import Qt, pyqtSignal, QFile, QTextStream
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QStackedWidget, QScrollArea

import os
import sys

from API import funzioni as f, LOG as log
from OBJ import OBJ_UI_Sensore as o
from CMP import header as h, QWidgetSensore as w

from PAGE import (
     home_page as home, 
     impostazioni_page as impo , 
     stanze_page as stanze,
     sensori_page as sensori, 
     tastierino_dialog as tastierino
)

class MainWindows(QMainWindow):

    def __init__(self):
        super().__init__()

        screen_geometry = QApplication.primaryScreen().geometry()
        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()


        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        wid = QWidget()
        wid.setContentsMargins(0,0,0,0)
        lista = []

        # Creazione degli oggetti Sensore
        oggetto0 = o.Sensore(0, 1, 0, "23/13/12", "cucina", 0, 0, 1)
        lista.append(oggetto0)
        oggetto1 = o.Sensore(0, 2, 0, "23/13/12", "cucina", 0, 0, 0)
        lista.append(oggetto1)
        oggetto2 = o.Sensore(0, 3, 1, "23/13/12", "cucina", 0, 0, 1)
        lista.append(oggetto2)
        oggetto3 = o.Sensore(0, 4, 1, "23/13/12", "cucina", 0, 0, 0)
        lista.append(oggetto3)
        oggetto4 = o.Sensore(0, 5, 2, "23/13/12", "cucina", 0, 0, 1)
        lista.append(oggetto4)
        oggetto5 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 0)
        lista.append(oggetto5)
        oggetto6 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 0)
        lista.append(oggetto6)
        oggetto7 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 0)
        lista.append(oggetto7)
        oggetto8 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 0)
        lista.append(oggetto8)
        oggetto9 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 0)
        lista.append(oggetto9)
        oggetto10 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 0)
        lista.append(oggetto10)
        oggetto11 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 0)
        lista.append(oggetto11)

        # Creazione della QScrollArea
        area = QScrollArea()
        area.setContentsMargins(0,0,0,0)
        area.setFixedHeight(350)
        area.setFixedWidth(self.screen_width)
        area.setWidgetResizable(True)  # Permette il ridimensionamento del widget

        

        # Creazione della QScrollArea
        area1 = QScrollArea()
        area1.setContentsMargins(0,0,0,0)
        area1.setFixedHeight(350)
        area1.setFixedWidth(self.screen_width)
        area1.setWidgetResizable(True)  # Permette il ridimensionamento del widget

        # Widget interno che conterrà il layout orizzontale
        scroll_content = QWidget()
        p = scroll_content.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        scroll_content.setPalette(p)
        scroll_content.setObjectName("oggetto")
        h0 = QHBoxLayout(scroll_content)
        h0.addSpacing(30)


        # Widget interno che conterrà il layout orizzontale
        scroll_content1 = QWidget()
        p = scroll_content1.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        scroll_content1.setPalette(p)
        h1 = QHBoxLayout(scroll_content1)
        scroll_content1.setObjectName("oggetto")
        h1.addSpacing(30)

        # Aggiunta degli oggetti alla scroll area
        for oggetto in lista: 
            if oggetto.Stato:
                UI_og = w.QWidgetSensore(oggetto)
                UI_og.setObjectName("sensore")
                UI_og.signal_parametri.connect(self.apri_parametri)
                UI_og.signal_cestino.connect(self.elimina_sensore)
                h0.addWidget(UI_og)
                h0.addSpacing(30)
            else:
                UI_og = w.QWidgetSensore(oggetto)
                UI_og.setObjectName("sensore")
                UI_og.signal_parametri.connect(self.apri_parametri)
                UI_og.signal_cestino.connect(self.elimina_sensore)

                h1.addWidget(UI_og)
                h1.addSpacing(30)

        # Aggiunge un'espansione alla fine
        h0.addStretch()
        h1.addStretch()

        # Imposta il widget contenitore all'interno della scroll area

        titotlo1 = QLabel("Sensori Attivi")
        titotlo1.setObjectName("titolo")
        area.setWidget(scroll_content)

        
        titotlo2 = QLabel("Sensori Disattivi")
        titotlo2.setObjectName("titolo")
        area1.setWidget(scroll_content1)

        # Aggiungi la scroll area al layout principale
        layout.addWidget(titotlo1)
        layout.addWidget(area)
        layout.addSpacing(50)
        layout.addWidget(titotlo2)
        layout.addWidget(area1)
        layout.addStretch()

        # Imposta il layout principale
        wid.setLayout(layout)
        self.setCentralWidget(wid)

        self.set_background_color()



    def apri_parametri(self, sensor_id):
        print(f"Apertura della schermata parametri per il sensore {sensor_id}")

    def elimina_sensore(self, sensor_id):
        print(f"Eliminazione del sensore {sensor_id}")

    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)
        # Load the stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        file = QFile(f.get_style("sensori.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()

    sys.exit(app.exec())