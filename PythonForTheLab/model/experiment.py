import os
from time import sleep

import numpy as np
import yaml

from PythonForTheLab.model.real_daq import DAQ
from PythonForTheLab.model.dummy_daq import DummyDAQ
from PythonForTheLab.model import ur


class Experiment:
    def __init__(self):
        self.scan_progress = 0
        self.scan_running = False
        self.config = {} # Configuration dictionary for the experiment
        self.current_voltage = 0 * ur('V')

    def load_config(self, filename):
        with open(filename, 'r') as f:
            self.config = yaml.load(f)

    def load_daq(self):
        if self.config['daq']['type'] == 'RealDAQ':
            self.daq = DAQ(self.config['daq']['port'], self.config['daq']['resistance'])
        elif self.config['daq']['type'] == 'DummyDAQ':
            self.daq = DummyDAQ(self.config['daq']['port'], self.config['daq']['resistance'])
        else:
            raise Exception('DAQ not recognized')

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
        self.scan_running = True
        i = 0
        self.scan_progress = 0
        for voltage in self.voltages:
            self.current_voltage = voltage * ur('V')
            self.daq.set_analog_value(self.config['scan']['channel_out'], voltage)
            self.currents[i] = self.daq.read_current(self.config['scan']['channel_in']).m_as('mA')
            sleep(delay.m_as('s'))
            i += 1
            self.scan_progress = int(i/self.voltages.shape[0]*100)
            if self.stop_scan:
                break
        self.scan_running = False

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

        metadata_filename, ext = os.path.splitext(file_path)
        metadata_filename = metadata_filename + '.yml'
        self.save_scan_metadata(metadata_filename)

    def save_scan_metadata(self, file_path):
        with open(file_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)

    def finalize(self):
        self.daq.finalize()

    def __del__(self):
        self.finalize()

if __name__ == '__main__':
    exp = Experiment()
    conf = '../config/simple_daq.yml'
    exp.load_config(conf)
    exp.save_scan_data()
