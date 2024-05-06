import sounddevice as sd
import numpy as np
from io import BytesIO
import soundfile as sf

def record(duration = 3):
    sample_rate = 16000

    print("🎵 - Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()

    byte_io = BytesIO()
    sf.write(byte_io, audio, sample_rate, format='WAV')

    byte_io.seek(0)

    return byte_io