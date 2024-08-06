import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt6.QtCore import QRect, Qt, QTimer

from API import funzioni as f

class QPushButtonBadge(QPushButton):
    """classe estende button 


    funzionamento:

        self.button = BadgeButton("calendar.png", None, self, "000000")     #crea senza badge
        self.button.setFixedSize(400, 400)                                  #csetta le dimensioni 
        
       
        self.button.setBadgeText("1")                              #agginge il bedge con 1
        self.button.removeBadge()                                   #rimuove il bedge

    """
    def __init__(self, image_path=None, badge_text=None, parent=None, color="f1f1f1"):
        super().__init__("", parent)
        self.badge_text = badge_text
        self.image_path = f.get_img(image_path)
        self.icon = None
        if image_path:
            self.setButtonImage(image_path)
        self.initStylesheet(color)

    def initStylesheet(self, color):
        self.setStyleSheet("""
            QPushButton {
                background-color: #""" + color +""";
                border: none;
            }
            
        """)

    #private
    def setButtonImage(self, image_path):
        self.image_path = image_path
        self.icon = QIcon(image_path)
        self.updateIconSize()

    #private
    
    def updateIconSize(self):
        if self.icon:
            self.setIcon(self.icon)
            self.setIconSize(self.size())

    #private
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateIconSize()

    def setBadgeText(self, new_text):
        """setta il valore del bedge

        Args:
            new_text (str): appare nel tondo rosso
        """        
        self.badge_text = new_text
        self.update()  # Questo forza il ridisegno del pulsante

    def removeBadge(self):
        """rimuove il badge
        """        
        self.badge_text = None
        self.update()  # Questo forza il ridisegno del pulsante

    def getBedgeValue(self):
        """restituisce il valore del badge

        Returns:
            str: bedge text
        """        
        return self.badge_text

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.badge_text:
            rect = self.rect()
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Draw badge background
            badge_size = min(rect.width(), rect.height()) // 4  # Badge size proportional to the button size
            badge_rect = QRect(rect.right() - badge_size, rect.top(), badge_size, badge_size)
            painter.setBrush(QColor(255, 0, 0))
            painter.setPen(Qt.GlobalColor.transparent)
            painter.drawEllipse(badge_rect)
            
            # Draw badge text
            painter.setPen(QColor(255, 255, 255))
            font = painter.font()
            font.setBold(True)
            font.setPointSize(badge_size // 2)  # Font size proportional to badge size
            painter.setFont(font)
            painter.drawText(badge_rect, Qt.AlignmentFlag.AlignCenter, self.badge_text)


