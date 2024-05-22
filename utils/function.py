import threading
import time
from gesture.main import *
from speech2txt.main import *

# 初始化信号量，限制同时运行的线程数量为1
thread_semaphore = threading.Semaphore(1)

# 定义各个操作的锁
audio_thread_lock_merge = threading.Lock()
audio_thread_lock_create = threading.Lock()
audio_thread_lock_open = threading.Lock()
audio_thread_lock_add_close = threading.Lock()
audio_thread_lock_write = threading.Lock()

def print_active_threads():
    print("Active threads:")
    for thread in threading.enumerate():
        print(f"Thread name: {thread.name}, Thread ID: {thread.ident}")

def thread_wrapper(target, *args):
    with thread_semaphore:
        target(*args)

def merge(memo1, memo2, memo_list, opened_memo, audio_done_event_merge, last_audio_trigger_time_merge, audio_trigger_interval, result_queue, audio_pipe):
    current_time = time.time()
    if not audio_done_event_merge.is_set() and (current_time - last_audio_trigger_time_merge > audio_trigger_interval):
        with audio_thread_lock_merge:
            print('🥝 - Merge - Start Merge Command Recognition')
            last_audio_trigger_time_merge = current_time
            audio_done_event_merge.clear()
            audio_thread = threading.Thread(target=thread_wrapper, args=(audio_trigger_merge, audio_pipe, result_queue, audio_done_event_merge))
            audio_thread.start()
            print_active_threads()
    if audio_done_event_merge.is_set():
        recognition_result = result_queue.get()
        if recognition_result:
            print('🥝 - Merge - Using Merge Command to Merge Memo')
            memo1.merge(memo2)
            memo_list.remove(memo2)
            if memo2 == opened_memo:
                opened_memo = memo1
        audio_done_event_merge.clear()
    return memo_list, opened_memo, audio_done_event_merge, last_audio_trigger_time_merge, result_queue

def create(position, audio_done_event_create, last_audio_trigger_time_create, audio_trigger_interval, result_queue, audio_pipe):
    current_time = time.time()
    memo_new = None
    if audio_done_event_create.is_set():
        recognition_result = result_queue.get()
        if recognition_result:
            print('🍉 - Create - Using Create Command to Create Memo')
            memo_new = Memo(position)
        audio_done_event_create.clear()
    elif not audio_done_event_create.is_set() and (current_time - last_audio_trigger_time_create > audio_trigger_interval):
        with audio_thread_lock_create:
            print('🍉 - Create - Start Create Command Recognition')
            last_audio_trigger_time_create = current_time
            audio_done_event_create.clear()
            audio_thread = threading.Thread(target=thread_wrapper, args=(audio_trigger_create, audio_pipe, result_queue, audio_done_event_create))
            audio_thread.start()
            print_active_threads()
    return memo_new, audio_done_event_create, last_audio_trigger_time_create, result_queue

def open(opened_memo, pinched_memo, audio_done_event_open, last_audio_trigger_time_open, audio_trigger_interval, result_queue, audio_pipe):
    current_time = time.time()
    if not audio_done_event_open.is_set() and (current_time - last_audio_trigger_time_open > audio_trigger_interval):
        with audio_thread_lock_open:
            print('🍑 - Open - Start Open Command Recognition')
            last_audio_trigger_time_open = current_time
            audio_done_event_open.clear()
            audio_thread = threading.Thread(target=thread_wrapper, args=(audio_trigger_open, audio_pipe, result_queue, audio_done_event_open))
            audio_thread.start()
            print_active_threads()
    if audio_done_event_open.is_set():
        recognition_result = result_queue.get()
        if recognition_result:
            print('🍑 - Open - Open Memo')
            opened_memo = pinched_memo
        audio_done_event_open.clear()
    return opened_memo, audio_done_event_open, last_audio_trigger_time_open, result_queue

def add_close(opened_memo, memo, audio_done_event_add_close, last_audio_trigger_time_add_close, audio_trigger_interval, result_queue, audio_pipe):
    current_time = time.time()
    if not audio_done_event_add_close.is_set() and (current_time - last_audio_trigger_time_add_close > audio_trigger_interval):
        with audio_thread_lock_add_close:
            print('🫐🥑 - Add or Close - Start Command Recognition')
            last_audio_trigger_time_add_close = current_time
            audio_done_event_add_close.clear()
            audio_thread = threading.Thread(target=thread_wrapper, args=(audio_trigger_add, audio_pipe, result_queue, audio_done_event_add_close))
            audio_thread.start()
            print_active_threads()
    if audio_done_event_add_close.is_set():
        recognition_result = result_queue.get()
        if recognition_result == 1:
            print('🫐 - Add - Now You Can Speak Your Memo Content')
            memo.update_added(True)
        elif recognition_result == 2:
            print('🥑 - Close - Close Memo')
            opened_memo = None
        audio_done_event_add_close.clear()
    return opened_memo, audio_done_event_add_close, last_audio_trigger_time_add_close, result_queue

def write(memo, audio_done_event_write, last_audio_trigger_time_write, audio_trigger_interval, result_queue, audio_pipe):
    audio_trigger_interval = 10
    current_time = time.time()
    if not audio_done_event_write.is_set() and (current_time - last_audio_trigger_time_write > audio_trigger_interval):
        with audio_thread_lock_write:
            print('🥥 - Write - Start Write Command Recognition')
            last_audio_trigger_time_write = current_time
            audio_done_event_write.clear()
            audio_thread = threading.Thread(target=thread_wrapper, args=(audio_trigger_write, audio_pipe, result_queue, audio_done_event_write))
            audio_thread.start()
            print_active_threads()
    if audio_done_event_write.is_set():
        recognition_result = result_queue.get()
        if recognition_result:
            print('🥥 - Write - Writing Memo...')
            memo.update_content(recognition_result)
            memo.update_added(False)
        audio_done_event_write.clear()
    return audio_done_event_write, last_audio_trigger_time_write, result_queue


def add_memo_bar_to_frame(frame, memo, bar_height=200, bg_color=(255, 255, 255), text_color=(0, 0, 0), font_scale=0.5, thickness=1):
    height, width = frame.shape[:2]
    # bg_color = memo.color
    text_color = memo.font_color
    full_frame = np.zeros((height + bar_height, width, 3), dtype=np.uint8)
    full_frame[:height, :, :] = frame
    cv2.rectangle(full_frame, (0, height), (width, height + bar_height), bg_color, -1)

    vertical_position = height + 15
    
    cv2.putText(full_frame, memo.content, (10, vertical_position), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness)
    vertical_position += int(bar_height * 0.15)

    return full_frame


def add_status_bar_to_frame(frame, status_texts, bar_height=300, bg_color=(255, 255, 255), text_color=(0, 0, 0), font_scale=0.5, thickness=1):
    height, width = frame.shape[:2]
    full_frame = np.zeros((height + bar_height, width, 3), dtype=np.uint8)
    full_frame[:height, :, :] = frame
    cv2.rectangle(full_frame, (0, height), (width, height + bar_height), bg_color, -1)

    vertical_position = height + 15
    
    for text in status_texts:
        cv2.putText(full_frame, text, (10, vertical_position), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, thickness)
        vertical_position += int(bar_height * 0.15)

    return full_frame


class OutputStatus:
    def __init__(self, output_status = []):
        self.status = output_status
    
    def update_output_status(self, new_status):
        if len(self.status) >= 10:
            self.status = self.status[-9:]
        self.status.append(new_status)