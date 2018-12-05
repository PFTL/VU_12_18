import os
import numpy as np

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

from pint import UnitRegistry
ur = UnitRegistry()


import pyqtgraph as pg

class MainWindow(QMainWindow):
    def __init__(self, experiment):
        super().__init__()
        this_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(this_dir, 'main_window.ui')
        uic.loadUi(ui_file, self)

        self.start_button.clicked.connect(self.start_clicked)
        # self.start_button.clicked.connect(self.stop_clicked)

        self.stop_button.clicked.connect(self.stop_clicked)
        self.experiment = experiment

        self.start_line.setText(self.experiment.config['scan']['start'])
        self.stop_line.setText(self.experiment.config['scan']['stop'])
        self.step_line.setText(self.experiment.config['scan']['step'])

        self.start_line.editingFinished.connect(self.start_line_check)

        self.plot_widget = pg.PlotWidget(self)
        layout = self.centralwidget.layout()
        layout.addWidget(self.plot_widget)

    def start_line_check(self):
        start = ur(self.start_line.text())
        max_out = ur(self.experiment.config['daq']['maximum_out'])
        min_out = ur(self.experiment.config['daq']['minimum_out'])
        if start < min_out or start > max_out:
            self.start_button.setEnabled(False)
        else:
            self.start_button.setEnabled(True)

    def start_clicked(self):
        start = ur(self.start_line.text())
        max_out = ur(self.experiment.config['daq']['maximum_out'])
        min_out = ur(self.experiment.config['daq']['minimum_out'])
        if start<min_out or start>max_out:
            print('Start outside of range!')
            return

        # stop = ur(self.stop_line.text())
        # if stop<min_out or stop>max_out:
        #     print('Stop outside of range!')
        #     return

        self.experiment.config['scan']['start'] = self.start_line.text()
        self.experiment.config['scan']['stop'] = self.stop_line.text()
        self.experiment.config['scan']['step'] = self.step_line.text()
        self.experiment.do_scan()

    def stop_clicked(self):
        x_data = self.experiment.voltages
        y_data = self.experiment.currents

        self.plot_widget.plot(x_data, y_data)
