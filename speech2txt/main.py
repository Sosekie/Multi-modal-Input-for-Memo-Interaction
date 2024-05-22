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
    simimarity = similarity(byte_io, audio_path2)
    print('🥝 - 🎼 - Merge: ', simimarity)
    if simimarity > 0.5:
        result_queue.put(True)
    result_queue.put(False)
    done_event.set()


def audio_trigger_create(pipe, result_queue, done_event):
    byte_io = record(duration=1)
    audio_path2 = 'speech2txt/Recording/create.wav'
    simimarity = similarity(byte_io, audio_path2)
    print('🍉 - 🎼 - Create: ', simimarity)
    if simimarity > 0.5:
        result_queue.put(True)
    else:
        result_queue.put(False)
    done_event.set()


def audio_trigger_open(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 1)
    # text = speech2txt(pipe, sample=byte_io.read())
    audio_path2 = 'speech2txt/Recording/open.wav'
    simimarity = similarity(byte_io, audio_path2)
    print('🍑 - 🎼 - Open: ', simimarity)
    if simimarity > 0.5:
        result_queue.put(True)
    result_queue.put(False)
    done_event.set()
    

def audio_trigger_add(pipe, result_queue, done_event):
    byte_io = record(duration=1)
    byte_io.seek(0)
    audio_path2_add = 'speech2txt/Recording/add.wav'
    audio_path2_close = 'speech2txt/Recording/close.wav'

    similarity_add = similarity(byte_io, audio_path2_add)
    similarity_close = similarity(byte_io, audio_path2_close)
    
    print('🫐 - 🎼 - Add: ', similarity_add,' - 🎼 - Close: ', similarity_close)
    
    if similarity_add > 0.5 and similarity_add-0.2 > similarity_close:
        result_queue.put(1)
    elif similarity_close > 0.5 and similarity_close > similarity_add-0.2:
        result_queue.put(2)
    else:
        result_queue.put(0)
    
    done_event.set()

def audio_trigger_write(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 5)
    text = speech2txt(pipe, sample=byte_io.read())
    print('🥥 - 👣 - Write: ', text)
    result_queue.put(text)
    done_event.set()