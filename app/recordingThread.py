import os
import pyaudio
import wave
from PyQt5.QtCore import QThread, pyqtSignal
from transcriptionThread import TranscriptionThread
from pydub import AudioSegment
import io

class RecordingThread(QThread):
    update_status = pyqtSignal(str)
    update_transcription = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.recording = False
        self.audio = None
        self.stream = None
        self.frames = []

    def run(self):
        if self.recording:
            self.stop_recording()
            self.update_status.emit("Stopped recording")
            self.transcribe_audio()
        else:
            self.start_recording()
            self.update_status.emit("Started recording")

    def start_recording(self):
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=16000, 
                                      input=True,
                                      frames_per_buffer=1024,
                                      stream_callback=self.callback)
        self.frames = []
        self.stream.start_stream()
        self.recording = True

    def stop_recording(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
        self.recording = False

    def callback(self, in_data, frame_count, time_info, status):
        self.frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def transcribe_audio(self):
        try:
            # Process the audio in memory
            audio_data = b''.join(self.frames)
            audio_segment = AudioSegment(
                audio_data,
                sample_width=self.audio.get_sample_size(pyaudio.paInt16),
                frame_rate=16000,  
                channels=1
            )

            # Save the audio to an in-memory file
            audio_buffer = io.BytesIO()
            audio_segment.export(audio_buffer, format="wav")
            audio_buffer.seek(0)
            
            self.transcription_thread = TranscriptionThread(audio_buffer)
            self.transcription_thread.update_transcription.connect(self.update_transcription)
            self.transcription_thread.update_status.connect(self.update_status)
            self.transcription_thread.start()
        except Exception as e:
            self.update_status.emit(f"Error during transcription: {str(e)}")