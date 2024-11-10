from PyQt6.QtGui import QGuiApplication,QIcon
from PyQt6.QtWidgets import (QMainWindow,QGraphicsBlurEffect)
from PyQt6.QtCore import Qt
from .Container import Container
from Model.ConexionEsp import Datos

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.buildWindow()
        self.buildIU()
    
    def buildWindow(self):
        self.resize(1100,500)
        self.setWindowTitle("MioCheck")
        self.setWindowIcon(QIcon('./View/source/ecg.png'))
        qRect = self.frameGeometry()
        centerPoint = QGuiApplication.primaryScreen().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())
        #self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        #self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.show()
        
    def buildIU(self):
        self.datos = Datos()
        self.container = Container(datos=self.datos)
        self.setCentralWidget(self.container)
