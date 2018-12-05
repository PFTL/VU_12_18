from time import sleep
import sys
import os
from model.experiment import Experiment

import threading

from view.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

exp = Experiment()
exp.load_config('config/simple_daq.yml')
exp.load_daq()

app = QApplication([])
mw = MainWindow(exp)
mw.show()
app.exec_()

exp.finalize()
