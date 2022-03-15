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
        self.version = pathlib.Path("./main.py").parent.absolute().__str__().split("/")[-1]
        self.WIDTH = 1200
        self.HEIGHT = 650
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
            titleFontSize = 24
            baseFontSize = 16
        self.titleFont = MyFont(titleFontSize, True, False, True)
        self.underlineFont = MyFont(baseFontSize, False, False, True)
        self.basicFont = MyFont(baseFontSize, False, False, False)
        self.boldFont = MyFont(baseFontSize, True, False, False)
        self.italicFont = MyFont(baseFontSize, False, True, False)
        self.set_basic_ui()

        self.lastDate = "Please load data to display last date"
        self.dateLabel = QLabel(self.lastDate, self)
        self.dateLabel.setGeometry(625, 110, 500, 25)
        self.dateLabel.setFont(self.italicFont)

        self.btnRecoltData = QPushButton("Récolter les données", self)
        self.btnRecoltData.setGeometry(220, 100, 200, 50)

        self.btnUploadData = QPushButton("Charger les données", self)
        self.btnUploadData.setGeometry(10, 100, 200, 50)
        self.btnUploadData.clicked.connect(lambda: self.csvToTable(self.csvUrl))

        self.columnsNames = ["Date", "PM10", "PM2.5", "NO2", "SO2", "NO", "NOX", "O3", "Temperature", "Wind speed",
                             "Humidity", "Pressure", "Wind direction", "Weather event", "ATMO"]

        self.table = QTableWidget(self)
        self.table.setColumnCount(15)
        self.header = self.table.horizontalHeader()
        for i, cname in enumerate(self.columnsNames):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(cname))
            if 0 < i < 8:
                self.table.setColumnWidth(i, 50)
        self.table.setCurrentCell(-1, -1)
        self.table.setGeometry(10, 160, 1180, 400)
        self.autoResizeTable()

        self.btnPredict = QPushButton("Predict next 12h ATMO index", self)
        self.btnPredict.setGeometry(10, 590, 220, 50)
        self.btnPredict.setEnabled(False)
        self.btnPredict.clicked.connect(self.displayPredictions)

        self.btnQuit = QPushButton("Quit", self)
        self.btnQuit.setGeometry(self.WIDTH - 110, 590, 100, 50)
        self.btnQuit.setFont(self.boldFont)
        self.btnQuit.clicked.connect(QCoreApplication.instance().quit)

        self.setFocus()

    def set_basic_ui(self):
        title = QLabel("Prévision indice ATMO", self)
        title.setGeometry(round(self.WIDTH / 2 - 370 / 2), 10, 370, 40)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(self.titleFont)

        todayLabel = QLabel("Last date in table :", self)
        todayLabel.setGeometry(440, 110, 200, 25)
        todayLabel.setFont(self.underlineFont)

        logoCiteos = QLabel(self)
        pixmapCiteos = QPixmap('../images/citeos.png')
        logoCiteos.setPixmap(pixmapCiteos)
        logoCiteos.resize(pixmapCiteos.width(), pixmapCiteos.height())
        logoCiteos.setGeometry(self.WIDTH - pixmapCiteos.width(), 0, pixmapCiteos.width(), pixmapCiteos.height())

        logoEsme = QLabel(self)
        pixmapEsme = QPixmap("../images/esme.png")
        logoEsme.setPixmap(pixmapEsme)
        logoEsme.resize(pixmapEsme.width(), pixmapEsme.height())
        logoEsme.setGeometry(self.WIDTH - pixmapEsme.width(), 40, pixmapEsme.width(), pixmapEsme.height())

        labelVersion = QLabel(f"version: {self.version}", self)
        labelVersion.setGeometry(1, 1, 63, 10)
        labelVersion.setFont(MyFont(10, False, False, False))
        labelVersion.setStyleSheet("color: grey")

    def autoResizeTable(self):
        self.header = self.table.horizontalHeader()
        for i in range(len(self.columnsNames)):
            if i == 0:
                self.header.setSectionResizeMode(i, QHeaderView.Stretch)
            else:
                self.header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def csvToTable(self, path):
        df = pd.read_csv(path, sep=';').dropna()
        df = df[['date', 'PM10', 'PM25', 'NO2', 'SO2', 'NO', 'NOX', 'O3', 'temp', 'wind_speed', 'wind_dir', 'hum',
                 'press', 'weather_event', 'ATMO']]
        self.df = formatDataframe(df)
        values = list(df.values)
        self.table.setRowCount(len(values))
        for i, row in enumerate(values):
            row_values = row.tolist()
            for val in row_values:
                idx = row_values.index(val)
                self.table.setItem(i, idx, QTableWidgetItem(str(val)))
                self.table.item(i, idx).setFlags(Qt.ItemIsEnabled)
        self.dateLabel.setText(self.getLastDate())
        self.autoResizeTable()
        self.btnPredict.setEnabled(True)

    def getLastDate(self):
        lastDate = self.table.item(self.table.rowCount() - 1, 0).text()
        self.dateLabel.setFont(self.basicFont)
        return lastDate

    def formatPredictionData(self):
        X_test = self.df[-120:]
        X_test = np.expand_dims(X_test, axis=0)
        return X_test

    @staticmethod
    def getColorAndIcon(value):
        color = ""
        icon = None
        if 0 < value <= 1:
            color = "green"
            icon = QPixmap("../images/icon-good.png")
        elif 1 <= value < 2:
            color = "blue"
            icon = QPixmap("../images/icon-ok.png")
        elif 2 <= value < 3:
            color = "rgb(255, 212, 51)"
            icon = QPixmap("../images/icon-warning-ok.png")
        elif 3 <= value < 4:
            color = "rgb(255, 131, 50)"
            icon = QPixmap("../images/icon-warning.png")
        elif 4 <= value < 5:
            color = "red"
            icon = QPixmap("../images/icon-bad.png")
        elif value >= 5:
            color = "purple"
            icon = QPixmap("../../images/icon-rlybad.png")
        return color, icon

    def displayPredictions(self):
        X_test = self.formatPredictionData()
        y_pred = getPredictions(self.modelPath, X_test)
        value = np.round(y_pred[0][0], 2)
        message = f"ATMO index : {str(value)}"
        color, icon = self.getColorAndIcon(value)
        popup = QMessageBox()
        popup.setWindowTitle("Prediction result")
        popup.setText(message)
        popup.setFont(self.boldFont)
        popup.setStyleSheet(f"color: {color}")
        popup.setIconPixmap(icon)
        popup.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Citeos Demo")
    window = CiteosVision()
    window.show()
    sys.exit(app.exec_())
