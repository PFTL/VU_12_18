import sys
import os
from PythonForTheLab.model.experiment import Experiment
from PythonForTheLab.view.main_window import MainWindow
from PyQt5.QtWidgets import QApplication


def start():
    """Starts the GUI for the experiment using the config file specified as system argument.
    """
    args = sys.argv[1:]
    if len(args) != 1:
        print(help_message)
        return

    experiment = Experiment()
    experiment.load_config(args[0])
    experiment.load_daq()
    app = QApplication([])
    mw = MainWindow(experiment)
    mw.show()
    app.exec_()


help_message = \
"""
Welcome to Python For The Lab
-----------------------------
In order to run the program, you need to supply the path to the config file.
For example, you can invoke this program as:
py4lab Config/experiment.yml
"""


if __name__ == "__main__":
    start()