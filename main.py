from gesture.main import *
from speech2txt.main import *
import threading
import queue


def test_1(memo1, memo2):

    memo1.merge(memo2)

    # show memos
    cv2.imshow("memo1", memo1.get_pic())
    cv2.imshow("memo2", memo2.get_pic())
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test_2(memo1, memo2, detector, audio_pipe):
    cap = cv2.VideoCapture(0)
    audio_done_event = threading.Event()
    result_queue = queue.Queue()
    last_audio_trigger_time = 0  # 上一次触发录音的时间戳
    audio_trigger_interval = 3  # 允许触发录音的最小时间间隔（秒）
    while True:
        ret, frame = cap.read()
        if ret:
            frame = np.array(frame[:, ::-1, :], dtype=np.uint8)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            detection_result = detector.detect(mp_image)
            if detection_result:
                frame = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)
                memo_1_detect, memo_2_detect = False, False
                if memo1.is_triggered(detection_result, frame):
                    highlight_memo(frame, memo1)
                    memo_1_detect = True
                if memo2.is_triggered(detection_result, frame):
                    highlight_memo(frame, memo2)
                    memo_2_detect = True
                    
                current_time = time.time()
                if memo_1_detect and memo_2_detect and not audio_done_event.is_set() and (current_time - last_audio_trigger_time > audio_trigger_interval):
                    print('Now start audio recognition:')
                    last_audio_trigger_time = current_time  # 更新上一次触发录音的时间
                    audio_done_event.clear()
                    audio_thread = threading.Thread(target=audio_trigger, args=(audio_pipe, result_queue, audio_done_event))
                    audio_thread.start()
                    
                if audio_done_event.is_set():
                    recognition_result = result_queue.get()  # 安全地获取结果
                    if recognition_result:
                        print('Now using audio to merge:')
                        memo1.merge(memo2)
                    audio_done_event.clear()

            frame = add_memo(frame, memo1)
            frame = add_memo(frame, memo2)
            cv2.imshow("camera", frame)
        # press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":

    # initialize audio_model
    model_id = ["openai/whisper-base", "openai/whisper-large-v3"]
    audio_pipe = model_initialize(model_id[0])
    memo1 = Memo([200, 30, 30], "A", side="left")
    memo2 = Memo([30, 30, 200], "B", side="right")
    detector = detector_init()
    test_2(memo1, memo2, detector, audio_pipe)