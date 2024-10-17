from PyQt6.QtWidgets import QWidget, QVBoxLayout, QDialog, QGridLayout, QLabel, QHBoxLayout, QMessageBox
from PyQt6.QtCore import QFile, QTextStream, Qt, QSize, QRect
from PyQt6.QtGui import QColor, QFont, QPainter, QIcon

import sys

from API import funzioni as f
from API.LOG import log_file
from CMP import (
    QPushButtonBadge as q,
    QTastierino as qn,
    QDispalyNumpad as qd
)


class Tastierino(QWidget):

    def __init__(self, master, header):
        super().__init__()

        self.master = master
        self.master.setWindowTitle("ImpoPage")
        self.header = header

        self.cont_error = 0
        self.current_value = ""

        self.main_layout = QVBoxLayout()
        self.initUI()

        self.setLayout(self.main_layout)
        self.setAutoFillBackground(True)
        self.set_background_color()

        # Log interface initialization
        log_file(1, "tastierino")

    def initUI(self):
        # Label to show the number entered
        self.pin_display = qd.CirclePinDisplay(num_digits=6)
        self.main_layout.addWidget(self.pin_display)

        # Widget containing the grid layout for buttons
        wid = QWidget()
        wid.setFixedSize(500, 800)
        l = QGridLayout()

        # Create number buttons from 0-9
        self.buttons = {}
        positions = [(i, j) for i in range(4) for j in range(3)]
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'x', '0', 'v']

        for position, number in zip(positions, numbers):
            if number:
                button = qn.QPushButtonBadge(text=str(number))
                button.setFixedSize(150,150)
                button.clicked.connect(lambda checked, num=number: self.button_pressed(num))
                l.addWidget(button, *position)
                self.buttons[number] = button
        h = QHBoxLayout()
        wid.setLayout(l)

        h.addStretch()
        h.addWidget(wid)
        h.addStretch()

        self.main_layout.addStretch()
        self.main_layout.addLayout(h)
        self.main_layout.addStretch()

        # Log grid layout initialization
        log_file(3, "tastierino")

    def button_pressed(self, number):
        if len(self.current_value) < 6:  # Limite di 6 cifre
            if number == "x":
                log_file(303)
                self.current_value = ""   
            elif number == "v":
                pass
            elif len(self.current_value) == 0:
                self.current_value = number
            else:
                self.current_value += number
            self.pin_display.update_display(self.current_value)

            if len(self.current_value) == 6:
                print("disabilitazione")
                log_file(304)
                for but in self.buttons.values():
                    testo = but.text()
                    print(testo)
                    if testo != "":
                        but.setEnabled(False)
        else:
            if number == "x":
                self.current_value = ""
                for but in self.buttons.values():
                    testo = but.text()
                    print(testo)
                    if testo != "":
                        log_file(305)
                        but.setEnabled(True)
            elif number == "v":
                log_file(302)
                if self.current_value == "123457":
                    log_file(300)
                    self.master.tastierino_pass()
                else:
                    log_file(301)
                    self.cont_error += 1
                    print("conta")
                    self.current_value = ""
                    if self.cont_error > 2:  
                        log_file(403)
                        self.master.tastierino_err()
                    else:
                        self.message_error()

    def message_error(self):
        log_file(6, f"{3 - self.cont_error} tentativi rimasti")
        ico = QIcon(f.get_img("bell_orange.png"))
        titolo = f"Errore {self.cont_error}"
        desc = f"{3 - self.cont_error} tentativi rimasti"

        # Disabilita i pulsanti per evitare ulteriori interazioni
        for button in self.buttons.values():
            button.setEnabled(False)

        errore = QMessageBox(self)
        errore.setWindowTitle(titolo)
        errore.setText(desc)
        errore.setIcon(QMessageBox.Icon.Warning)
        errore.setStandardButtons(QMessageBox.StandardButton.Ok)
        errore.setWindowIcon(ico)

        # Connetti il segnale al metodo per gestire l'azione dopo la chiusura
        errore.buttonClicked.connect(self.handle_messagebox_click)

        errore.exec()

    def handle_messagebox_click(self, button):
        log_file(305)
        # Riabilita i pulsanti dopo la chiusura del QMessageBox
        for button in self.buttons.values():
            button.setEnabled(True)

        # Reset il valore corrente dopo la chiusura del QMessageBox
        self.current_value = ""
        self.pin_display.update_display(self.current_value)

    def set_background_color(self):
        log_file(4, "tastierino")
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)
        # Load the stylesheet
        self.load_stylesheet()

    def reset_ui(self):
        log_file(2, "tastierino")
        # Reset il valore corrente
        self.current_value = ""
        self.cont_error = 0
        # Reset il display
        self.pin_display.update_display(self.current_value)

        # Abilita tutti i pulsanti
        for button in self.buttons.values():
            button.setEnabled(True)

    def load_stylesheet(self):
        log_file(5, "tastierino")
        file = QFile(f.get_style("tastierino.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)