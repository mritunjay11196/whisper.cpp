import os
import pyaudio
import wave
from PyQt5.QtWidgets import QPushButton, QApplication, QTextEdit
from recordingThread import RecordingThread

class PushButton(QPushButton):
    def __init__(self, label, main_window, parent=None):
        super().__init__(label, parent)
        self.main_window = main_window
        self.recording_thread = RecordingThread()  
        self.recording_thread.update_status.connect(self.main_window.setPlainText)
        self.recording_thread.update_transcription.connect(self.main_window.setTranscription)
        self.initUI()

    def initUI(self):
        self.clicked.connect(self.on_click)

    def on_click(self):
        self.recording_thread.start()