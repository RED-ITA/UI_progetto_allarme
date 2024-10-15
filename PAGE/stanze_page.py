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

class Stanze_Page(QWidget):

    signal_sensor_clicked = pyqtSignal(int)

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
        log_file(1, "stanze")

        # Scroll area a sinistra con le stanze disponibili
        self.area_stanze = QScrollArea()
        self.area_stanze.setMaximumWidth(300)
        self.area_stanze.setWidgetResizable(True)
        self.scroll_content_stanze = QWidget()
        self.scroll_content_stanze.setObjectName("wid")
        self.v_layout_stanze = QVBoxLayout(self.scroll_content_stanze)
        self.v_layout_stanze.setContentsMargins(10, 10, 10, 10)
        self.area_stanze.setWidget(self.scroll_content_stanze)
        self.main_layout.addWidget(self.area_stanze)

        # Aggiunge le stanze alla scroll area
        self.populate_stanze()

        # Area per i sensori attivi della stanza selezionata
        self.scroll_content_sensori = QWidget()
        self.scroll_content_sensori.setObjectName("wid")
        self.h_layout_sensori = QVBoxLayout(self.scroll_content_sensori)
        self.h_layout_sensori.setContentsMargins(10, 10, 10, 10)
        self.area_sensori = QScrollArea()
        
        self.area_sensori.setWidgetResizable(True)
        self.area_sensori.setWidget(self.scroll_content_sensori)
        self.main_layout.addWidget(self.area_sensori)

    def populate_stanze(self):
        log_file(200, "stanze")
        self.clear_layout(self.v_layout_stanze)

        # Pulsante per aggiungere una nuova stanza
        self.add_stanza_button = qn.QPushButtonBadge(f.get_img("plus.png")) 
        self.add_stanza_button.setFixedSize(51,50)
        self.add_stanza_button.clicked.connect(self.on_add_stanza_clicked)
        self.v_layout_stanze.addWidget(self.add_stanza_button)
        self.v_layout_stanze.addSpacing(50)

        self.buttons = {}

        stanze_data = db_api.get_all_stanze()
        for stanza in stanze_data:
            button = QPushButton(stanza[0])
            button.setObjectName("stanza_button")
            button.setStyleSheet("text-align: left;")

            pixmap = QPixmap(f.get_img("stanza_nosel"))
            icon = QIcon(pixmap)
            button.setIcon(icon)

            button.clicked.connect(lambda checked, nome=stanza[0]: self.on_stanza_clicked(nome))
            self.v_layout_stanze.addWidget(button)
            self.buttons[stanza[0]] = button
        self.v_layout_stanze.addStretch()

    def on_stanza_clicked(self, stanza_nome):
        log_file(201, f"{stanza_nome}")

        for nome, button in self.buttons.items():
            button.setProperty("selected", False)
            button.style().unpolish(button)
            button.style().polish(button)

            pixmap = QPixmap(f.get_img("stanza_nosel"))
            icon = QIcon(pixmap)
            button.setIcon(icon)

        sender = self.buttons[stanza_nome]
        sender.setProperty("selected", True)
        sender.style().unpolish(sender)
        sender.style().polish(sender)

        selected_pixmap = QPixmap(f.get_img("stanza_sel"))
        selected_icon = QIcon(selected_pixmap)
        sender.setIcon(selected_icon)

        self.populate_sensori(stanza_nome)

    def populate_sensori(self, stanza_nome):
        log_file(202, f"{stanza_nome}")
        self.clear_layout(self.h_layout_sensori)
        sensori_stanza = db_api.get_sensori_by_stanza(stanza_nome)

        riga_superiore_layout = QHBoxLayout()
        riga_inferiore_layout = QHBoxLayout()
        self.h_layout_sensori.addLayout(riga_superiore_layout)
        self.h_layout_sensori.addLayout(riga_inferiore_layout)

        for index, sensor_data in enumerate(sensori_stanza):
            riga_layout = riga_superiore_layout if index % 2 == 0 else riga_inferiore_layout
            sensore = o.Sensore(
                SensorePk=sensor_data[0],
                Id=sensor_data[1],
                Tipo=sensor_data[2],
                Data=sensor_data[3],
                Stanza=sensor_data[4],
                Soglia=sensor_data[5],
                Error=sensor_data[6],
                Stato=sensor_data[7]
            )
            sensore_widget = w.QWidgetSensore(sensore)
            sensore_widget.setObjectName("sensore")
            sensore_widget.signal_parametri.connect(self.on_sensor_clicked)
            riga_layout.addWidget(sensore_widget)

        riga_superiore_layout.addStretch()
        riga_inferiore_layout.addStretch()

    def on_sensor_clicked(self, sensor_pk):
        log_file(203, f"{sensor_pk}")
        self.signal_sensor_clicked.emit(sensor_pk)

    def on_add_stanza_clicked(self):
        log_file(203, "Pulsante 'Aggiungi Stanza' cliccato")
        self.create_new_stanza()

    def create_new_stanza(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Crea Nuova Stanza")
        dialog_layout = QVBoxLayout()

        self.nome_stanza_input = QLineEdit()
        self.nome_stanza_input.setPlaceholderText("Nome della nuova stanza")
        dialog_layout.addWidget(self.nome_stanza_input)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(lambda: self.on_confirm_add_stanza(dialog))
        buttons.rejected.connect(dialog.reject)
        dialog_layout.addWidget(buttons)

        dialog.setLayout(dialog_layout)
        dialog.exec()

    def on_confirm_add_stanza(self, dialog):
        nome_stanza = self.nome_stanza_input.text().strip()
        if nome_stanza:
            log_file(204, f"{nome_stanza}")
            result = db_api.add_stanza(nome_stanza)
            if result:
                log_file(2104, f"{nome_stanza}")
                self.populate_stanze()
            else:
                log_file(402, f"{nome_stanza}")
        dialog.accept()

    def clear_layout(self, layout):
        log_file(2, "stanze")
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

    def set_background_color(self):
        log_file(4, "stanze")
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)
        self.load_stylesheet()

    def load_stylesheet(self):
        log_file(5, "stanze")
        file = QFile(f.get_style("stanze.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)