from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt, QRectF

class SvgLabel(QLabel):
    def __init__(self, svg_file, parent=None):
        super().__init__(parent)
        self.renderer = QSvgRenderer(svg_file)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def paintEvent(self, event):
        painter = QPainter(self)
        size = self.size()
        # Calcola la dimensione mantenendo il rapporto d'aspetto
        svg_size = self.renderer.defaultSize()
        svg_aspect = svg_size.width() / svg_size.height()
        widget_aspect = size.width() / size.height()

        if widget_aspect > svg_aspect:
            # Widget più largo, limita l'altezza
            new_height = size.height()
            new_width = int(new_height * svg_aspect)
        else:
            # Widget più alto, limita la larghezza
            new_width = size.width()
            new_height = int(new_width / svg_aspect)

        x = (size.width() - new_width) / 2
        y = (size.height() - new_height) / 2

        target_rect = QRectF(int(x), int(y), new_width, new_height)
        self.renderer.render(painter, target_rect)