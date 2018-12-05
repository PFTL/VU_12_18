import serial
from time import sleep, time
from pint import UnitRegistry

ur = UnitRegistry()

class SimpleDaq:
    DEFAULTS = {'write_termination': '\n',
                'read_termination': '\n',
                'encoding': 'ascii',
                'baudrate': 9600,
                'write_timeout': 1,
                'read_timeout': 1,
                }
    rsc = None

    def __init__(self, port):
        self.initialize(port)

    def initialize(self, port):
        self.rsc = serial.Serial(port=port,
                                 baudrate=self.DEFAULTS['baudrate'],
                                 timeout=self.DEFAULTS['read_timeout'],
                                 write_timeout=self.DEFAULTS['write_timeout'])
        sleep(0.5)

    def idn(self):
        return self.query("IDN")

    def get_analog_value(self, channel):
        query_string = 'IN:CH{}'.format(channel)
        value = int(self.query(query_string))
        return value

    def set_analog_value(self, channel, value):
        write_string = 'OUT:CH{}:{}'.format(channel, value)
        self.write(write_string)

    def finalize(self):
        if self.rsc is not None:
            self.rsc.close()

    def query(self, message):
        self.write(message)
        return self.read()

    def write(self, message):
        if self.rsc is None:
            raise Warning("Trying to write to device before initializing")

        msg = (message + self.DEFAULTS['write_termination']).encode(self.DEFAULTS['encoding'])
        self.rsc.write(msg)
        sleep(0.1)

    def read(self):
        line = "".encode(self.DEFAULTS['encoding'])
        read_termination = self.DEFAULTS['read_termination'].encode(self.DEFAULTS['encoding'])

        t0 = time()
        new_char = "".encode(self.DEFAULTS['encoding'])
        while new_char != read_termination:
            new_char = self.rsc.read(size=1)
            line += new_char
            if time()-t0 > self.DEFAULTS['read_timeout']:
                raise Exception("Readout time reached when reading from the device")

        return line.decode(self.DEFAULTS['encoding'])