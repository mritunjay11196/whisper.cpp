from PyQt5.QtWidgets import QTextEdit

class TextBox(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setReadOnly(True) 
        self.setStyleSheet("font-size: 14px;")