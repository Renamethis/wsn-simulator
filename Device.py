class Device:
    __connected_sensor = None
    def __init__(self, pos, delay=None, energy=None, temperature=None, load=None):
        self._pos = pos
        self._delay = delay
        self._energy = energy
        self._temperature = temperature
        self._load = load

    def set_sensor(self, sensor):
        self.__connected_sensor = sensor

    def get_pos(self):
        return self._pos

    def get_sensor(self):
        return self.__connected_sensor

class Sensor(Device):
    def __init__(self, pos):
        super().__init__(pos) 

