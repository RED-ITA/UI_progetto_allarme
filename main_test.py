from PyQt6.QtGui import  QColor
from PyQt6.QtCore import Qt, pyqtSignal
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
        
        layout = QVBoxLayout()
        wid = QWidget()
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

        # Creazione della QScrollArea
        area = QScrollArea()
        area.setFixedHeight(350)
        area.setFixedWidth(600)
        area.setWidgetResizable(True)  # Permette il ridimensionamento del widget

        # Widget interno che conterrà il layout orizzontale
        scroll_content = QWidget()
        h0 = QHBoxLayout(scroll_content)
        h0.addSpacing(30)

        # Aggiunta degli oggetti alla scroll area
        for oggetto in lista: 
            UI_og = w.QWidgetSensore(oggetto)
            h0.addWidget(UI_og)
            h0.addSpacing(30)

        # Aggiunge un'espansione alla fine
        h0.addStretch()

        # Imposta il widget contenitore all'interno della scroll area
        area.setWidget(scroll_content)

        # Aggiungi la scroll area al layout principale
        layout.addWidget(area)
        layout.addStretch()

        # Imposta il layout principale
        wid.setLayout(layout)
        self.setCentralWidget(wid)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindows()
    window.show()

    sys.exit(app.exec())