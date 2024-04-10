from .record import *
from .totxt import *
import time
from datetime import datetime

def audio_trigger_merge(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 1)
    print(f"record time: {(datetime.now() - start_time).total_seconds()} seconds")
    text = speech2txt(pipe, sample=byte_io.read())
    print(f"to text time: {(datetime.now() - start_time).total_seconds()} seconds")
    print('text: ', text)
    if "m" in text.lower() or "g" in text.lower():
        result_queue.put(True)
        print(f"total time: {(datetime.now() - start_time).total_seconds()} seconds")
    result_queue.put(False)
    done_event.set()


def audio_trigger_create(pipe, result_queue, done_event):
    start_time = datetime.now()
    byte_io = record(duration = 1)
    print(f"record time: {(datetime.now() - start_time).total_seconds()} seconds")
    text = speech2txt(pipe, sample=byte_io.read())
    print(f"to text time: {(datetime.now() - start_time).total_seconds()} seconds")
    print('text: ', text)
    if "c" in text.lower():
        result_queue.put(True)
        print(f"total time: {(datetime.now() - start_time).total_seconds()} seconds")
    result_queue.put(False)
    done_event.set()