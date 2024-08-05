from PyQt6 import QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QStackedWidget


import os
import sys

from API import funzioni as f



class Home_Page(QWidget):

    def __init__(self, master):

        self.master = master
