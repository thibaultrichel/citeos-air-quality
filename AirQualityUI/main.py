import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from myfont import MyFont
import pandas as pd
from utils_model import getModel


class CiteosVision(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(CiteosVision, self).__init__(*args, **kwargs)

        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry()
        screenHeight = screenRect.height()
        screenWidth = screenRect.width()

        self.WIDTH = 1300
        self.HEIGHT = 700
        self.csvUrl = "https://raw.githubusercontent.com/thibaultrichel/citeos-air-quality/main/data/final/merged" \
                      "-final.csv "

        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("Citeos Demo")
        self.setGeometry(
            round(screenWidth / 2 - self.WIDTH / 2),
            round(screenHeight / 2 - self.HEIGHT / 2),
            self.WIDTH, self.HEIGHT
        )

        self.titleFont = MyFont(24, True, False, True)
        self.underlineFont = MyFont(16, False, False, True)
        self.basicFont = MyFont(16, False, False, False)
        self.italicFont = MyFont(16, False, True, False)
        self.set_basic_ui()

        self.lastDate = "Please load data to display last date"
        self.dateLabel = QLabel(self.lastDate, self)
        self.dateLabel.setGeometry(190, 100, 500, 25)
        self.dateLabel.setFont(self.italicFont)

        self.btnRecoltData = QPushButton("Récolter les données", self)
        self.btnRecoltData.setGeometry(10, 140, 200, 50)

        self.btnUploadData = QPushButton("Charger les données", self)
        self.btnUploadData.setGeometry(220, 140, 200, 50)
        self.btnUploadData.clicked.connect(lambda: self.csvToTable(self.csvUrl))

        self.columnsNames = ["Date", "PM10", "PM2.5", "NO2", "SO2", "NO", "NOX", "O3", "Temperature", "Wind speed",
                             "Humidity", "Pressure", "Wind direction", "Weather event", "ATMO"]

        self.table = QTableWidget(self)
        self.table.setColumnCount(15)
        self.table.verticalHeader().setFixedWidth(20)
        self.header = self.table.horizontalHeader()
        for i, cname in enumerate(self.columnsNames):
            self.table.setHorizontalHeaderItem(i, QTableWidgetItem(cname))
            if 0 < i < 8:
                self.table.setColumnWidth(i, 50)
        self.table.setCurrentCell(-1, -1)
        self.table.setGeometry(10, 200, 1190, 400)
        self.autoResizeTable()

        self.setFocus()

    def set_basic_ui(self):
        title = QLabel("Prévision indice ATMO", self)
        title.setGeometry(round(self.WIDTH / 2 - 370 / 2), 10, 370, 40)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(self.titleFont)

        todayLabel = QLabel("Last date in table :", self)
        todayLabel.setGeometry(10, 100, 200, 25)
        todayLabel.setFont(self.underlineFont)

    def autoResizeTable(self):
        self.header = self.table.horizontalHeader()
        for i in range(len(self.columnsNames)):
            if i == 0:
                self.header.setSectionResizeMode(i, QHeaderView.Stretch)
            else:
                self.header.setSectionResizeMode(i, QHeaderView.ResizeToContents)

    def csvToTable(self, path):
        df = pd.read_csv(path, sep=';')
        df = df[['date', 'PM10', 'PM25', 'NO2', 'SO2', 'NO', 'NOX', 'O3', 'temp', 'wind_speed', 'wind_dir', 'hum',
                 'press', 'weather_event', 'ATMO']]
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

    def getLastDate(self):
        lastDate = self.table.item(self.table.rowCount() - 1, 0).text()
        self.dateLabel.setFont(self.basicFont)
        return lastDate


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("Citeos Demo")
    window = CiteosVision()
    window.show()
    app.exec_()
