from controller.simple_daq import SimpleDaq


class DAQ:
    def __init__(self, port, resistance):
        self.driver = SimpleDaq(port)
        self.resistance = resistance

    def read_current(self, channel):
        value = self.driver.get_analog_value(channel)
        current = value / self.resistance
        return current

    def set_voltage(self, channel, voltage):
        self.driver.set_analog_value(channel, voltage)