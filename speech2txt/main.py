from .record import *
from .totxt import *
import time
from datetime import datetime

def audio_trigger_merge(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 2)
    # print(f"record time: {(datetime.now() - start_time).total_seconds()} seconds")
    text = speech2txt(pipe, sample=byte_io.read())
    # print(f"to text time: {(datetime.now() - start_time).total_seconds()} seconds")
    print('🥝 - 🎼 - Merge: ', text)
    if "m" in text.lower() or "g" in text.lower():
        result_queue.put(True)
        # print(f"total time: {(datetime.now() - start_time).total_seconds()} seconds")
    result_queue.put(False)
    done_event.set()


def audio_trigger_create(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 2)
    # print(f"record time: {(datetime.now() - start_time).total_seconds()} seconds")
    text = speech2txt(pipe, sample=byte_io.read())
    # print(f"to text time: {(datetime.now() - start_time).total_seconds()} seconds")
    print('🍉 - 🎼 - Create: ', text)
    if "create" in text.lower() or "new" in text.lower():
        result_queue.put(True)
        # print(f"total time: {(datetime.now() - start_time).total_seconds()} seconds")
    result_queue.put(False)
    done_event.set()


def audio_trigger_open(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 2)
    # print(f"record time: {(datetime.now() - start_time).total_seconds()} seconds")
    text = speech2txt(pipe, sample=byte_io.read())
    # print(f"to text time: {(datetime.now() - start_time).total_seconds()} seconds")
    print('🍑 - 🎼 - Open: ', text)
    if "open" in text.lower():
        result_queue.put(True)
        # print(f"total time: {(datetime.now() - start_time).total_seconds()} seconds")
    result_queue.put(False)
    done_event.set()
    

def audio_trigger_add(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 2)
    # print(f"record time: {(datetime.now() - start_time).total_seconds()} seconds")
    text = speech2txt(pipe, sample=byte_io.read())
    # print(f"to text time: {(datetime.now() - start_time).total_seconds()} seconds")
    print('🫐 - 🎼 - Add: ', text)
    if "add" in text.lower():
        result_queue.put(1)
        # print(f"total time: {(datetime.now() - start_time).total_seconds()} seconds")
    elif "close" in text.lower():
        result_queue.put(2)
    else:
        result_queue.put(0)
    done_event.set()


def audio_trigger_write(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 5)
    # print(f"record time: {(datetime.now() - start_time).total_seconds()} seconds")
    text = speech2txt(pipe, sample=byte_io.read())
    # print(f"to text time: {(datetime.now() - start_time).total_seconds()} seconds")
    print('🥥 - 👣 - Write: ', text)
    result_queue.put(text)
    # print(f"total time: {(datetime.now() - start_time).total_seconds()} seconds")
    done_event.set()