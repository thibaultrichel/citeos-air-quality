import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from AirQualityUI.utils.model_integration import label_positions, advices, colors


class UserWindow(QMainWindow):
    def __init__(self, callingWindow: QMainWindow):
        super(UserWindow, self).__init__()

        self.callingWindow = callingWindow

        self.WIDTH = 500
        self.HEIGHT = 300

        self.setFixedSize(self.WIDTH, self.HEIGHT)
        self.setWindowTitle("CiteosVision - User Window")
        self.setGeometry(
            round(self.callingWindow.screenWidth / 2 - self.WIDTH / 2),
            round(self.callingWindow.screenHeight / 2 - self.HEIGHT / 2),
            self.WIDTH, self.HEIGHT
        )

        self.set_basic_ui()

        self.rectangles = {}
        for i, c in enumerate(colors):
            rect = QLabel(self)
            rect.setGeometry(25 + i*75, 90, 75, 20)
            rect.setStyleSheet(f"background-color: {c}")
            self.rectangles[c] = rect

        self.btnPredict = QPushButton("Predict", self)
        self.btnPredict.setGeometry(int(self.WIDTH / 2 - 100 / 2), self.HEIGHT - 50, 100, 30)
        self.btnPredict.clicked.connect(self.displayPredictions)

        self.labelResult = QLabel(self)
        self.labelResult.setFont(self.callingWindow.boldFont)
        self.labelResult.setGeometry(0, 0, 50, 50)
        self.labelResult.setAlignment(Qt.AlignCenter)
        self.labelResult.setVisible(False)

        self.arrowPixmap = QPixmap("../../images/arrow.png")
        self.arrow = QLabel(self)
        self.arrow.setPixmap(self.arrowPixmap)
        self.arrow.setVisible(False)

        self.textAdvice = QLabel("Conseil :", self)
        self.textAdvice.setGeometry(20, 200, 70, 30)
        self.textAdvice.setFont(self.callingWindow.boldFont)
        self.textAdvice.setVisible(False)

        self.adviceLabel = QLabel(self)
        self.adviceLabel.setGeometry(90, 200, 500, 30)
        self.adviceLabel.setFont(self.callingWindow.italicFont)
        self.adviceLabel.setVisible(False)

    def set_basic_ui(self):
        title = QLabel("UserVision", self)
        title.setGeometry(round(self.WIDTH / 2 - 200 / 2), 10, 200, 40)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(self.callingWindow.titleFont)

    def closeEvent(self, event):
        self.callingWindow.show()
        self.close()

    def displayPredictions(self):
        value, color = self.callingWindow.getPredictions()
        radius = int(max([self.labelResult.width(), self.labelResult.height()]) / 2)
        intval = np.round(value)
        x, y = label_positions[intval]
        self.labelResult.setText(str(value))
        self.labelResult.move(x, y)
        self.arrow.setGeometry(x + 15, y - 20, self.arrowPixmap.width(), self.arrowPixmap.height())
        self.labelResult.setStyleSheet(f"color: black; background-color: {color}; border-radius: {radius}px; "
                                       f"border: 2px solid black")
        self.adviceLabel.setText(advices[intval])
        self.labelResult.setVisible(True)
        self.arrow.setVisible(True)
        self.adviceLabel.setVisible(True)
        self.textAdvice.setVisible(True)

