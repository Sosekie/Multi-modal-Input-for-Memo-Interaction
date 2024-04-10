from gesture.main import *
from speech2txt.main import *
import threading
import queue


def test_1(memo1, memo2):
    memo1.merge(memo2)
    cv2.imshow("memo1", memo1.get_pic())
    cv2.imshow("memo2", memo2.get_pic())
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def merge(memo1, memo2, audio_done_event, last_audio_trigger_time, audio_trigger_interval, result_queue, audio_pipe):
    current_time = time.time()
    if not audio_done_event.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
        print('Now start audio recognition:')
        last_audio_trigger_time = current_time
        audio_done_event.clear()
        audio_thread = threading.Thread(target=audio_trigger_merge, args=(audio_pipe, result_queue, audio_done_event))
        audio_thread.start()
    if audio_done_event.is_set():
        recognition_result = result_queue.get()
        if recognition_result:
            print('Now using audio to merge memo:')
            memo1.merge(memo2)
            print('Merge is done!')
            print('----------------------------------')
        audio_done_event.clear()
    return audio_done_event, last_audio_trigger_time, result_queue


def create(position, audio_done_event, last_audio_trigger_time, audio_trigger_interval, result_queue, audio_pipe):
    current_time = time.time()
    memo_new = None
    if not audio_done_event.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
        print('Now start audio recognition:')
        last_audio_trigger_time = current_time
        audio_done_event.clear()
        audio_thread = threading.Thread(target=audio_trigger_create, args=(audio_pipe, result_queue, audio_done_event))
        audio_thread.start()
    if audio_done_event.is_set():
        recognition_result = result_queue.get()
        if recognition_result:
            print('Now using audio to create memo:')
            memo_new = Memo(position, "NEW")
            print('Create is done!')
            print('----------------------------------')
        audio_done_event.clear()
    return memo_new, audio_done_event, last_audio_trigger_time, result_queue


def start(memo_list, detector, audio_pipe):
    cap = cv2.VideoCapture(0)
    # threading event here
    audio_done_event_merge = threading.Event()
    audio_done_event_create = threading.Event()
    result_queue_merge = queue.Queue()
    result_queue_create = queue.Queue()
    last_audio_trigger_time = 0
    audio_trigger_interval = 3

    memo_new = None     # a memo that is not settled
    while True:
        ret, frame = cap.read()
        if ret:
            frame = np.array(frame[:, ::-1, :], dtype=np.uint8)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            detection_result = detector.detect(mp_image)
            if detection_result:
                frame = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)
                
                # Merge memo function
                triggered_memo_list = [memo for memo in memo_list if memo.is_triggered(detection_result, frame)][:2]   # the first 2 triggered memos
                highlight_memo(frame, triggered_memo_list)
                if len(triggered_memo_list) == 2:
                    audio_done_event_merge, last_audio_trigger_time, result_queue_merge = merge(triggered_memo_list[0], triggered_memo_list[1], audio_done_event_merge, last_audio_trigger_time, audio_trigger_interval, result_queue_merge, audio_pipe)
                
                # Create memo function
                position = is_pinched(detection_result)
                if position:
                    position = [int(position[0]*frame.shape[1]), int(position[1]*frame.shape[0])]   # the position from detection_result is a float [0,1], we need int

                    # if memo_new already exist, change its position, else create a new memo
                    if memo_new:
                        memo_new.update_position(position)
                        add_memo(frame, [memo_new])
                    else:
                        memo_new, audio_done_event_create, last_audio_trigger_time, result_queue_create = create(position, audio_done_event_create, last_audio_trigger_time, audio_trigger_interval, result_queue_create, audio_pipe)
                elif memo_new:
                    memo_list.append(memo_new)
                    memo_new = None

            frame = add_memo(frame, memo_list)

            cv2.imshow("camera", frame)
        # press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    # initialize
    model_id = ["openai/whisper-base", "openai/whisper-large-v3"]
    audio_pipe = model_initialize(model_id[0])
    memo1 = Memo([0, 0], "A")
    # memo2 = Memo([0, 600], "B")
    memo_list = [memo1]
    detector = detector_init()

    start(memo_list, detector, audio_pipe)