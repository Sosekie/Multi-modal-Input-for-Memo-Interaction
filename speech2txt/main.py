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
    print('🎼 - Merge: ', text)
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
    print('🎼 - Create: ', text)
    if "c" in text.lower() or "t" in text.lower():
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
    print('🎼 - Open: ', text)
    if "o" in text.lower() or "p" in text.lower() or "n" in text.lower():
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
    print('🎼 - Add: ', text)
    if "a" in text.lower() or "d" in text.lower():
        result_queue.put(True)
        # print(f"total time: {(datetime.now() - start_time).total_seconds()} seconds")
    result_queue.put(False)
    done_event.set()


def audio_trigger_write(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 5)
    # print(f"record time: {(datetime.now() - start_time).total_seconds()} seconds")
    text = speech2txt(pipe, sample=byte_io.read())
    # print(f"to text time: {(datetime.now() - start_time).total_seconds()} seconds")
    print('👣 - Write: ', text)
    result_queue.put(text)
    # print(f"total time: {(datetime.now() - start_time).total_seconds()} seconds")
    done_event.set()


# to do
def audio_trigger_close(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 2)
    # print(f"record time: {(datetime.now() - start_time).total_seconds()} seconds")
    text = speech2txt(pipe, sample=byte_io.read())
    # print(f"to text time: {(datetime.now() - start_time).total_seconds()} seconds")
    print('🎼 - Text: ', text)
    if "c" in text.lower() or "t" in text.lower():
        result_queue.put(True)
        # print(f"total time: {(datetime.now() - start_time).total_seconds()} seconds")
    result_queue.put(False)
    done_event.set()