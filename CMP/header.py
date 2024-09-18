from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QMainWindow, QApplication, QLabel
from PyQt6.QtCore import QFile, QTextStream, QSize, Qt, QTimer, QTime, QDate
from PyQt6.QtGui import QColor, QPalette

import sys

from API import funzioni as f
from CMP import QPushButtonBadge as q


class Header(QWidget):
    def __init__(self, master):
        """header

        Args:
            master (classe regina): main.py
            
        """     
        
        super().__init__()   
        self.prima_riga = QHBoxLayout()
        self.master = master
        
        self.setup_timer()
        self.home()
        self.setLayout(self.prima_riga)

        self.setAutoFillBackground(True)
        self.set_background_color()
        
    def resizeEvent(self, event):
        # Update icon size when application window size changes
        self.update_icon_size()
        super().resizeEvent(event)

    def update_icon_size(self):
        
        size_ico = int(self.get_icon_size() / 1.5)
        for button in [self.sos, self.home_button]:
            button.setFixedSize(size_ico, size_ico)

    def setup_timer(self):
        # Create a QTimer to update the time every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # Update every 1000 milliseconds (1 second)

    def update_time(self):
        # Get the current time and set it to the QLabel
        current_time = QTime.currentTime().toString("HH:mm")
        current_date = QDate.currentDate().toString("dddd d MMMM")
    
        try:
            self.ora.setText(current_time)
            self.data.setText(current_date)
        except Exception:
            pass
        

    def set_tipo(self, tipo):
        print(f"dioporco {tipo}")
        """set modello

        Args:
            tipo (int): 0 :home page header
                        1 :impostazioni page header
        """        
        self.clearLayout(self.prima_riga)

        if tipo == 0:
            self.home()
        elif tipo == 1:
            self.impostazioni()
        elif tipo == 2:
            self.sensori()
        elif tipo == 3:
            self.stanze()

        

    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(241, 241, 241))
        self.setPalette(p)
        # Load the stylesheet
        self.load_stylesheet()

    def load_stylesheet(self):
        file = QFile(f.get_style("header.qss"))
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)

    def home(self):
        size_ico = int(self.get_icon_size() / 1.8)

        # Navigation bar
        self.sos = q.QPushButtonBadge("sos.png")
        self.sos.clicked.connect(self.sos_f)
        self.sos.setFixedSize(size_ico, size_ico)
        # Ora
        v = QVBoxLayout()
        self.data = QLabel("Giorno N Mese")
        self.data.setObjectName("data")
        self.data.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Time label that will be updated
        self.ora = QLabel("HH : MM")
        self.ora.setObjectName("ora")
        self.ora.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(self.data)
        v.addWidget(self.ora)

        self.layout_pagina = QHBoxLayout()
        self.home_button = q.QPushButtonBadge("home.png")
        self.home_button.setFixedSize(size_ico, size_ico)
        self.layout_pagina.setSpacing(0)
        self.layout_pagina.addWidget(self.home_button)

        self.prima_riga.addSpacing(self.get_icon_size())
        self.prima_riga.addWidget(self.sos)
        self.prima_riga.addStretch()
        self.prima_riga.addLayout(v)
        self.prima_riga.addStretch()
        self.prima_riga.addLayout(self.layout_pagina)
        self.prima_riga.addSpacing(self.get_icon_size())
        self.update_time()


    def impostazioni(self):
        size_ico = int(self.get_icon_size() / 1.8)

        # Navigation bar
        self.sos = q.QPushButtonBadge("go_back.png")
        self.sos.clicked.connect(self.back)
        self.sos.setFixedSize(size_ico, size_ico)
        # Ora
        v = QVBoxLayout()
        pag = QLabel("pagina")
        pag.setObjectName("data")
        pag.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Time label that will be updated
        nome = QLabel("IMPOSTAZIONI")
        nome.setObjectName("ora")
        nome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(pag)
        v.addWidget(nome)

        self.layout_pagina = QHBoxLayout()
        self.home_button = q.QPushButtonBadge("settings.png")
        self.home_button.setFixedSize(size_ico, size_ico)
        self.layout_pagina.setSpacing(0)
        self.layout_pagina.addWidget(self.home_button)

        self.prima_riga.addSpacing(self.get_icon_size())
        self.prima_riga.addWidget(self.sos)
        self.prima_riga.addStretch()
        self.prima_riga.addLayout(v)
        self.prima_riga.addStretch()
        self.prima_riga.addLayout(self.layout_pagina)
        self.prima_riga.addSpacing(self.get_icon_size())
        #self.update_time()

    def sensori(self):
        size_ico = int(self.get_icon_size() / 1.8)

        # Navigation bar
        self.sos = q.QPushButtonBadge("go_back.png")
        self.sos.clicked.connect(self.back)
        self.sos.setFixedSize(size_ico, size_ico)
        # Ora
        v = QVBoxLayout()
        pag = QLabel("pagina")
        pag.setObjectName("data")
        pag.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Time label that will be updated
        nome = QLabel("SENSORI")
        nome.setObjectName("ora")
        nome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(pag)
        v.addWidget(nome)

        self.layout_pagina = QHBoxLayout()
        self.home_button = q.QPushButtonBadge("eye.png")
        self.home_button.setFixedSize(size_ico, size_ico)
        self.layout_pagina.setSpacing(0)
        self.layout_pagina.addWidget(self.home_button)

        self.prima_riga.addSpacing(self.get_icon_size())
        self.prima_riga.addWidget(self.sos)
        self.prima_riga.addStretch()
        self.prima_riga.addLayout(v)
        self.prima_riga.addStretch()
        self.prima_riga.addLayout(self.layout_pagina)
        self.prima_riga.addSpacing(self.get_icon_size())
        self.update_time()

    def stanze(self):
        size_ico = int(self.get_icon_size() / 1.8)

        # Navigation bar
        self.sos = q.QPushButtonBadge("go_back.png")
        self.sos.clicked.connect(self.back)
        self.sos.setFixedSize(size_ico, size_ico)
        
        # Ora
        v = QVBoxLayout()
        pag = QLabel("pagina")
        pag.setObjectName("data")
        pag.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Time label that will be updated
        nome = QLabel("STANZE")
        nome.setObjectName("ora")
        nome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        v.addWidget(pag)
        v.addWidget(nome)

        self.layout_pagina = QHBoxLayout()
        self.home_button = q.QPushButtonBadge("rooms.png")
        self.home_button.setFixedSize(size_ico, size_ico)
        self.layout_pagina.setSpacing(0)
        self.layout_pagina.addWidget(self.home_button)

        self.prima_riga.addSpacing(self.get_icon_size())
        self.prima_riga.addWidget(self.sos)
        self.prima_riga.addStretch()
        self.prima_riga.addLayout(v)

        self.prima_riga.addStretch()
        self.prima_riga.addLayout(self.layout_pagina)
        self.prima_riga.addSpacing(self.get_icon_size())
        #self.update_time()

    def sos_f(self):
        print("SOS")

    def back(self):
        self.master.change_page(0)


    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def get_icon_size(self):
        # Calculate icon size based on application window width
        return int(self.master.width() * 0.1)