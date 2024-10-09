from PyQt6.QtWidgets import QWidget, QVBoxLayout, QDialog, QGridLayout, QLabel
from PyQt6.QtCore import QFile, QTextStream, Qt
from PyQt6.QtGui import QColor

import sys

from API import funzioni as f
from CMP import (
    QPushButtonBadge as q,
    QPushButtonNoBadge as qn
)


class Tastierino(QDialog):

    def __init__(self, master, header):
        super().__init__()

        self.master = master
        self.master.setWindowTitle("ImpoPage")
        self.header = header

        self.current_value = ""

        self.main_layout = QVBoxLayout()
        self.initUI()

        self.setLayout(self.main_layout)
        self.setAutoFillBackground(True)
        self.set_background_color()

    def initUI(self):
        # Label to show the number entered
        self.display_label = QLabel("0")
        self.display_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display_label.setStyleSheet("font-size: 24px; padding: 10px;")
        self.main_layout.addWidget(self.display_label)

        # Widget containing the grid layout for buttons
        wid = QWidget()
        l = QGridLayout()

        # Create number buttons from 0-9
        self.buttons = {}
        positions = [(i, j) for i in range(4) for j in range(3)]
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '', '0', '']

        for position, number in zip(positions, numbers):
            if number:
                button = qn.QPushButtonBadge(f.get_img(f"{number}.png"))
                button.setFixedSize(50,50)
                button.clicked.connect(lambda checked, num=number: self.button_pressed(num))
                l.addWidget(button, *position)
                self.buttons[number] = button

        wid.setLayout(l)
        self.main_layout.addWidget(wid)
        self.main_layout.addStretch()

    def button_pressed(self, number):
        if self.current_value == "0":
            self.current_value = number
        else:
            self.current_value += number
        self.display_label.setText(self.current_value)

    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)
        # Load the stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        file = QFile(f.get_style("impo.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)