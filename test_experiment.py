import sys
import os
from model.experiment import Experiment

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


exp = Experiment()
exp.load_config('config/simple_daq.yml')
exp.load_daq()
exp.do_scan()
exp.save_scan_data()