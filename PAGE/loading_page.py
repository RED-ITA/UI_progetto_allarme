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
                }}
                .container {{
                    position: absolute;
                    top: 50%;
                    left: 50%;
                    transform: translate(-50%, -50%);
                }}
                .loader {{
                  --c1:#673b14;
                  --c2:#f8b13b;
                  width: 40px;
                  height: 80px;
                  border-top: 4px solid var(--c1);
                  border-bottom: 4px solid var(--c1);
                  background: linear-gradient(90deg, var(--c1) 2px, var(--c2) 0 5px,var(--c1) 0) 50%/7px 8px no-repeat;
                  display: grid;
                  overflow: hidden;
                  animation: l5-0 2s infinite linear;
                }}
                .loader::before,
                .loader::after {{
                  content: "";
                  grid-area: 1/1;
                  width: 75%;
                  height: calc(50% - 4px);
                  margin: 0 auto;
                  border: 2px solid var(--c1);
                  border-top: 0;
                  box-sizing: content-box;
                  border-radius: 0 0 40% 40%;
                  -webkit-mask: 
                    linear-gradient(#000 0 0) bottom/4px 2px no-repeat,
                    linear-gradient(#000 0 0);
                  -webkit-mask-composite: destination-out;
                          mask-composite: exclude;
                  background: 
                    linear-gradient(var(--d,0deg),var(--c2) 50%,#0000 0) bottom /100% 205%,
                    linear-gradient(var(--c2) 0 0) center/0 100%;
                  background-repeat: no-repeat;
                  animation: inherit;
                  animation-name: l5-1;
                }}
                .loader::after {{
                  transform-origin: 50% calc(100% + 2px);
                  transform: scaleY(-1);
                  --s:3px;
                  --d:180deg;
                }}
                @keyframes l5-0 {{
                  80%  {{transform: rotate(0)}}
                  100% {{transform: rotate(0.5turn)}}
                }}
                @keyframes l5-1 {{
                  10%,70%  {{background-size:100% 205%,var(--s,0) 100%}}
                  70%,100% {{background-position: top,center}}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="loader"></div>
            </div>
        </body>
        </html>
        """

        self.web_view.setHtml(svg_html)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.web_view, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)