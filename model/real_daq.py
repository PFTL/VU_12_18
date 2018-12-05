from controller.simple_daq import SimpleDaq

from pint import UnitRegistry

ur = UnitRegistry()


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
        self.driver.set_analog_value(channel, value)
