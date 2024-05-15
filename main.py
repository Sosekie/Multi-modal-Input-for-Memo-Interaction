from gesture.main import *
from speech2txt.main import *
import threading
import queue
from utils.function import merge, create, open, add, write, close, add_memo_bar_to_frame, add_status_bar_to_frame, OutputStatus

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import time

# global variable
memo_new = None
detection_result_new = None


def start(memo_list, audio_pipe):
    global memo_new
    global detection_result_new

    cap = cv2.VideoCapture(0)
    # threading event here
    audio_done_event_merge, audio_done_event_create, audio_done_event_open, audio_done_event_add, audio_done_event_write, audio_done_event_close = threading.Event(), threading.Event(), threading.Event(), threading.Event(), threading.Event(), threading.Event()
    result_queue_merge, result_queue_create, result_queue_open, result_queue_add, result_queue_write, result_queue_close = queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue()
    last_audio_trigger_time = 0
    audio_trigger_interval = 1

    # Create a hand landmarker instance with the live stream mode
    base_options = python.BaseOptions(model_asset_path='./gesture/hand_landmarker.task')
    running_mode = vision.RunningMode.LIVE_STREAM

    options = vision.HandLandmarkerOptions(base_options=base_options,
                                           running_mode=running_mode,
                                           result_callback=result_callback,
                                           min_hand_detection_confidence=0.2,
                                           min_hand_presence_confidence=0.9,
                                           num_hands=2)

    # video stream
    with vision.HandLandmarker.create_from_options(options) as detector:
        triggered_memo_list = []
        pinched_memo_list = [None, None]

        while True:
            ret, frame = cap.read()
            if ret:
                height, width = frame.shape[:2]
                new_width = int(width * 1.3)
                new_height = int(height * 1.3)
                frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

                frame = np.array(frame[:, ::-1, :], dtype=np.uint8)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
                timestamp = int(round(time.time() * 1000))
                detector.detect_async(mp_image, timestamp)
                while detection_result_new is None:
                    pass
                detection_result = detection_result_new
                detection_result_new = None

                if detection_result:
                    frame = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)

                    hand_landmarks_list = detection_result.hand_landmarks
                    handedness_list = detection_result.handedness

                    # Merge memo
                    triggered_memo_list = get_triggered_memo_list(memo_list, hand_landmarks_list, frame, max_triggered=2)
                    if len(triggered_memo_list) >= 2:
                        audio_done_event_merge, last_audio_trigger_time, result_queue_merge = merge(triggered_memo_list[0], triggered_memo_list[1], audio_done_event_merge, last_audio_trigger_time, audio_trigger_interval, result_queue_merge, audio_pipe)

                    for idx in range(len(hand_landmarks_list)):
                        hand_landmarks = hand_landmarks_list[idx]
                        handedness_idx = handedness_list[idx][0].index
                        pinch_position = get_pinch_position(hand_landmarks, frame)
                        pinched_memo = pinched_memo_list[handedness_idx]

                        if pinch_position is not None:
                            if pinched_memo is not None:
                                # move memo
                                pinched_memo.update_position(pinch_position)
                            else:
                                # catch, move and open memo
                                for triggered_memo in triggered_memo_list:
                                    if is_pinched(triggered_memo, pinch_position):
                                        pinched_memo_list[handedness_idx] = triggered_memo
                                        triggered_memo.update_position(pinch_position)
                                        triggered_memo_list.remove(triggered_memo)
                                        # open
                                        audio_done_event_open, last_audio_trigger_time, result_queue_open = open(memo, memo_list,
                                                                                                                 audio_done_event_open, last_audio_trigger_time, audio_trigger_interval, result_queue_open, audio_pipe)
                                        break
                                # create a new memo
                                else:
                                    memo_new, audio_done_event_create, last_audio_trigger_time, result_queue_create = \
                                        create(pinch_position, audio_done_event_create, last_audio_trigger_time,
                                               audio_trigger_interval, result_queue_create, audio_pipe)
                        elif pinched_memo is not None:
                            # merge memo automatically
                            for memo in memo_list[::-1]:
                                if memo is not pinched_memo and is_overlap(memo, pinched_memo):
                                    pinched_memo.merge(memo)
                                    memo_list.remove(memo)
                                    if memo in pinched_memo_list:
                                        pinched_memo_list[(idx+1)%2] = None
                                    break
                            pinched_memo_list[handedness_idx] = None

                ############Chenrui###############
                # add
                for memo in memo_list:
                    if memo.is_opened and not memo.is_added:
                        audio_done_event_add, last_audio_trigger_time, result_queue_add = add(
                            memo, audio_done_event_add, last_audio_trigger_time, audio_trigger_interval,
                            result_queue_add, audio_pipe)
                    if memo.is_added:
                        audio_done_event_write, last_audio_trigger_time, result_queue_write = write(
                            memo, audio_done_event_write, last_audio_trigger_time, audio_trigger_interval,
                            result_queue_write, audio_pipe)
                ##################################

                if memo_new is not None:
                    memo_list.append(memo_new)
                highlight_memo(frame, triggered_memo_list)
                highlight_memo(frame, pinched_memo_list, highlight_color=(64, 64, 255))
                frame = draw_memo(frame, memo_list)

                ############Chenrui###############
                for memo in memo_list:
                    if memo.is_opened:
                        cv2.imshow("memo_display", memo.get_big_pic())
                        # frame = add_memo_bar_to_frame(frame, memo)
                ##################################
                cv2.imshow("camera", frame)

            # press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


def result_callback(result: vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global detection_result_new
    detection_result_new = result




if __name__ == "__main__":
    # initialize
    model_id = ["openai/whisper-base", "openai/whisper-large-v3"]
    audio_pipe = model_initialize(model_id[0])
    memo1 = Memo([0, 0], content="A")
    memo_list = [memo1]

    start(memo_list, audio_pipe)