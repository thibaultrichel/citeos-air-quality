import pandas as pd
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from AirQualityUI.utils.model_integration import formatDataframe, getPredictions, getColorAndIcon


class TechWindow(QMainWindow):
    def __init__(self, callingWindow: QMainWindow):
        super(TechWindow, self).__init__()

        self.callingWindow = callingWindow
        self.callingWindow.setVisible(False)
        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry()
        screenHeight = screenRect.height()
        screenWidth = screenRect.width()

        self.WIDTH = 1200
        self.HEIGHT = 650

        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("CiteosVision - Technical Window")
        self.setGeometry(
            round(screenWidth / 2 - self.WIDTH / 2),
            round(screenHeight / 2 - self.HEIGHT / 2),
            self.WIDTH, self.HEIGHT
        )

        self.df = None

        self.lastDate = "Please load data to display last date"
        self.dateLabel = QLabel(self.lastDate, self)
        self.dateLabel.setGeometry(625, 110, 500, 25)
        self.dateLabel.setFont(self.callingWindow.italicFont)

        self.btnRecoltData = QPushButton("Récolter les données", self)
        self.btnRecoltData.setGeometry(220, 100, 200, 50)

        self.btnUploadData = QPushButton("Charger les données", self)
        self.btnUploadData.setGeometry(10, 100, 200, 50)
        self.btnUploadData.clicked.connect(lambda: self.csvToTable(self.callingWindow.csvUrl))

        self.table = QTableWidget(self)
        self.table.setColumnCount(15)
        self.header = self.table.horizontalHeader()
        for i, cname in enumerate(self.callingWindow.columnsNames):
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

        self.setFocus()

    def closeEvent(self, event):
        self.callingWindow.show()
        self.close()

    def autoResizeTable(self):
        self.header = self.table.horizontalHeader()
        for i in range(len(self.callingWindow.columnsNames)):
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
        self.dateLabel.setFont(self.callingWindow.basicFont)
        return lastDate

    def formatPredictionData(self):
        X_test = self.df[-120:]
        X_test = np.expand_dims(X_test, axis=0)
        return X_test

    def displayPredictions(self):
        X_test = self.formatPredictionData()
        y_pred = getPredictions(self.callingWindow.modelPath, X_test)
        value = np.round(y_pred[0][0], 2)
        message = f"ATMO index : {str(value)}"
        color = getColorAndIcon(value)
        print(message, color)
