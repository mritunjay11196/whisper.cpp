import os
import pyaudio
import wave
import subprocess
import tempfile
import time

# ─── Configuration ──────────────────────────────────────────────────────────

# Calculate project root and paths dynamically
WHISPER_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WHISPER_CLI = os.path.join(WHISPER_ROOT, "build", "bin", "whisper-cli")
MODEL_PATH = os.path.join(WHISPER_ROOT, "models", "ggml-base.en.bin")

# Recording settings
CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16-bit
CHANNELS = 1              # mono
RATE = 16000              # 16 kHz
RECORD_SECONDS = 5        # record duration

# ─── Recording Function ─────────────────────────────────────────────────────

def record_to_wav(path, device_index=None):
    pa = pyaudio.PyAudio()
    stream_kwargs = dict(format=FORMAT, channels=CHANNELS, rate=RATE,
                         input=True, frames_per_buffer=CHUNK)
    if device_index is not None:
        stream_kwargs["input_device_index"] = device_index

    stream = pa.open(**stream_kwargs)
    print(f"🎙️ Recording for {RECORD_SECONDS} seconds...")
    frames = [stream.read(CHUNK) for _ in range(int(RATE / CHUNK * RECORD_SECONDS))]
    print("✅ Recording complete.")

    stream.stop_stream()
    stream.close()
    pa.terminate()

    with wave.open(path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pa.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    print(f"✔️ Saved WAV to {path}")

# ─── Transcription Function ─────────────────────────────────────────────────

def transcribe(path):
    cmd = [
        WHISPER_CLI,
        "-f", path,
        "-m", MODEL_PATH,
        "-t", "8",
        "--beam-size", "1",
        "--best-of", "1",
        "--no-timestamps"
    ]

    start_time = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True)
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"time: {elapsed:.2f} seconds")
    print(result.stdout)

# ─── Main Routine ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
        wav_path = tf.name
    try:
        record_to_wav(wav_path)
        transcribe(wav_path)
    finally:
        os.remove(wav_path)