from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QColor, QPainter



class CirclePinDisplay(QWidget):
    def __init__(self, num_digits=6):
        super().__init__()
        self.num_digits = num_digits
        self.entered_digits = []
        
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        # Create placeholders for the circles
        self.circles = []
        for _ in range(self.num_digits):
            circle = CircleWidget()
            self.circles.append(circle)
            self.layout.addWidget(circle)

    def update_display(self, value):
        self.entered_digits = list(value)
        for i in range(self.num_digits):
            if i < len(self.entered_digits):
                self.circles[i].set_digit(self.entered_digits[i])
            else:
                self.circles[i].set_digit(None)

class CircleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.digit = None
        self.setFixedSize(QSize(65, 65))

    def set_digit(self, digit):
        self.digit = digit
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRect(10,10,50, 50)
        # Draw the circle outline with a thicker pen
        painter.setBrush(Qt.BrushStyle.NoBrush)
        pen = painter.pen()
        pen.setColor(QColor(200, 200, 200))  # Light grey for empty circles
        pen.setWidth(5)  # Thicker outline
        painter.setPen(pen)
        
        painter.drawEllipse(rect)

        # Fill the circle if a digit is present
        if self.digit is not None:
            painter.setBrush(QColor(200, 200, 200))  # Black for filled circles
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(rect)
