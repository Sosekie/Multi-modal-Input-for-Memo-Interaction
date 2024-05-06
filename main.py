from gesture.main import *
from speech2txt.main import *
import threading
import queue
from utils.function import merge, create, open, add, write, close


def start(memo_list, detector, audio_pipe):
    cap = cv2.VideoCapture(0)
    # threading event here
    audio_done_event_merge, audio_done_event_create, audio_done_event_open, audio_done_event_add, audio_done_event_write, audio_done_event_close = threading.Event(), threading.Event(), threading.Event(), threading.Event(), threading.Event(), threading.Event()
    result_queue_merge, result_queue_create, result_queue_open, result_queue_add, result_queue_write, result_queue_close = queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue(), queue.Queue()
    last_audio_trigger_time = 0
    audio_trigger_interval = 1

    memo_new = None     # a valuable to keep the feedback from create stream

    while True:
        ret, frame = cap.read()
        if ret:
            frame = np.array(frame[:, ::-1, :], dtype=np.uint8)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            detection_result = detector.detect(mp_image)
            if detection_result:
                frame = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)
                
                # Merge memo
                triggered_memo_list = get_triggered_memo_list(memo_list, detection_result, frame, max_triggered=2)
                if len(triggered_memo_list) >= 2:
                    audio_done_event_merge, last_audio_trigger_time, result_queue_merge = merge(triggered_memo_list[0], triggered_memo_list[1], audio_done_event_merge, last_audio_trigger_time, audio_trigger_interval, result_queue_merge, audio_pipe)

                # get pinched memo list
                pinched_memo_list = get_pinched_memo_list(memo_list)

                # pinch position -> create memo / merge memo automatically / catch and move memo
                position = get_pinch_position(detection_result, frame)
                if position:
                    if position[0][0] == -1:    # all the gestures are not pinch
                        for pinched_memo in pinched_memo_list:
                            # merge memo automatically
                            for memo in memo_list:
                                if memo is not pinched_memo and is_overlap(memo, pinched_memo):
                                    pinched_memo.merge(memo)
                                    memo_list.remove(memo)
                                    break
                            pinched_memo.update_pinched(False)

                    elif len(position) == 1:
                        if len(pinched_memo_list) == 0:
                            # catch and move memos
                            for triggered_memo in triggered_memo_list:
                                if is_pinched(triggered_memo, position[0]):
                                    triggered_memo.update_pinched(True)
                                    triggered_memo.update_position(position[0])
                                    triggered_memo_list.remove(triggered_memo)
                                    break
                            # create memo
                            else:
                                memo_new, audio_done_event_create, last_audio_trigger_time, result_queue_create = create(
                                    position[0], audio_done_event_create, last_audio_trigger_time, audio_trigger_interval,
                                    result_queue_create, audio_pipe)
                        else:
                            # move memo
                            min_distance = float('inf')
                            for pinched_memo in pinched_memo_list:
                                memo_to_pinch_distance = distance.euclidean(pinched_memo.position, position[0])
                                if memo_to_pinch_distance < min_distance:
                                    min_distance = memo_to_pinch_distance
                                    memo_to_update = pinched_memo
                            if min_distance < memo_to_update.size:
                                memo_to_update.update_position(position[0])
                            # open
                            audio_done_event_open, last_audio_trigger_time, result_queue_open = open(
                                memo, memo_list, audio_done_event_open, last_audio_trigger_time, audio_trigger_interval,
                                result_queue_open, audio_pipe)

                    elif len(position) == 2:
                        if position[1][0] == -1:
                            if len(pinched_memo_list) == 0:
                                # catch and move memo
                                for triggered_memo in triggered_memo_list:
                                    if is_pinched(triggered_memo, position[0]):
                                        triggered_memo.update_pinched(True)
                                        triggered_memo.update_position(position[0])
                                        triggered_memo_list.remove(triggered_memo)
                                        break
                                # create a new memo
                                else:
                                    memo_new, audio_done_event_create, last_audio_trigger_time, result_queue_create = create(
                                        position[0], audio_done_event_create, last_audio_trigger_time,
                                        audio_trigger_interval,
                                        result_queue_create, audio_pipe)
                            elif len(pinched_memo_list) == 1:
                                # move memo
                                pinched_memo_list[0].update_position(position[0])
                            elif len(pinched_memo_list) == 2:
                                # move memo
                                sorted_pinched_memo_list = sorted(pinched_memo_list, key=lambda m: distance.euclidean(m.position, position[0]))
                                # After sorted, sorted_pinched_memo_list[0] is the memo closest to the pinch area
                                memo_to_update = sorted_pinched_memo_list[0]
                                memo_to_drop = sorted_pinched_memo_list[1]

                                memo_to_update.update_position(position[0])
                                # merge memo automatically
                                for memo in memo_list[::-1]:
                                    if memo is not memo_to_drop and is_overlap(memo, memo_to_drop):
                                        memo_to_drop.merge(memo)
                                        memo_list.remove(memo)
                                        break
                                memo_to_drop.update_pinched(False)
                        else:
                            if len(pinched_memo_list) == 0:
                                # catch and move memo
                                for pinch_position in position:
                                    for triggered_memo in triggered_memo_list:
                                        if is_pinched(triggered_memo, pinch_position):
                                            triggered_memo.update_pinched(True)
                                            triggered_memo.update_position(pinch_position)
                                            triggered_memo_list.remove(triggered_memo)
                                            break
                                    # create a new memo
                                    else:
                                        memo_new, audio_done_event_create, last_audio_trigger_time, result_queue_create = create(
                                            pinch_position, audio_done_event_create, last_audio_trigger_time,
                                            audio_trigger_interval,
                                            result_queue_create, audio_pipe)
                            elif len(pinched_memo_list) == 1:
                                # move memo
                                sorted_position = sorted(position, key=lambda p: distance.euclidean(pinched_memo_list[0].position, p))
                                pinched_memo_list[0].update_position(sorted_position[0])

                                # catch and move memo
                                for triggered_memo in triggered_memo_list:
                                    if is_pinched(triggered_memo, sorted_position[1]):
                                        triggered_memo.update_pinched(True)
                                        triggered_memo.update_position(sorted_position[1])
                                        triggered_memo_list.remove(triggered_memo)
                                        break
                                # create a new memo
                                else:
                                    memo_new, audio_done_event_create, last_audio_trigger_time, result_queue_create = create(
                                        sorted_position[1], audio_done_event_create, last_audio_trigger_time,
                                        audio_trigger_interval,
                                        result_queue_create, audio_pipe)
                            elif len(pinched_memo_list) == 2:
                                # move memo
                                sorted_position = sorted(position, key=lambda p: distance.euclidean(pinched_memo_list[0].position, p))
                                pinched_memo_list[0].update_position(sorted_position[0])
                                pinched_memo_list[1].update_position(sorted_position[1])

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

            if memo_new is not None:
                memo_list.append(memo_new)
            highlight_memo(frame, triggered_memo_list)
            pinched_memo_list = get_pinched_memo_list(memo_list)
            highlight_memo(frame, pinched_memo_list, highlight_color=(64, 64, 255))
            frame = draw_memo(frame, memo_list)

            cv2.imshow("camera", frame)
            for memo in memo_list:
                if memo.is_opened:
                    cv2.imshow("memo_display", memo.get_big_pic())

        # press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":

    # initialize
    model_id = ["openai/whisper-base", "openai/whisper-large-v3"]
    audio_pipe = model_initialize(model_id[0])
    # audio_pipe_large = model_initialize(model_id[1])
    memo1 = Memo([0, 0], content="A")
    memo1.update_pinched(False)
    # memo2 = Memo([0, 600], content="B")
    memo_list = [memo1]
    detector = detector_init()

    start(memo_list, detector, audio_pipe)