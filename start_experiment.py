import sys
import os
from PythonForTheLab.model.experiment import Experiment

from PythonForTheLab.view.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

exp = Experiment()
exp.load_config('config/simple_daq.yml')
exp.load_daq()

app = QApplication([])
mw = MainWindow(exp)
mw.show()
app.exec_()
