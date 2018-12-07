import numpy as np
from model import ur


class DummyDAQ:
    def __init__(self, port, resistance):
        self.port = port
        self.resistance = resistance

    def idn(self):
        return 'Summy daq at port {} with resistance {}'.format(self.port, self.resistance)

    def read_current(self, channel):
        return np.random.random((1)) * ur('A')

    def set_analog_value(self, channel, value):
        pass

    def finalize(self):
        pass