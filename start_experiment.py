import sys
import os
from model.experiment import Experiment


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

exp = Experiment()
exp.load_config('config/simple_daq.yml')
exp.load_daq()
print(exp.daq.read_current(0).to('mA'))
print(exp.config)
exp.finalize()