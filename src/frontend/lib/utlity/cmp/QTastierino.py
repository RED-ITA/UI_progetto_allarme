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
    def __init__(self, text=None, parent=None, color="f1f1f1"):
        super().__init__("", parent)
        
        
        self.icon = None
        if text:
            if text != "x" and text != "v":
                self.setText(text)
                self.initStylesheet(color)
            else:
                if text == "v":
                    image_path = "checkmark.png"
                if text == "x":
                    image_path = "delete.png"
                self.image_path = f.get_img(image_path)
                self.setButtonImage(self.image_path)
                self.initStylesheet2(color)

    def initStylesheet(self, color):
        self.setStyleSheet("""
            QPushButton {
                background-color: #""" + color +""";
                border: 20px solid #A5A5A9;
                font-size: 60px;
                color: #8E8E93;
                font-size: 32xp;
                border-radius: 55px;
            }


            QPushButton:pressed {
                background-color: #A5A5A9;
            }

            
        """)

    def initStylesheet2(self, color):
        self.setStyleSheet("""
            QPushButton {
                background-color: #""" + color +""";
                
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


    
    

