import pyaudio
import wave

# 录音参数
FORMAT = pyaudio.paInt16  # 音频格式
CHANNELS = 1  # 单声道
RATE = 44100  # 采样率
CHUNK = 1024  # 每次读取的帧数
RECORD_SECONDS = 1  # 录音时间（秒）
OUTPUT_FILENAME = "speech2txt/Recording/merge.wav"  # 输出文件名

# 创建PyAudio对象
audio = pyaudio.PyAudio()

# 打开流
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

# 存储音频数据
frames = []

# 开始录音
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Finished recording.")

# 停止录音
stream.stop_stream()
stream.close()
audio.terminate()

# 保存音频文件为WAV格式
with wave.open(OUTPUT_FILENAME, 'wb') as wf:
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))

print(f"Audio recorded and saved as {OUTPUT_FILENAME}")
