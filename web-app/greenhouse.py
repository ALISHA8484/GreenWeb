import serial
import json
import threading

class Greenhouse:
    def __init__(self, name, port):
        self.name = name
        self.port = port
        self.latest_data = {'temp': 0, 'hum': 0, 'status': 'Initializing'}
        try:
            self.ser = serial.Serial(self.port, 115200, timeout=1)

        except:
            self.latest_data['status'] = 'Offline'

    def read_loop(self):
        while True:
            try:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').rstrip()
                    data = json.loads(line)
                    self.latest_data = {
                        'temp': data.get('t'),
                        'hum': data.get('h') + 1,
                        'status': 'Online'
                    }
                return self.latest_data
            except Exception as e:
                self.latest_data['status'] = 'Error'

    def get_data(self):
        return self.latest_data