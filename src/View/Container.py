from PyQt6.QtWidgets import (QWidget,QLabel,QVBoxLayout,QHBoxLayout)
from PyQt6.QtGui import QCloseEvent, QPixmap, QAction, QFont
from PyQt6.QtCore import QTimer, Qt
import pyqtgraph as pg
from collections import deque

class Container(QWidget):
    
    def __init__(self, datos):
        super().__init__()
        self.datos = datos
        self.buildWidget()
        
    def buildWidget(self):
        self.setStyleSheet("QWidget { border-radius: 30px; }")
        self.font = QFont("Comic Sans MS", 20)
        
        self.plotWidget = pg.PlotWidget()
        self.plotWidget.setXRange(0, 100)
        #self.plot_ir = self.plotWidget.plot(pen='b')
        self.plot_red = self.plotWidget.plot(pen='r')
        #self.data_ir = deque(maxlen=100) #Datos led infrarrojo
        self.data_red = deque(maxlen=100) #Datos led rojo
        
        self.timer = QTimer()
        self.timer.setInterval(20)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(20)
        
        hLayout = QHBoxLayout()
        hLayout.addWidget(self.heartWidget()) #HeartRate Widget (bpm)
        hLayout.addWidget(self.oxyWidget()) #Oximetry Widget (SPO2)
        hLayout.addWidget(self.tempWidget()) #Temperature Widget (°C)
        
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.plotWidget)
        vLayout.addLayout(hLayout)
                
        self.setLayout(vLayout)
    
    def heartWidget(self):
        self.heartWidget = QWidget()
        
        self.heartWidget.setStyleSheet('''
            background-color: rgba(255, 77, 77, 0.5);
        ''')
        
        label_Image = QLabel()
        label_Image.setMinimumWidth(150)
        label_Image.setMaximumWidth(150)
        pixmap = QPixmap("./View/source/Heart.png").scaled(label_Image.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        label_Image.setPixmap(pixmap)
        
        self.label_heart_text = QLabel()
        self.label_heart_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_heart_text.setFont(self.font)
        self.label_heart_text.setText("No Finger")
        
        layout = QHBoxLayout()
        layout.addWidget(label_Image)
        layout.addWidget(self.label_heart_text)
        
        self.heartWidget.setLayout(layout)
        return self.heartWidget
    
    def oxyWidget(self):
        self.spo2Widget = QWidget()
        
        self.spo2Widget.setStyleSheet("""
            background-color: rgba(153, 204, 255, 0.5);                   
        """)
        
        labelImage = QLabel()
        labelImage.setMinimumWidth(150)
        labelImage.setMaximumWidth(150)
        pixmap = QPixmap("./View/source/SPO2.png").scaled(labelImage.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        labelImage.setPixmap(pixmap)
        
        self.label_oxy_text = QLabel()
        self.label_oxy_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_oxy_text.setText("Saturación\n99%")
        self.label_oxy_text.setFont(self.font)
        
        layout = QHBoxLayout()
        layout.addWidget(labelImage)
        layout.addWidget(self.label_oxy_text)
        
        self.spo2Widget.setLayout(layout)
        return self.spo2Widget
    
    def tempWidget(self):
        self.tempWidget = QWidget()
        
        self.tempWidget.setStyleSheet("""
            background-color: rgba(255, 195, 0, 0.5);
        """)
        
        labelImage = QLabel()
        labelImage.setMinimumWidth(150)
        labelImage.setMaximumWidth(150)
        pixmap = QPixmap("./View/source/Temp.png").scaled(labelImage.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        labelImage.setPixmap(pixmap)
        
        self.label_temp_text = QLabel()
        self.label_temp_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_temp_text.setText('Temperatura\n0°C')
        self.label_temp_text.setFont(self.font)
        
        layout = QHBoxLayout()
        layout.addWidget(labelImage)
        layout.addWidget(self.label_temp_text)
        
        self.tempWidget.setLayout(layout)
        return self.tempWidget
    
    def update_plot(self):
        data_dict = self.datos.readData()
        if data_dict is not None:
            try:
                #data_float_ir = float(data_dict['irValue'])
                data_float_red = float(data_dict['redValue'])
                
                #self.data_ir.append(data_float_ir)
                self.data_red.append(data_float_red)
                
                if data_dict['finger'] != 'No finger?':
                    #self.plot_ir.setData(self.data_ir)
                    self.plot_red.setData(self.data_red)

                    self.label_heart_text.setText(f"{data_dict['beatAvg']} Bpm")
                else:    
                    self.label_heart_text.setText("No Finger")
            except ValueError as val:
                pass
        
    