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

        # Layout principale
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.wid = QWidget()
        self.wid.setContentsMargins(0, 0, 0, 0)

        # Lista sensori
        self.lista = self.crea_lista_sensori()

        # Scroll area per sensori attivi e disattivi
        self.area_attivi = QScrollArea()
        self.area_disattivi = QScrollArea()

        self.area_attivi.setContentsMargins(0, 0, 0, 0)
        self.area_attivi.setFixedHeight(350)
        self.area_attivi.setFixedWidth(self.screen_width)
        self.area_attivi.setWidgetResizable(True)

        self.area_disattivi.setContentsMargins(0, 0, 0, 0)
        self.area_disattivi.setFixedHeight(350)
        self.area_disattivi.setFixedWidth(self.screen_width)
        self.area_disattivi.setWidgetResizable(True)

        # Label per i titoli
        self.titolo_attivi = QLabel("Sensori Attivi")
        self.titolo_attivi.setObjectName("titolo")
        self.titolo_disattivi = QLabel("Sensori Disattivi")
        self.titolo_disattivi.setObjectName("titolo")

        # Popolamento iniziale dei sensori
        self.rigenera_interfaccia()

        # Aggiungi la scroll area al layout principale
        self.layout.addWidget(self.titolo_attivi)
        self.layout.addWidget(self.area_attivi)
        self.layout.addSpacing(50)
        self.layout.addWidget(self.titolo_disattivi)
        self.layout.addWidget(self.area_disattivi)
        self.layout.addStretch()

        # Imposta il layout principale
        self.wid.setLayout(self.layout)
        self.setCentralWidget(self.wid)

        self.set_background_color()

    def crea_lista_sensori(self):
        # Crea una lista di sensori
        lista = []
        # Creazione degli oggetti Sensore
        oggetto0 = o.Sensore(0, 1, 0, "23/13/12", "cucina", 0, 0, 1)
        lista.append(oggetto0)
        oggetto1 = o.Sensore(0, 2, 0, "23/13/12", "cucina", 0, 0, 0)
        lista.append(oggetto1)
        oggetto2 = o.Sensore(0, 3, 1, "23/13/12", "cucina", 0, 0, 1)
        lista.append(oggetto2)
        oggetto3 = o.Sensore(0, 4, 1, "23/13/12", "cucina", 0, 0, 1)
        lista.append(oggetto3)
        oggetto4 = o.Sensore(0, 5, 2, "23/13/12", "cucina", 0, 0, 1)
        lista.append(oggetto4)
        oggetto5 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 1)
        lista.append(oggetto5)
        oggetto6 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 1)
        lista.append(oggetto6)
        oggetto7 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 1)
        lista.append(oggetto7)
        oggetto8 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 1)
        lista.append(oggetto8)
        oggetto9 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 1)
        lista.append(oggetto9)
        oggetto10 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 0)
        lista.append(oggetto10)
        oggetto11 = o.Sensore(0, 6, 2, "23/13/12", "cucina", 0, 0, 0)
        lista.append(oggetto11)

        # Aggiungi tutti i sensori
        return lista

    def rigenera_interfaccia(self):
        """
        Ricostruisce l'interfaccia popolando le due aree (attivi e disattivi).
        """
        # Rimuovi tutti i widget dalle aree di scorrimento
        for i in reversed(range(self.area_attivi.layout().count())):
            widget_to_remove = self.area_attivi.layout().itemAt(i).widget()
            self.area_attivi.layout().removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        for i in reversed(range(self.area_disattivi.layout().count())):
            widget_to_remove = self.area_disattivi.layout().itemAt(i).widget()
            self.area_disattivi.layout().removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        # Layout per sensori attivi
        scroll_content_attivi = QWidget()
        h0 = QHBoxLayout(scroll_content_attivi)
        h0.addSpacing(30)

        # Layout per sensori disattivi
        scroll_content_disattivi = QWidget()
        h1 = QHBoxLayout(scroll_content_disattivi)
        h1.addSpacing(30)

        # Aggiunta degli oggetti alla scroll area
        for oggetto in self.lista:
            UI_og = w.QWidgetSensore(oggetto)
            UI_og.setObjectName("sensore")
            UI_og.signal_parametri.connect(self.apri_parametri)
            UI_og.signal_cestino.connect(self.elimina_sensore)
            
            if oggetto.Stato:  # Sensore attivo
                h0.addWidget(UI_og)
                h0.addSpacing(30)
            else:  # Sensore disattivo
                h1.addWidget(UI_og)
                h1.addSpacing(30)

        # Aggiungi le espansioni finali
        h0.addStretch()
        h1.addStretch()

        # Imposta il widget contenitore all'interno delle scroll area
        self.area_attivi.setWidget(scroll_content_attivi)
        self.area_disattivi.setWidget(scroll_content_disattivi)

    def apri_parametri(self, sensor_id):
        print(f"Apertura della schermata parametri per il sensore {sensor_id}")

    def elimina_sensore(self, sensor_id):
        """
        Elimina il sensore impostandolo come disattivato e rigenera l'interfaccia.
        """
        print(f"Eliminazione del sensore {sensor_id}")
        for sensore in self.lista:
            if sensore.Id == sensor_id:
                sensore.Stato = False  # Imposta lo stato del sensore a False
                break
        
        # Rigenera l'interfaccia
        self.rigenera_interfaccia()

    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)

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