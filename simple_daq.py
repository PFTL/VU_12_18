from time import sleep

import pint
import numpy as np
import serial


ur = pint.UnitRegistry()

class Device:
    def __init__(self, port):
        self.rsc = serial.Serial(port)
        self.port = port
        sleep(0.5)
        self.write_termination = '\n'
        self.read_termination = '\r\n'
        self.delay_write_read = 0.2  # Delay between writing and reading, in seconds
        self.encoding = 'ascii'

    def idn(self):
        return self.query('IDN')

    def read_analog_value(self, channel):
        command = 'IN:CH{}'.format(channel)
        answer = self.query(command)
        value_bits = int(answer)
        value_volts = value_bits * 3.3/4095
        return value_volts * ur('V')

    def set_analog_value(self, channel, value):
        command = 'OUT:CH{}:{}'.format(channel, value)
        self.write(command)
        sleep(0.1)

    def finalize(self):
        self.rsc.close()

    def write(self, command):
        command = command + self.write_termination
        self.rsc.write(command.encode(self.encoding))

    def query(self, command):
        self.write(command)
        sleep(self.delay_write_read)
        answer = self.rsc.readline()
        without_encoding = answer.decode(self.encoding)
        without_read_termination = without_encoding.strip(self.read_termination)
        return without_read_termination


    def scan_voltage(self, channel_out, channel_in, start_V, stop_V, step):
        """
        """
        start_V = start_V.m_as('V')
        stop_V = stop_V.m_as('V')
        step = step.m_as('V')

        voltages = np.arange(start_V, stop_V, step)
        self.measured_voltages = []

        for voltage in voltages:
            value = int(voltage/3.3*4095)
            self.set_analog_value(channel_out, value)
            self.measured_voltages.append(self.read_analog_value(channel_in))


    def __str__(self):
        return 'DAQ Device on port {}'.format(self.port)


dev = Device('/dev/ttyACM0')

start = 2500 * ur('mV')
stop = 3.29 * ur('V')
step = 100 * ur('mV')

dev.scan_voltage(0, 0, start, stop, step)
print(dev.measured_voltages)
dev.finalize()