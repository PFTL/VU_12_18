from controller.simple_daq import SimpleDaq
from model import ur

class DAQ:
    def __init__(self, port, resistance):
        self.driver = SimpleDaq(port)
        self.resistance = ur(resistance)

    def idn(self):
        return self.driver.idn()

    def read_current(self, channel):
        value = self.driver.get_analog_value(channel)
        current = value/1023*ur('3.3V')/self.resistance
        return current

    def set_analog_value(self, channel, value):
        """ value should be in volts.
        """
        value = int(value/3.3*4095)
        if value > 4095:
            raise Exception('Value out of range')

        self.driver.set_analog_value(channel, value)

