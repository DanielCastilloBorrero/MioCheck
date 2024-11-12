import serial

class Datos():
    
    datos = {}

    def __init__(self):
        if self.connection():
            self.readData()
        else:
            print("algo salio mal")

    def connection(self):
        try:
            self.serialPort = serial.Serial(port='COM3', baudrate=115200)
            return True
        except serial.SerialException as serialErr:
            #self.serialPort = #Error porque no hay nada q hacer cuando no se inicializa el serialPort
            print(f"Error al comunicarse por el puerto serial \n{serialErr}")
            return False
    
    def readData(self):
        try:
            linea = self.serialPort.readline().decode('utf-8').rstrip()
            valores = linea.split(',')
            
            self.datos = {
                'irValue': valores[0],
                'beatsPerMinute': valores[1],
                'beatAvg': valores[2],
                'redValue': valores[3],
                'temperature': valores[4],
                'finger': valores[5]
            }
            return self.datos
        except AttributeError as err:
            print(f'Error prro{err}')
            return None
    
    '''def closeConnection(self):
        self.serialPort.close()
        print("cerrado")'''