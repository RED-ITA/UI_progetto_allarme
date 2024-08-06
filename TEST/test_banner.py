import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMainWindow
from PyQt6.QtGui import QPainter, QColor, QFont
from PyQt6.QtCore import QRect, Qt, QTimer

class BadgeButton(QPushButton):
    def __init__(self, text, badge_text=None, parent=None):
        super().__init__(text, parent)
        self.badge_text = badge_text

    def setBadgeText(self, new_text):
        self.badge_text = new_text
        self.update()  # Questo forza il ridisegno del pulsante

    def removeBadge(self):
        self.badge_text = None
        self.update()  # Questo forza il ridisegno del pulsante

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.badge_text:
            rect = self.rect()
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Draw badge background
            badge_rect = QRect(rect.right() - 30, rect.top(), 20, 20)
            painter.setBrush(QColor(255, 0, 0))
            painter.setPen(Qt.GlobalColor.transparent)
            painter.drawEllipse(badge_rect)
            
            # Draw badge text
            painter.setPen(QColor(255, 255, 255))
            font = QFont()
            font.setBold(True)
            painter.setFont(font)
            painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, self.badge_text)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Badge Button Example")
        self.setGeometry(100, 100, 300, 200)
        self.initUI()

    def initUI(self):
        wid = QWidget()

        l = QVBoxLayout(wid)
        self.button = BadgeButton("Home", None, self)
        self.button.setGeometry(50, 50, 200, 100)
        l.addWidget(self.button)

        self.setCentralWidget(wid)

        # Aggiungi il numero del badge dopo 3 secondi
        QTimer.singleShot(3000, self.addBadge)

    def addBadge(self):
        self.button.setBadgeText("1")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
