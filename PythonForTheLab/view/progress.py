import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class Progress(QWidget):
    def __init__(self):
        super().__init__()
        this_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(this_dir, 'progress.ui')
        uic.loadUi(ui_file, self)

        self.RED_STYLE = """
                        QProgressBar{
                            border: 2px solid grey;
                            border-radius: 5px;
                            text-align: center
                        }

                        QProgressBar::chunk {
                            background-color: red;
                            width: 10px;
                            margin: 1px;
                        }
                        """

        self.DEFAULT_STYLE = """
                        QProgressBar{
                            border: 2px solid grey;
                            border-radius: 5px;
                            text-align: center
                        }

                        QProgressBar::chunk {
                            background-color: green;
                            width: 10px;
                            margin: 1px;
                        }
                        """

        self.YELLOW_STYLE = """
                        QProgressBar{
                            border: 2px solid grey;
                            border-radius: 5px;
                            text-align: center
                        }

                        QProgressBar::chunk {
                            background-color: yellow;
                            width: 10px;
                            margin: 1px;
                        }
                        """

    def update_progress_bar(self, value):
        if value > 75:
            self.scan_progress_bar.setStyleSheet(self.RED_STYLE)
        self.scan_progress_bar.setValue(value)

    def update_voltage(self, value):
        percentage = round(value.m_as('V')/3.3*100)
        self.scan_progress_bar.setValue(percentage)
        self.set_voltage_line.setText('{:~3.3f}'.format(value))