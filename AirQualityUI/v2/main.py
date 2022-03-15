import sys
import pathlib
import numpy as np
import pandas as pd
from AirQualityUI.utils.myfont import MyFont
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from platform import system
from PyQt5.QtWidgets import *
from AirQualityUI.utils.model_integration import getPredictions, formatDataframe


class CiteosVision(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(CiteosVision, self).__init__(*args, **kwargs)

        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry()
        screenHeight = screenRect.height()
        screenWidth = screenRect.width()

        self.running_system = system()
        self.version = pathlib.Path("main.py").parent.absolute().__str__().split("/")[-1]
        self.WIDTH = 500
        self.HEIGHT = 200
        self.modelPath = "/home/thibault/Bureau/citeos-air-quality/models/LSTM_multi_with_target.h5"
        self.csvUrl = "https://raw.githubusercontent.com/thibaultrichel/citeos-air-quality/main/data/final/merged" \
                      "-final.csv "
        self.df = None

        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("Citeos Demo")
        self.setGeometry(
            round(screenWidth / 2 - self.WIDTH / 2),
            round(screenHeight / 2 - self.HEIGHT / 2),
            self.WIDTH, self.HEIGHT
        )

        if self.running_system == "Darwin":  # MacOS
            titleFontSize = 28
            baseFontSize = 20
        else:  # Linux or Windows
            titleFontSize = 22
            baseFontSize = 12
        self.titleFont = MyFont(titleFontSize, True, False, True)
        self.underlineFont = MyFont(baseFontSize, False, False, True)
        self.basicFont = MyFont(baseFontSize, False, False, False)
        self.boldFont = MyFont(baseFontSize, True, False, False)
        self.italicFont = MyFont(baseFontSize, False, True, False)
        self.set_basic_ui()

        self.btnTechnicalWindow = QPushButton("Technical", self)
        self.btnTechnicalWindow.setGeometry(50, 130, 200, 40)

        self.btnUserWindow = QPushButton("User", self)
        self.btnUserWindow.setGeometry(self.WIDTH - 240, 130, 200, 40)

    def set_basic_ui(self):
        title = QLabel("CiteosVision", self)
        title.setGeometry(round(self.WIDTH / 2 - 200 / 2), 10, 200, 40)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(self.titleFont)

        labelUser = QLabel("Choose your user type :", self)
        labelUser.setGeometry(10, 70, 200, 40)
        labelUser.setAlignment(Qt.AlignCenter)
        labelUser.setFont(self.basicFont)

        labelVersion = QLabel(f"version: {self.version}", self)
        labelVersion.setGeometry(1, 1, 63, 10)
        labelVersion.setFont(MyFont(10, False, False, False))
        labelVersion.setStyleSheet("color: grey")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Citeos Demo")
    window = CiteosVision()
    window.show()
    sys.exit(app.exec_())
