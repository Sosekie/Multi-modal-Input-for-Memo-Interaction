import pyaudio
import wave

# 定义音频文件参数
FORMAT = pyaudio.paInt16 # 音频格式
CHANNELS = 1 # 声道数
RATE = 44100 # 采样率
CHUNK = 1024 # 块大小
RECORD_SECONDS = 5 # 录音时间
WAVE_OUTPUT_FILENAME = "output.wav" # 输出文件名

audio = pyaudio.PyAudio()

# 开始录音
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print("recording...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("finished recording")

# 停止录音
stream.stop_stream()
stream.close()
audio.terminate()

# 保存录音文件
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()