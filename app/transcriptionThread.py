import os
from PyQt5.QtCore import QThread, pyqtSignal
import time
import io
import wave
import numpy as np
import subprocess
import tempfile

# Calculate project root and paths dynamically
WHISPER_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WHISPER_CLI = os.path.join(WHISPER_ROOT, "build", "bin", "whisper-cli")
MODEL_PATH = os.path.join(WHISPER_ROOT, "models", "ggml-base.en.bin")

class TranscriptionThread(QThread):
    update_transcription = pyqtSignal(str)
    update_status = pyqtSignal(str)

    def __init__(self, audio_buffer, parent=None):
        super().__init__(parent)
        self.audio_buffer = audio_buffer

    def run(self):
        self.update_status.emit("Transcription in progress...")
        transcription_start = time.time()
        
        try:
            # Read the audio buffer as a wave file
            self.audio_buffer.seek(0)  
            with wave.open(self.audio_buffer, 'rb') as wf:
                params = wf.getparams()
                audio_data = wf.readframes(wf.getnframes())

            # Write audio_data to a temporary WAV file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
                wav_path = tf.name
                with wave.open(tf, 'wb') as wf_out:
                    wf_out.setparams(params)
                    wf_out.writeframes(audio_data)

            # Transcribe using whisper-cli
            cmd = [
                WHISPER_CLI,
                "-f", wav_path,
                "-m", MODEL_PATH,
                "-t", "8",
                "--beam-size", "1",
                "--best-of", "1",
                "--no-timestamps"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            transcription = result.stdout.strip()
            elapsed = time.time() - transcription_start
            self.update_transcription.emit(transcription)
            self.update_status.emit(f"Transcription complete. Time taken: {elapsed:.2f} seconds.")

        except Exception as e:
            self.update_status.emit(f"Error during transcription: {str(e)}")
            print(f"Error during transcription: {str(e)}")
        finally:
            # Clean up temp file
            try:
                if 'wav_path' in locals() and os.path.exists(wav_path):
                    os.remove(wav_path)
            except Exception:
                pass