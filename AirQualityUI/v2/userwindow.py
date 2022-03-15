import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from AirQualityUI.utils.model_integration import getPredictions, formatDataframe


class UserWindow(QMainWindow):
    def __init__(self, callingWindow: QMainWindow):
        super(UserWindow, self).__init__()

        self.callingWindow = callingWindow
        self.callingWindow.setVisible(False)
        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry()
        screenHeight = screenRect.height()
        screenWidth = screenRect.width()

        self.WIDTH = 500
        self.HEIGHT = 200

        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("CiteosVision - User Window")
        self.setGeometry(
            round(screenWidth / 2 - self.WIDTH / 2),
            round(screenHeight / 2 - self.HEIGHT / 2),
            self.WIDTH, self.HEIGHT
        )

        # self.modelPath = "/home/thibault/Bureau/citeos-air-quality/models/LSTM_multi_with_target.h5"
        # self.csvUrl = "https://raw.githubusercontent.com/thibaultrichel/citeos-air-quality/main/data/final/merged" \
        #               "-final.csv "

        self.set_basic_ui()

        colors = ["cyan", "green", "yellow", "orange", "red", "purple"]
        self.rectangles = {}
        for i, c in enumerate(colors):
            rect = QLabel(self)
            rect.setGeometry(25 + i*75, 90, 75, 20)
            rect.setStyleSheet(f"background-color: {c}")
            self.rectangles[c] = rect

        self.btnPredict = QPushButton("Predict", self)
        self.btnPredict.setGeometry(50, 20, 100, 30)
        self.btnPredict.clicked.connect(self.callingWindow.displayPredictions)

    def set_basic_ui(self):
        label = QLabel("USER", self)
        label.setGeometry(0, 0, 50, 15)

    def closeEvent(self, event):
        self.callingWindow.show()
        self.close()
