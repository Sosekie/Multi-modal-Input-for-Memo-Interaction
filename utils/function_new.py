import threading
import time
from gesture.main import *
from speech2txt.main import *

def merge(memo1, memo2, memo_list, opened_memo, audio_done_event_merge, last_audio_trigger_time, audio_trigger_interval, result_queue_merge):
    current_time = time.time()
    if not audio_done_event_merge.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
        print('🥝 - Merge - Start Merge Command Recognition')
        audio_trigger_merge(result_queue_merge, audio_done_event_merge)
        last_audio_trigger_time = current_time
        audio_done_event_merge.clear()
    if audio_done_event_merge.is_set():
        recognition_result = result_queue_merge.get()
        if recognition_result:
            print('🥝 - Merge - Using Merge Command to Merge Memo')
            memo1.merge(memo2)
            memo_list.remove(memo2)
            if memo2 == opened_memo:
                opened_memo = memo1
        audio_done_event_merge.clear()
    return memo_list, opened_memo, last_audio_trigger_time

def create(position, last_audio_trigger_time, audio_trigger_interval, result_queue_create, audio_done_event_create):
    current_time = time.time()
    memo_new = None
    print('audio_done_event_create.is_set(): ', audio_done_event_create.is_set())
    if audio_done_event_create.is_set():
        print('hello')
        recognition_result = result_queue_create.get()
        if recognition_result:
            print('🍉 - Create - Using Create Command to Create Memo')
            memo_new = Memo(position)
        audio_done_event_create.clear()
    elif not audio_done_event_create.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
        print('🍉 - Create - Start Create Command Recognition')
        audio_trigger_create(result_queue_create, audio_done_event_create)
        last_audio_trigger_time = current_time
        audio_done_event_create.clear()
    return memo_new, last_audio_trigger_time

def open(opened_memo, pinched_memo, audio_done_event_open, last_audio_trigger_time, audio_trigger_interval, result_queue_open):
    current_time = time.time()
    if not audio_done_event_open.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
        print('🍑 - Open - Start Open Command Recognition')
        audio_trigger_open(result_queue_open, audio_done_event_open)
        last_audio_trigger_time = current_time
        audio_done_event_open.clear()
    if audio_done_event_open.is_set():
        recognition_result = result_queue_open.get()
        if recognition_result:
            print('🍑 - Open - Open Memo')
            opened_memo = pinched_memo
        audio_done_event_open.clear()
    return opened_memo, last_audio_trigger_time

def add_close(opened_memo, memo, audio_done_event_add_close, last_audio_trigger_time, audio_trigger_interval, result_queue_add_close):
    current_time = time.time()
    if not audio_done_event_add_close.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
        print('🫐🥑 - Add or Close - Start Command Recognition')
        audio_trigger_add(result_queue_add_close, audio_done_event_add_close)
        last_audio_trigger_time = current_time
        audio_done_event_add_close.clear()
    if audio_done_event_add_close.is_set():
        recognition_result = result_queue_add_close.get()
        if recognition_result == 1 and not memo.is_added:
            print('🫐 - Add - Now You Can Speak Your Memo Content')
            memo.update_added(True)
        elif recognition_result == 2:
            print('🥑 - Close - Close Memo')
            opened_memo = None
        audio_done_event_add_close.clear()
    return opened_memo, last_audio_trigger_time

def write(memo, audio_pipe, audio_done_event_write, last_audio_trigger_time, audio_trigger_interval, result_queue_write):
    if audio_trigger_interval > 10:
        audio_trigger_interval = 10
    current_time = time.time()
    if not audio_done_event_write.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
        print('🥥 - Write - Start Write Command Recognition')
        audio_trigger_write(audio_pipe, result_queue_write, audio_done_event_write)
        last_audio_trigger_time = current_time
        audio_done_event_write.clear()
    if audio_done_event_write.is_set():
        recognition_result = result_queue_write.get()
        if recognition_result:
            print('🥥 - Write - Writing Memo...')
            memo.update_content(recognition_result)
            memo.update_added(False)
        audio_done_event_write.clear()
    return last_audio_trigger_time
