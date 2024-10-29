import sys
import time
from PyQt6.QtCore import Qt, QRunnable, QThreadPool, pyqtSignal, QObject, QTimer
from PyQt6.QtGui import QMovie
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtSvgWidgets import QSvgWidget

from API import funzioni as f

from PyQt6.QtWebEngineWidgets import QWebEngineView



class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)


class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()

        # QWebEngineView per visualizzare l'animazione SVG
        self.web_view = QWebEngineView()

        # Rendi la WebEngineView con lo sfondo specifico
        self.web_view.setStyleSheet("background: rgb(241, 241, 241);")

        # Leggi il contenuto SVG e imposta lo sfondo del contenuto come desiderato
        with open(f.get_img("loading.svg"), "r") as svg_file:
            svg_content = svg_file.read()
        
        # Inietta un CSS che imposta il background come il colore desiderato nell'SVG caricato
        svg_html = f"""
        <html>
        <head>
            <style>
  body {{
    margin: 0;
    background: rgb(241, 241, 241);
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }}

  .spinner {{
    position: relative;
  }}

  .spinner div {{
    width: 10px;
    height: 30px;
    background: #444444;
    position: absolute;
    left: 50%;
    top: 50%;
    opacity: 0;
    border-radius: 50px;
    box-shadow: 0 0 3px rgba(0,0,0,0.2);
    animation: fade 1s linear infinite;
    transform-origin: center -40px;
  }}

  @keyframes fade {{
    from {{ opacity: 1; }}
    to {{ opacity: 0.25; }}
  }}

  .spinner div.bar1 {{ transform: rotate(0deg); animation-delay: 0s; }}
  .spinner div.bar2 {{ transform: rotate(30deg); animation-delay: -0.9167s; }}
  .spinner div.bar3 {{ transform: rotate(60deg); animation-delay: -0.833s; }}
  .spinner div.bar4 {{ transform: rotate(90deg); animation-delay: -0.7497s; }}
  .spinner div.bar5 {{ transform: rotate(120deg); animation-delay: -0.667s; }}
  .spinner div.bar6 {{ transform: rotate(150deg); animation-delay: -0.5837s; }}
  .spinner div.bar7 {{ transform: rotate(180deg); animation-delay: -0.5s; }}
  .spinner div.bar8 {{ transform: rotate(210deg); animation-delay: -0.4167s; }}
  .spinner div.bar9 {{ transform: rotate(240deg); animation-delay: -0.333s; }}
  .spinner div.bar10 {{ transform: rotate(270deg); animation-delay: -0.2497s; }}
  .spinner div.bar11 {{ transform: rotate(300deg); animation-delay: -0.167s; }}
  .spinner div.bar12 {{ transform: rotate(330deg); animation-delay: -0.0833s; }}
</style>

        </head>
        <body>
            <div class="spinner">
              <div class="bar1"></div>
              <div class="bar2"></div>
              <div class="bar3"></div>
              <div class="bar4"></div>
              <div class="bar5"></div>
              <div class="bar6"></div>
              <div class="bar7"></div>
              <div class="bar8"></div>
              <div class="bar9"></div>
              <div class="bar10"></div>
              <div class="bar11"></div>
              <div class="bar12"></div>
            </div>
        </body>
        </html>
        """

        self.web_view.setHtml(svg_html)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.web_view, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)


        