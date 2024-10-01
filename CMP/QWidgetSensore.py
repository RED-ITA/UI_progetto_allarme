import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton, QHBoxLayout,QLabel
from PyQt6.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt6.QtCore import QRect, Qt, QTimer, QFile, QTextStream, pyqtSignal

from API import funzioni as f
from OBJ import OBJ_UI_Sensore as sensore
from CMP import QPushButtonNoBadge as p


class QWidgetSensore(QWidget):
    """
        |-------------------|
        |      SENSORI      |
        |-------------------|
        |  SensorPk         |    INTEGER (Primary Key, AUTOINCREMENT)  -- Unique identifier for each sensor
        |  Id               |    INTEGER  -- Modbus line ID, not unique
        |  Tipo             |    INTEGER  -- Type of sensor: 0 = motion, 1 = magnetic, 2 = vibration
        |  Data             |    TEXT     -- Date when the sensor was added
        |  Stanza           |    TEXT     -- Room name where the sensor is located
        |  Soglia           |    INTEGER  -- Threshold value for triggering the sensor
        |  Error            |    INTEGER  -- Error status: 0 = no error, 1 = error
        |  Stato            |    INTEGER  -- Sensor status: 1 = Active, 0 = Inactive
        |-------------------|
    """
    signal_parametri = pyqtSignal()
    signal_cestino = pyqtSignal()

    def __init__(self, obj:sensore.Sensore, parent=None):
        super().__init__()
        self.oggetto = obj
        self.layout1 = QVBoxLayout()
        self.setFixedSize(300,300)

        if obj.Tipo == 0: 
            nome="movimento"
            if obj.Stato: 
                immagine = "movimento.png"
            else: 
                immagine = "movimento.red.png"
        elif obj.Tipo == 1: 
            nome="contatto"
            if obj.Stato: 
                immagine = "contatto.png"
            else: 
                immagine = "contatto.red.png"
        elif obj.Tipo == 2: 
            nome="vibrazione"
            if obj.Stato: 
                immagine = "vibrazione.png"
            else: 
                immagine = "vibrazione.red.png"

        h0 = QHBoxLayout()
        logo_label = QLabel()
        logo_label.setObjectName("img")
        ico = f.get_img(immagine)
        larghezza = int(260)
        altezza = int(140)
        logo_label.setPixmap(QPixmap(ico).scaled(larghezza, altezza, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        h0.addStretch()
        h0.addWidget(logo_label)
        h0.addStretch()

        
        h1 = QHBoxLayout()
        titolo_label=QLabel(nome)
        titolo_label.setObjectName("titolo")

        h1.addStretch()
        h1.addWidget(titolo_label)
        h1.addStretch()
        
        self.layout1.addLayout(h0)
        self.layout1.addLayout(h1)
        
        if obj.Stato:
            h2 = QHBoxLayout()
            self.p1 = p.QPushButtonBadge("parametri.png", color="DEDEDE")
            self.p1.setFixedSize(75,75)
            self.p2 = p.QPushButtonBadge("cestino.png", color="DEDEDE")
            self.p2.setFixedSize(75,75)

             # Connetti i pulsanti ai segnali
            self.p1.clicked.connect(self.emit_parametri_signal)
            self.p2.clicked.connect(self.emit_cestino_signal)

            h2.addSpacing(10)
            h2.addWidget(self.p1)
            h2.addStretch()
            h2.addWidget(self.p2)
            h2.addSpacing(10)
        
            self.layout1.addLayout(h2)

        wid = QWidget()
        wid.setLayout(self.layout1)
        wid.setObjectName("sensore")

        laa = QHBoxLayout()
        laa.setContentsMargins(0,0,0,0)
        laa.setSpacing(0)

        laa.addWidget(wid)
        self.setLayout(laa)

        self.setAutoFillBackground(True)
        #self.set_background_color()
        # Load the stylesheet
        self.load_stylesheet()
        

    # Metodo per emettere il segnale quando viene premuto il pulsante 'parametri'
    def emit_parametri_signal(self):
        print(f"premuto parametri del sensore {self.oggetto.Id}")
        self.signal_parametri.emit()

    # Metodo per emettere il segnale quando viene premuto il pulsante 'cestino'
    def emit_cestino_signal(self):
        print(f"premuto elimina del sensore {self.oggetto.Id}")
        self.signal_cestino.emit()

    def set_background_color(self):
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor.fromRgb(222, 222, 222))
        self.setPalette(p)
        self.repaint()
        

    def load_stylesheet(self):
        qss_file = f.get_style("sensore.qss")
        if not QFile.exists(qss_file):
            print(f"File {qss_file} not found.")
            return
        file = QFile(qss_file)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            style_sheet = stream.readAll()
            file.close()
            self.setStyleSheet(style_sheet)
            print("Stylesheet applied successfully.")
        else:
            print("Failed to open stylesheet.")

