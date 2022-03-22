import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas import to_datetime
from AirQualityUI.utils.model_integration import formatDataframe, getDateNext12h


class PredInfos(QMainWindow):
    def __init__(self, callingWindow: QMainWindow, mainWindow: QMainWindow):
        super(PredInfos, self).__init__()

        self.mainWindow = mainWindow
        self.callingWindow = callingWindow

        self.WIDTH = 800
        self.HEIGHT = 600

        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("CiteosVision - Technical Window")
        self.setGeometry(
            round(self.mainWindow.screenWidth / 2 - self.WIDTH / 2),
            round(self.mainWindow.screenHeight / 2 - self.HEIGHT / 2),
            self.WIDTH, self.HEIGHT
        )

        self.df, self.gb = self.getDatasetForPlots()

        self.fig = QLabel(self)
        pix = self.testPlot()
        self.fig.setPixmap(pix)
        self.fig.setGeometry(
            int(self.WIDTH / 2 - pix.width() / 2),
            int(self.HEIGHT / 2 - pix.height() / 2),
            pix.width(),
            pix.height()
        )

    def closeEvent(self, event):
        self.callingWindow.show()
        self.close()

    def getDatasetForPlots(self):
        df = formatDataframe(self.mainWindow.dfraw, 2)
        df.date = to_datetime(df.date)
        df.day = to_datetime(df.day)
        gb = df.groupby("day").mean()
        return df, gb

    def testPlot(self):
        myFmt = mdates.DateFormatter('%d/%m/%Y %H:%M')
        path = "../../images/figs/testfig.png"
        X = self.df.date[-120:]
        Y = self.df.atmo_cat[-120:]
        pred, color = self.mainWindow.getPredictions()
        f, ax = plt.subplots(figsize=(12, 10))
        plt.plot(X, Y, linestyle="-", marker='o', label="last 120h")
        lastDate = self.callingWindow.getLastDate()
        nextDate = getDateNext12h(lastDate)
        Xpred = to_datetime(np.array([nextDate]))
        Ypred = np.array([pred])
        ax.scatter(Xpred, Ypred, c="red", label="prediction")
        ax.set_title("Last 120h of ATMO index, and prediction for the next 12h")
        ax.set_xlabel("ATMO index")
        ax.set_ylabel("Date")
        ax.xaxis.set_major_formatter(myFmt)
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=10))
        ax.tick_params(axis='x', labelrotation=45)
        ax.legend()
        plt.savefig(path, dpi=60)
        return QPixmap(path)
