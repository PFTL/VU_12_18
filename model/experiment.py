from time import sleep

import numpy as np
import yaml

from model.real_daq import DAQ
from model import ur


class Experiment:
    def load_config(self, filename):
        with open(filename, 'r') as f:
            self.config = yaml.load(f)

    def load_daq(self):
        self.daq = DAQ(self.config['daq']['port'], self.config['daq']['resistance'])

    def do_scan(self):
        start = ur(self.config['scan']['start'])
        start = start.m_as('V')
        stop = ur(self.config['scan']['stop'])
        stop = stop.m_as('V')
        step = ur(self.config['scan']['step'])
        step = step.m_as('V')

        self.voltages = np.arange(start, stop+step, step)
        self.currents = np.zeros(self.voltages.shape[0])
        self.stop_scan = False
        i = 0
        for voltage in self.voltages:
            self.daq.set_analog_value(self.config['scan']['channel_out'], voltage)
            self.currents[i] = self.daq.read_current(self.config['scan']['channel_in']).m_as('mA')
            sleep(self.config['scan']['delay'].m_as('s'))
            i += 1
            if self.stop_scan:
                break

        return self.currents

    def save_scan_data(self, file_path=None):
        pass

    def save_scan_metadata(self):
        pass

    def finalize(self):
        pass
