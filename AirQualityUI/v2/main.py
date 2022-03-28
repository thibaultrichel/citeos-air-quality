import sys
import pathlib
import numpy as np
import pandas as pd
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from platform import system
from PyQt5.QtWidgets import *
from techwindow import TechWindow
from userwindow import UserWindow
from AirQualityUI.utils.myfont import MyFont
from AirQualityUI.utils.model_integration import formatDataframe, getColorAndIcon, ModelUtil


class CiteosVision(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(CiteosVision, self).__init__(*args, **kwargs)

        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry()
        self.screenHeight = screenRect.height()
        self.screenWidth = screenRect.width()
        self.WIDTH = 500
        self.HEIGHT = 200

        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("CiteosVision")
        self.setGeometry(
            round(self.screenWidth / 2 - self.WIDTH / 2),
            round(self.screenHeight / 2 - self.HEIGHT / 2),
            self.WIDTH, self.HEIGHT
        )

        self.techWindow, self.userWindow = None, None
        self.running_system = system()
        self.version = pathlib.Path("main.py").parent.absolute().__str__().split("/")[-1]

        if self.running_system == "Darwin":  # MacOS
            self.modelPath = "../../models/LSTM_multi_with_target.h5"
            titleFontSize = 28
            baseFontSize = 20
        else:  # Linux
            self.modelPath = "/home/thibault/Bureau/citeos-air-quality/models/LSTM_multi_with_target.h5"
            titleFontSize = 20
            baseFontSize = 12
        self.titleFont = MyFont(titleFontSize, True, False, True)
        self.underlineFont = MyFont(baseFontSize, False, False, True)
        self.basicFont = MyFont(baseFontSize, False, False, False)
        self.boldFont = MyFont(baseFontSize, True, False, False)
        self.italicFont = MyFont(baseFontSize, False, True, False)
        self.set_basic_ui()

        self.btnTechnicalWindow = QPushButton("Technical", self)
        self.btnTechnicalWindow.setGeometry(50, 130, 200, 40)
        self.btnTechnicalWindow.clicked.connect(self.openTechWindow)

        self.btnUserWindow = QPushButton("User", self)
        self.btnUserWindow.setGeometry(self.WIDTH - 240, 130, 200, 40)
        self.btnUserWindow.clicked.connect(self.openUserWindow)

        self.csvUrl = "https://raw.githubusercontent.com/thibaultrichel/citeos-air-quality/main/data/final/merged" \
                      "-final.csv"
        self.columnsNames = ["Date", "PM10", "PM2.5", "NO2", "SO2", "NO", "NOX", "O3", "Temperature", "Wind speed",
                             "Humidity", "Pressure", "Wind direction", "Weather event", "ATMO"]
        self.dfraw = pd.read_csv(self.csvUrl, sep=';').dropna()
        self.dfraw = self.dfraw[
            ['date', 'PM10', 'PM25', 'NO2', 'SO2', 'NO', 'NOX', 'O3', 'temp', 'wind_speed', 'wind_dir',
             'hum', 'press', 'weather_event', 'ATMO']
        ]
        self.df = formatDataframe(self.dfraw, 1)
        self.modelUtil = ModelUtil(self.modelPath)

        self.setFocus()

    def set_basic_ui(self):
        title = QLabel("CiteosVision", self)
        title.setGeometry(round(self.WIDTH / 2 - 200 / 2), 0, 200, 40)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(self.titleFont)

        labelUser = QLabel("Choose your user type :", self)
        labelUser.setGeometry(10, 70, 200, 40)
        labelUser.setAlignment(Qt.AlignCenter)
        labelUser.setFont(self.basicFont)

        labelVersion = QLabel(f"version: {self.version}", self)
        labelVersion.setGeometry(1, self.HEIGHT - 12, 63, 10)
        labelVersion.setFont(MyFont(10, False, False, False))
        labelVersion.setStyleSheet("color: grey")

        logoCiteos = QLabel(self)
        pixmapCiteos = QPixmap('../../images/citeos.resized.png')
        logoCiteos.setPixmap(pixmapCiteos)
        logoCiteos.resize(pixmapCiteos.width(), pixmapCiteos.height())
        logoCiteos.setGeometry(0, 0, pixmapCiteos.width(), pixmapCiteos.height())

        logoEsme = QLabel(self)
        pixmapEsme = QPixmap("../../images/esme.resized.png")
        logoEsme.setPixmap(pixmapEsme)
        logoEsme.resize(pixmapEsme.width(), pixmapEsme.height())
        logoEsme.setGeometry(self.WIDTH - pixmapEsme.width(), 0, pixmapEsme.width(), pixmapEsme.height())

    def openTechWindow(self):
        self.techWindow = TechWindow(self)
        self.techWindow.show()
        self.hide()

    def openUserWindow(self):
        self.userWindow = UserWindow(self)
        self.userWindow.show()
        self.hide()

    def formatPredictionData(self):
        X_test = self.df[-120:]
        X_test = np.expand_dims(X_test, axis=0)
        return X_test

    def getPredictions(self):
        X_test = self.formatPredictionData()
        y_pred = self.modelUtil.getPredictions(X_test)
        # y_pred = getPredictions(self.modelPath, X_test)
        value = np.round(y_pred[0][0], 2)
        color = getColorAndIcon(value)
        return value, color


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Citeos Demo")
    window = CiteosVision()
    window.show()
    sys.exit(app.exec_())
