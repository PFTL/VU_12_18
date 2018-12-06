import os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from model import ur

import pyqtgraph as pg


class MainWindow(QMainWindow):
    def __init__(self, experiment):
        super().__init__()
        this_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(this_dir, 'main_window.ui')
        uic.loadUi(ui_file, self)

        self.start_button.clicked.connect(self.start_clicked)

        self.stop_button.clicked.connect(self.stop_clicked)
        self.experiment = experiment

        self.out_start_line.setText(self.experiment.config['scan']['start'])
        self.out_stop_line.setText(self.experiment.config['scan']['stop'])
        self.out_step_line.setText(self.experiment.config['scan']['step'])
        self.in_delay_line.setText(self.experiment.config['scan']['delay'])
        self.out_channel_line.setText(str(self.experiment.config['scan']['channel_out']))
        self.in_channel_line.setText(str(self.experiment.config['scan']['channel_in']))

        self.plot_widget = pg.PlotWidget(self)
        layout = self.centralwidget.layout()
        layout.addWidget(self.plot_widget)

    def start_clicked(self):
        self.experiment.config['scan']['start'] = self.out_start_line.text()
        self.experiment.config['scan']['stop'] = self.out_stop_line.text()
        self.experiment.config['scan']['step'] = self.out_step_line.text()
        self.experiment.config['scan']['delay'] = self.in_delay_line.text()
        self.experiment.config['scan']['channel_out'] = self.out_channel_line.text()
        self.experiment.config['scan']['channel_in'] = self.in_channel_line.text()
        self.experiment.do_scan()

    def stop_clicked(self):
        x_data = self.experiment.voltages
        y_data = self.experiment.currents

        self.plot_widget.plot(x_data, y_data, clear=True)
