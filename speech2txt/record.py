import sounddevice as sd
import numpy as np
from io import BytesIO
import soundfile as sf

def record(duration = 1):
    # duration = 1  # 录音时长，以秒为单位
    sample_rate = 16000  # 采样率

    # 录制音频
    print("start recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
    sd.wait()  # 等待录音结束
    print("end recording")

    # 将numpy数组转换为byte流
    byte_io = BytesIO()
    sf.write(byte_io, audio, sample_rate, format='WAV')
    
    # 将byte流作为输入传给speech2txt函数
    byte_io.seek(0)  # 重置读指针到开始位置

    return byte_io