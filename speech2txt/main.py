from .record import *
from .totxt import *
from .similarity import *
import time
from datetime import datetime

def audio_trigger_merge(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 1)
    # text = speech2txt(pipe, sample=byte_io.read())
    audio_path2 = 'speech2txt/Recording/merge.wav'
    noise_path2 = 'speech2txt/Recording/noise.wav'
    simimarity = similarity(byte_io, audio_path2)
    noise_simimarity = similarity(byte_io, noise_path2)
    print('🥝 - 🎼 - Merge: ', simimarity, ' - Noise: ', noise_simimarity)
    if simimarity > 0.07 and noise_simimarity < 0.02:
        result_queue.put(True)
    result_queue.put(False)
    done_event.set()


def audio_trigger_create(pipe, result_queue, done_event):
    byte_io = record(duration = 1)
    audio_path2 = 'speech2txt/Recording/create.wav'
    noise_path2 = 'speech2txt/Recording/noise.wav'
    print("🎵 - Saving...")
    simimarity = similarity(byte_io, audio_path2)
    noise_simimarity = similarity(byte_io, noise_path2)
    print('🍉 - 🎼 - Create: ', simimarity, ' - Noise: ', noise_simimarity)
    if simimarity > 0.10 and noise_simimarity < 0.02:
        result_queue.put(True)
    else:
        result_queue.put(False)
    done_event.set()


def audio_trigger_open(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 1)
    audio_path2 = 'speech2txt/Recording/open.wav'
    noise_path2 = 'speech2txt/Recording/noise.wav'
    simimarity = similarity(byte_io, audio_path2)
    noise_simimarity = similarity(byte_io, noise_path2)
    print('🍑 - 🎼 - Open: ', simimarity, ' - Noise: ', noise_simimarity)
    if simimarity > 0.06 and noise_simimarity < 0.02:
        result_queue.put(True)
    result_queue.put(False)
    done_event.set()
    

def audio_trigger_add(pipe, result_queue, done_event, memo):
    byte_io = record(duration = 1)
    byte_io.seek(0)
    audio_path2_add = 'speech2txt/Recording/add.wav'
    audio_path2_close = 'speech2txt/Recording/close.wav'
    noise_path2 = 'speech2txt/Recording/noise.wav'
    similarity_add = similarity(byte_io, audio_path2_add)
    similarity_close = similarity(byte_io, audio_path2_close)
    noise_simimarity = similarity(byte_io, noise_path2)
    
    print('🫐🥑 - 🎼 - Add: ', similarity_add,' - 🎼 - Close: ', similarity_close, ' - Noise: ', noise_simimarity)
    
    if similarity_add > 0.10 and noise_simimarity < similarity_add and similarity_add > similarity_close-0.03 and not memo.is_finished:
        result_queue.put(1)
    elif similarity_close > 0.12 and noise_simimarity < 0.02:
        result_queue.put(2)
    else:
        result_queue.put(3)
    
    done_event.set()

def audio_trigger_write(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 5)
    text = speech2txt(pipe, sample=byte_io.read())
    print('🥥 - 👣 - Write: ', text)
    result_queue.put(text)
    done_event.set()