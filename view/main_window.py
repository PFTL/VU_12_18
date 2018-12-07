import os
import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from model import ur

import pyqtgraph as pg

from view.general_worker import WorkerThread


class MainWindow(QMainWindow):
    def __init__(self, experiment):
        super().__init__()
        this_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(this_dir, 'main_window.ui')
        uic.loadUi(ui_file, self)

        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.update_plot)

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

        self.worker_thread = WorkerThread(self.experiment.do_scan)
        self.action_Save.triggered.connect(self.experiment.save_scan_data)
        self.actionOpen_File.triggered.connect(self.load_data)

    def start_clicked(self):
        if self.experiment.scan_running:
            print('Scan Running')
            return

        self.experiment.config['scan']['start'] = self.out_start_line.text()
        self.experiment.config['scan']['stop'] = self.out_stop_line.text()
        self.experiment.config['scan']['step'] = self.out_step_line.text()
        self.experiment.config['scan']['delay'] = self.in_delay_line.text()
        self.experiment.config['scan']['channel_out'] = self.out_channel_line.text()
        self.experiment.config['scan']['channel_in'] = self.in_channel_line.text()
        self.worker_thread.start()
        self.refresh_timer.start(30)  #<- Time in milliseconds
        self.start_button.setEnabled(False)



    def load_data(self):
        self.filename = str(QFileDialog.getOpenFileName(self, "Select File", self.experiment.config['saving']['directory'])[0])

        data = np.loadtxt(self.filename, delimiter=',')

        self.plot_widget.plot(data[:,1], data[:,0], clear=True)



    def stop_clicked(self):
        self.experiment.stop_scan = True

    def update_plot(self):
        x_data = self.experiment.voltages
        y_data = self.experiment.currents

        self.plot_widget.plot(x_data, y_data, clear=True)

        if not self.experiment.scan_running:
            self.refresh_timer.stop()
            self.start_button.setEnabled(True)
