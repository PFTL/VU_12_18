import yaml
from model.real_daq import DAQ


class Experiment:

    def load_config(self, filename):
        with open(filename, 'r') as f:
            self.config = yaml.load(f)

    def load_daq(self):
        self.daq = DAQ(self.config['daq']['port'], self.config['daq']['resistance'])

    def do_scan(self):
        return self.daq.read_current(0)

    def save_data(self):
        pass

    def save_metadata(self):
        pass

    def finalize(self):
        pass
