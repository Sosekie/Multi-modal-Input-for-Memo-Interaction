from gesture.main import *
from speech2txt.main import *
import threading


def merge(memo1, memo2, audio_done_event, last_audio_trigger_time, audio_trigger_interval, result_queue, audio_pipe):
    current_time = time.time()
    if not audio_done_event.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
        print('🥝 - Merge - Start Merge Command Recognition')
        last_audio_trigger_time = current_time
        audio_done_event.clear()
        audio_thread = threading.Thread(target=audio_trigger_merge, args=(audio_pipe, result_queue, audio_done_event))
        audio_thread.start()
    if audio_done_event.is_set():
        recognition_result = result_queue.get()
        if recognition_result:
            print('🥝 - Merge - Using Merge Command to Merge Memo')
            memo1.merge(memo2)
        audio_done_event.clear()
    return audio_done_event, last_audio_trigger_time, result_queue


def create(position, audio_done_event, last_audio_trigger_time, audio_trigger_interval, result_queue, audio_pipe):
    current_time = time.time()
    memo_new = None
    if not audio_done_event.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
        print('🍉 - Create - Start Create Command Recognition')
        last_audio_trigger_time = current_time
        audio_done_event.clear()
        audio_thread = threading.Thread(target=audio_trigger_create, args=(audio_pipe, result_queue, audio_done_event))
        audio_thread.start()
    if audio_done_event.is_set():
        recognition_result = result_queue.get()
        if recognition_result:
            print('🍉 - Create - Using Create Command to Create Memo')
            memo_new = Memo(position)
        audio_done_event.clear()
    return memo_new, audio_done_event, last_audio_trigger_time, result_queue


def open(memo, memo_list, audio_done_event, last_audio_trigger_time, audio_trigger_interval, result_queue, audio_pipe):
    current_time = time.time()
    if not audio_done_event.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
        print('🍑 - Open - Start Open Command Recognition')
        last_audio_trigger_time = current_time
        audio_done_event.clear()
        audio_thread = threading.Thread(target=audio_trigger_open, args=(audio_pipe, result_queue, audio_done_event))
        audio_thread.start()
    if audio_done_event.is_set():
        recognition_result = result_queue.get()
        if recognition_result:
            print('🍑 - Open - Open Memo')
            for mm in memo_list:
                mm.update_opened(False)
            memo.update_opened(True)
        audio_done_event.clear()
    return audio_done_event, last_audio_trigger_time, result_queue


def add(memo, audio_done_event, last_audio_trigger_time, audio_trigger_interval, result_queue, audio_pipe):
    current_time = time.time()
    if not audio_done_event.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
        print('🫐 - Add - Start Add Command Recognition')
        last_audio_trigger_time = current_time
        audio_done_event.clear()
        audio_thread = threading.Thread(target=audio_trigger_add, args=(audio_pipe, result_queue, audio_done_event))
        audio_thread.start()
    if audio_done_event.is_set():
        recognition_result = result_queue.get()
        if recognition_result:
            print('🫐 - Add - Now You Can Speak Your Memo Content')
            memo.update_added(True)
        audio_done_event.clear()
    return audio_done_event, last_audio_trigger_time, result_queue


def write(memo, audio_done_event, last_audio_trigger_time, audio_trigger_interval, result_queue, audio_pipe):
    current_time = time.time()
    if not audio_done_event.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
        print('🥥 - Write - Start Write Command Recognition')
        last_audio_trigger_time = current_time
        audio_done_event.clear()
        audio_thread = threading.Thread(target=audio_trigger_write, args=(audio_pipe, result_queue, audio_done_event))
        audio_thread.start()
    if audio_done_event.is_set():
        recognition_result = result_queue.get()
        if recognition_result:
            print('🥥 - Write - Writing Memo...')
            memo.update_content(recognition_result)
            memo.update_added(False)
        audio_done_event.clear()
    return audio_done_event, last_audio_trigger_time, result_queue


# to do
def close(memo, audio_done_event, last_audio_trigger_time, audio_trigger_interval, result_queue, audio_pipe):
    current_time = time.time()
    if not audio_done_event.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
        print('Now start audio recognition:')
        last_audio_trigger_time = current_time
        audio_done_event.clear()
        audio_thread = threading.Thread(target=audio_trigger_close, args=(audio_pipe, result_queue, audio_done_event))
        audio_thread.start()
    if audio_done_event.is_set():
        recognition_result = result_queue.get()
        if recognition_result:
            print('Now using audio to create memo:')
            memo.update_content(recognition_result)
            print('Create is done!')
            print('----------------------------------')
        audio_done_event.clear()
    return audio_done_event, last_audio_trigger_time, result_queue