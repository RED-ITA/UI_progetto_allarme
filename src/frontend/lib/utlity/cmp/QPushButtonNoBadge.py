import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt6.QtCore import QRect, Qt, QTimer

from API import funzioni as f

class QPushButtonBadge(QPushButton):
    """classe estende button 


    funzionamento:

        self.button = QPushButtonBadge("calendar.png", self, "000000")        #crea senza badge e senza testo cons fondo nero
        self.button.setFixedSize(400, 400)                                          #setta le dimensioni 
        


    """
    def __init__(self, image_path=None, parent=None, color="f1f1f1"):
        super().__init__("", parent)
        
        
        self.icon = None
        if image_path:
            self.image_path = f.get_img(image_path)
            self.setButtonImage(self.image_path)
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


    
    

