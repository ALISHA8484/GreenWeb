# import serial
import json
import time
import random

class Greenhouse:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.baud_rate = 115200

    # def read_sensor_data(self):
    #     try:
    #         with serial.Serial(self.port, self.baud_rate, timeout=1) as ser:
    #             ser.flushInput()
                
    #             line = ser.readline().decode('utf-8').rstrip()
                
    #             if line:
    #                 data = json.loads(line)
    #                 return {
    #                     'temp': data.get('t'),
    #                     'hum': data.get('h'),
    #                     'status': 'Online'
    #                 }
    #             else:
    #                 return {'temp': 0, 'hum': 0, 'status': 'No Data'}

    #     except serial.SerialException:
    #         print(f"Warning: Could not open {self.port}. Using dummy data.")
    #         return {
    #             'temp': round(25 + random.uniform(-2, 2), 1),
    #             'hum': round(45 + random.uniform(-5, 5), 1),
    #             'status': 'Simulation'
    #         }
    #     except Exception as e:
    #         print(f"Error reading sensor: {e}")
    #         return {'temp': 0, 'hum': 0, 'status': 'Error'}