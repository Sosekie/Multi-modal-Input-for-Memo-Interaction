from .record import *
from .totxt import *
from .similarity import *
from .voice import *
import time
from datetime import datetime

def audio_trigger_merge(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 2)
    noise_path2 = 'speech2txt/Recording/noise.wav'
    noise_simimarity = loudness_difference(byte_io, noise_path2)
    # print('🥝 - 🎼 - Merge voice: ', noise_simimarity)
    if noise_simimarity > 0.02:
        result_queue.put(True)
    result_queue.put(False)
    done_event.set()


def audio_trigger_create(pipe, result_queue, done_event):
    byte_io = record(duration = 2)
    noise_path2 = 'speech2txt/Recording/noise.wav'
    # print("🎵 - Saving...")
    noise_simimarity = loudness_difference(byte_io, noise_path2)
    # print('🍉 - 🎼 - Create voice: ', noise_simimarity)
    if noise_simimarity > 0.02:
        result_queue.put(True)
    else:
        result_queue.put(False)
    done_event.set()


def audio_trigger_open(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 2)
    noise_path2 = 'speech2txt/Recording/noise.wav'
    noise_simimarity = loudness_difference(byte_io, noise_path2)
    # print('🍑 - 🎼 - Open voice: ', noise_simimarity)
    if noise_simimarity > 0.02:
        result_queue.put(True)
    result_queue.put(False)
    done_event.set()
    

def audio_trigger_add(pipe, result_queue, done_event, memo):
    byte_io = record(duration = 2)
    byte_io.seek(0)
    audio_path2_add = 'speech2txt/Recording/fr_add.wav'
    audio_path2_close = 'speech2txt/Recording/fr_close.wav'
    noise_path2 = 'speech2txt/Recording/noise.wav'
    similarity_add = similarity(byte_io, audio_path2_add)
    similarity_close = similarity(byte_io, audio_path2_close)
    noise_simimarity = loudness_difference(byte_io, noise_path2)
    
    # print('🫐🥑 - 🎼 - Add: ', similarity_add,' - 🎼 - Close: ', similarity_close, ' - Noise: ', noise_simimarity)
    
    if (noise_simimarity > 0.02 and similarity_add > similarity_close) or not memo.is_finished:
        result_queue.put(1)
    elif (noise_simimarity > 0.02 and similarity_close > similarity_add) or memo.is_finished:
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