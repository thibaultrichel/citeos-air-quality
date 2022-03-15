from PyQt5.QtGui import QFont


class MyFont(QFont):
    def __init__(self, size, bold, italic, underline):
        super(MyFont, self).__init__()
        self.setPointSize(size)
        self.setBold(bold)
        self.setItalic(italic)
        self.setUnderline(underline)
