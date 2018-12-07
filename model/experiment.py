import os
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
        delay = ur(self.config['scan']['delay'])
        self.voltages = np.arange(start, stop+step, step)
        self.currents = np.zeros(self.voltages.shape[0])
        self.stop_scan = False
        i = 0
        for voltage in self.voltages:
            self.daq.set_analog_value(self.config['scan']['channel_out'], voltage)
            self.currents[i] = self.daq.read_current(self.config['scan']['channel_in']).m_as('mA')
            sleep(delay.m_as('s'))
            i += 1
            if self.stop_scan:
                break

        return self.currents

    def save_scan_data(self, file_path=None):
        file_path = os.path.join(self.config['saving']['directory'], self.config['saving']['filename'])

        if not os.path.isdir(self.config['saving']['directory']):
            os.makedirs(self.config['saving']['directory'])

        i = 0
        base_filename, ext = os.path.splitext(file_path)
        while os.path.isfile(file_path):
            i += 1
            filename = base_filename + str(i)
            file_path = filename + ext

        with open(file_path, 'w') as f:
            header = "# Data saved from Python For The Lab by {}\n".format(self.config['user']['name'])
            f.write(header)
            description = "# Current (mA), Voltages (V)\n"
            f.write(description)
            for i in range(len(self.currents)):
                f.write("{}, {}\n".format(self.currents[i], self.voltages[i]))


    def save_scan_metadata(self):
        pass

    def finalize(self):
        pass

if __name__ == '__main__':
    exp = Experiment()
    conf = '../config/simple_daq.yml'
    exp.load_config(conf)
    exp.save_scan_data()