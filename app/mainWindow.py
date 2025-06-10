from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget
from pushButton import PushButton
from textBox import TextBox
from recordingThread import RecordingThread

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.recording_thread = RecordingThread()  
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        self.button = PushButton('Click Me', self)
        
        self.textbox = TextBox(self)
      
        layout = QGridLayout()
        layout.addWidget(self.button, 0, 0)
        layout.addWidget(self.textbox, 1, 0)
        
        central_widget.setLayout(layout)
        
        self.resize(400, 400)

    def setPlainText(self, text):
        self.statusBar().showMessage(text)

    def setTranscription(self, text):
        self.textbox.setPlainText(text)