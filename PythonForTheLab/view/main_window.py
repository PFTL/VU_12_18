import os
import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QFileDialog

import pyqtgraph as pg

from PythonForTheLab.view.general_worker import WorkerThread
from PythonForTheLab.view.progress import Progress


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

        self.plot_widget = pg.PlotWidget(self)
        self.progress_widget = Progress()
        layout = self.centralwidget.layout()
        layout.addWidget(self.plot_widget)
        layout.addWidget(self.progress_widget)

        self.out_start_line.setText(self.experiment.config['scan']['start'])
        self.out_stop_line.setText(self.experiment.config['scan']['stop'])
        self.out_step_line.setText(self.experiment.config['scan']['step'])
        self.in_delay_line.setText(self.experiment.config['scan']['delay'])
        self.out_channel_line.setText(str(self.experiment.config['scan']['channel_out']))
        self.in_channel_line.setText(str(self.experiment.config['scan']['channel_in']))

        self.worker_thread = WorkerThread(self.experiment.do_scan)
        self.action_Save.triggered.connect(self.experiment.save_scan_data)
        self.actionOpen_File.triggered.connect(self.load_data)
        self.progress_widget.scan_progress_bar.setValue(0)

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

        # self.progress_widget.set_voltage_line.setText("{:~3.3f}".format(self.experiment.current_voltage))
        # self.progress_widget.update_progress_bar(self.experiment.scan_progress)
        self.progress_widget.update_voltage(self.experiment.current_voltage)
        if not self.experiment.scan_running:
            self.refresh_timer.stop()
            self.start_button.setEnabled(True)
