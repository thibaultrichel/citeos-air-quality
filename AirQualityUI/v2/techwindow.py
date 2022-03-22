import pandas as pd
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from predinfos import PredInfos
from AirQualityUI.utils.model_integration import formatDataframe, getColorAndIcon


class TechWindow(QMainWindow):
    def __init__(self, callingWindow: QMainWindow):
        super(TechWindow, self).__init__()

        self.callingWindow = callingWindow

        self.WIDTH = 1200
        self.HEIGHT = 650

        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("CiteosVision - Technical Window")
        self.setGeometry(
            round(self.callingWindow.screenWidth / 2 - self.WIDTH / 2),
            round(self.callingWindow.screenHeight / 2 - self.HEIGHT / 2),
            self.WIDTH, self.HEIGHT
        )

        self.df = None
        self.btnInfoPopup = None
        self.popup = None
        self.btnOkPopup = None
        self.predInfosWindow = None

        self.lastDate = "Please load data to display last date"
        self.dateLabel = QLabel(self.lastDate, self)
        self.dateLabel.setGeometry(600, 110, 500, 25)
        self.dateLabel.setFont(self.callingWindow.italicFont)

        # self.btnRecoltData = QPushButton("Récolter les données", self)
        # self.btnRecoltData.setGeometry(220, 100, 200, 50)

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

        self.set_basic_ui()
        self.setFocus()

    def set_basic_ui(self):
        title = QLabel("TechVision", self)
        title.setGeometry(round(self.WIDTH / 2 - 200 / 2), 10, 200, 40)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(self.callingWindow.titleFont)

        todayLabel = QLabel("Last date in table :", self)
        todayLabel.setGeometry(440, 110, 200, 25)
        todayLabel.setFont(self.callingWindow.underlineFont)

    def closeEvent(self, event):
        if self.predInfosWindow is not None:
            self.predInfosWindow.close()
        self.close()
        self.callingWindow.show()

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
        self.df = formatDataframe(df, 3)
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
        value, color = self.callingWindow.getPredictions()
        message = f"ATMO index : {str(value)}"
        self.popup = QMessageBox()
        self.popup.setWindowTitle("Prediction result")
        self.popup.setText(message)
        self.popup.setFont(self.callingWindow.boldFont)
        self.popup.setStyleSheet(f"background-color: {color}")
        self.btnInfoPopup = self.popup.addButton("Details...", QMessageBox.NoRole)
        self.btnOkPopup = self.popup.addButton("Ok", QMessageBox.YesRole)
        self.btnInfoPopup.clicked.disconnect()
        self.btnInfoPopup.clicked.connect(self.showDetails)
        self.popup.exec_()

    def showDetails(self):
        self.predInfosWindow = PredInfos(self, self.callingWindow)
        self.popup.close()
        self.predInfosWindow.show()
