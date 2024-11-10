import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QPushButton, QWidget

class CustomDialog(QDialog):
    
    def __init__(self):
        super().__init__()
        self.exec()
    
    