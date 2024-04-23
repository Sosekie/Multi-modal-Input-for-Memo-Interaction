import cv2
import numpy as np
import matplotlib.pyplot as plt
from random import randint
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

COLOR_NUM = 20
COLOR_MAP = plt.cm.get_cmap('tab20', COLOR_NUM)

class Memo:
    def __init__(self, position, content, size=100):
        self.position = position    # position = [x, y]

        rand_color = np.array(COLOR_MAP(randint(0, COLOR_NUM-1))[:3]) * 255
        self.color = rand_color.astype(np.uint8)
        self.content = content
        self.size = int(size)
        
        self.pic = np.zeros((self.size, self.size, 3), dtype=np.uint8)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.font_color = (255, 255, 255)  # 白色
        self.font_thickness = 2

        self.update_pic()

    def update_pic(self):
        picture = np.broadcast_to(self.color, (self.size, self.size, 3))
        picture = cv2.cvtColor(picture, cv2.COLOR_BGR2RGB)
        
        # put text on the memo
        text_size = cv2.getTextSize(self.content, self.font, self.font_scale, self.font_thickness)
        text_x = int((self.size - text_size[0][0]) / 2)
        text_y = int((self.size + text_size[0][1]) / 2)
        cv2.putText(picture, self.content, (text_x, text_y), self.font, self.font_scale, self.font_color, self.font_thickness)

        # update
        self.pic = picture.astype(np.uint8)

    def get_pic(self):
        return self.pic

    def merge(self, memo):
        self.content = self.content + memo.content
        self.color = (self.color + memo.color) // 2
        self.update_pic()

    def is_triggered(self, detection_result, frame):
        hand_landmarks_list = detection_result.hand_landmarks
    
        for idx in range(len(hand_landmarks_list)):
            hand_landmarks = hand_landmarks_list[idx]
            for landmark in hand_landmarks:
                if (self.position[0] <= landmark.x*frame.shape[1] <= self.position[0]+self.size and
                        self.position[1] <= landmark.y*frame.shape[0] <= self.position[1]+self.size):
                    return True
        return False

    # Update position function
    def update_position(self, new_pos):
        self.position = new_pos


def is_pinched(detection_result):
    thumb_tip_distance = None
    hand_landmarks_list = detection_result.hand_landmarks

    for idx_hand, hand_landmarks in enumerate(hand_landmarks_list):
        # Both landmarks are in the touch area, calculate distance
        thumb_tip_distance = abs(hand_landmarks[8].x - hand_landmarks[4].x) + abs(hand_landmarks[8].y - hand_landmarks[4].y)
        thumb_tip_middle_distance = abs(hand_landmarks[6].x - hand_landmarks[3].x) + abs(hand_landmarks[6].y - hand_landmarks[3].y)
        if thumb_tip_distance < thumb_tip_middle_distance:
            position = [hand_landmarks[4].x, hand_landmarks[4].y]
            return position
    # No hands or landmarks in the touch area
    return []


def draw_landmarks_on_image(frame, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(frame)

    # Loop through the detected hands to visualize.
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        handedness = handedness_list[idx]

        # Draw the hand landmarks.
        hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        hand_landmarks_proto.landmark.extend([
        landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z) for landmark in hand_landmarks
        ])
        solutions.drawing_utils.draw_landmarks(
        annotated_image,
        hand_landmarks_proto,
        solutions.hands.HAND_CONNECTIONS,
        solutions.drawing_styles.get_default_hand_landmarks_style(),
        solutions.drawing_styles.get_default_hand_connections_style())

    return annotated_image

def draw_memo(frame, memo_list):
    for memo in memo_list:
        memo_pic = memo.get_pic()
        memo_right = min(memo.position[0]+memo.size, frame.shape[1])
        memo_bottom = min(memo.position[1]+memo.size, frame.shape[0])

        memo_pic = memo_pic[:memo_bottom - memo.position[1], :memo_right - memo.position[0]]
        frame[memo.position[1]: memo_bottom, memo.position[0]: memo_right] = memo_pic

    return frame

def highlight_memo(frame, triggered_memo_list):
    for memo in triggered_memo_list:
        highlight_left = max(memo.position[0] - 10, 0)
        highlight_right = min(memo.position[0] + memo.size + 10, frame.shape[1])
        highlight_top = max(memo.position[1] - 10, 0)
        highlight_bottom = min(memo.position[1] + memo.size + 10, frame.shape[0])

        cv2.rectangle(frame, (highlight_left, highlight_top), (highlight_right, highlight_bottom), (0, 255, 255), -1)

    return frame
    
def detector_init():

    base_options = python.BaseOptions(model_asset_path='./gesture/hand_landmarker.task')
    options = vision.HandLandmarkerOptions(base_options=base_options,
                                        min_hand_detection_confidence=0.2,
                                        min_hand_presence_confidence=0.9,
                                        num_hands=2)
    detector = vision.HandLandmarker.create_from_options(options)

    return detector
