from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TechWindow(QMainWindow):
    def __init__(self, callingWindow: QMainWindow):
        super(TechWindow, self).__init__()

        self.callingWindow = callingWindow
        self.callingWindow.setVisible(False)
        desktop = QApplication.desktop()
        screenRect = desktop.screenGeometry()
        screenHeight = screenRect.height()
        screenWidth = screenRect.width()

        self.WIDTH = 500
        self.HEIGHT = 200

        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("CiteosVision - Technical Window")
        self.setGeometry(
            round(screenWidth / 2 - self.WIDTH / 2),
            round(screenHeight / 2 - self.HEIGHT / 2),
            self.WIDTH, self.HEIGHT
        )

        self.modelPath = "/home/thibault/Bureau/citeos-air-quality/models/LSTM_multi_with_target.h5"
        self.csvUrl = "https://raw.githubusercontent.com/thibaultrichel/citeos-air-quality/main/data/final/merged" \
                      "-final.csv "
        self.df = None

        self.set_basic_ui()

    def set_basic_ui(self):
        label = QLabel("TECH", self)
        label.setGeometry(int(self.WIDTH/2 - 50), int(self.HEIGHT/2), 100, 30)
        label.setAlignment(Qt.AlignCenter)

    def closeEvent(self, event):
        self.callingWindow.show()
        self.close()
