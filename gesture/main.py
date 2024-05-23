import random
import string
import cv2
import numpy as np
import matplotlib.pyplot as plt
from random import randint
from scipy.spatial import distance
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class Memo:
    def __init__(self, position, content=None, size=100, big_size=[200, 838]):
        self.position = position    # position = [x, y]

        self.color = np.random.randint(150, 241, size=3).astype(np.uint8)
        self.content = random.choice(string.ascii_uppercase)
        if content:
            self.content = content
        self.size = int(size)
        self.big_size = big_size
        
        self.pic = np.zeros((self.size, self.size, 3), dtype=np.uint8)
        self.big_pic = np.zeros((self.big_size[0], self.big_size[1], 3), dtype=np.uint8)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.font_color = (255, 255, 255)
        self.font_thickness = 2

        self.is_added = False
        self.is_finished = False

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

        # for big pic
        picture = np.broadcast_to(self.color, (self.big_size[0], self.big_size[1], 3))
        picture = cv2.cvtColor(picture, cv2.COLOR_BGR2RGB)
        text_size = cv2.getTextSize(self.content, self.font, self.font_scale, self.font_thickness)
        text_x = 20
        text_y = text_size[0][1] + 20
        cv2.putText(picture, self.content, (text_x, text_y), self.font, self.font_scale, self.font_color, self.font_thickness)
        self.big_pic = picture.astype(np.uint8)

    def update_content(self, content):
        self.content = str(content)
        self.update_pic()

    def get_pic(self):
        return self.pic

    def get_big_pic(self):
        picture = self.big_pic
        if self.is_added:
            cv2.rectangle(picture, (0, 0), (self.big_size[1] - 1, self.big_size[0] - 1), (0, 0, 255), 10)  # Red border
        return picture

    def merge(self, memo):
        self.content = memo.content + self.content
        self.color = (self.color + memo.color) // 2
        self.update_pic()

    def is_triggered(self, hand_landmarks_list, frame):
        for hand_landmarks in hand_landmarks_list:
            for landmark in hand_landmarks:
                if (self.position[0] <= landmark.x*frame.shape[1] <= self.position[0]+self.size and
                        self.position[1] <= landmark.y*frame.shape[0] <= self.position[1]+self.size):
                    return True
        return False

    # Update position function
    def update_position(self, new_pos):
        if distance.euclidean(self.position, new_pos) < self.size:
            self.position = new_pos

    def update_added(self, status):
        self.is_added = status


# if there is any overlap between 2 memos
def is_overlap(memo1, memo2):
    return np.all(np.array(memo1.position)+memo1.size > memo2.position) and \
           np.all(np.array(memo2.position)+memo2.size > memo1.position)


# get a triggered memo list from memo list
def get_triggered_memo_list(memo_list, hand_landmarks_list, frame, max_triggered=5):
    triggered_memo_list = []
    for memo in memo_list[::-1]:
        if len(triggered_memo_list) >= max_triggered:
            break
        elif memo.is_triggered(hand_landmarks_list, frame):    # pinched memos and triggered memos are in different groups
            for triggered_memo in triggered_memo_list:
                if is_overlap(memo, triggered_memo):
                    break
            else:
                triggered_memo_list.append(memo)

    return triggered_memo_list


def get_pinch_position(hand_landmarks, frame):
    pinch_position = None

    # Both landmarks are in the touch area, calculate distance
    thumb_tip_distance = abs(hand_landmarks[8].x - hand_landmarks[4].x) + abs(hand_landmarks[8].y - hand_landmarks[4].y)
    thumb_tip_middle_distance = abs(hand_landmarks[6].x - hand_landmarks[3].x) + abs(hand_landmarks[6].y - hand_landmarks[3].y)
    if thumb_tip_distance < thumb_tip_middle_distance:
        pinch_position = [int(hand_landmarks[4].x*frame.shape[1]), int(hand_landmarks[4].y*frame.shape[0])]

    # If there is no hand or landmark in the touch area, it will return False
    return pinch_position


# If the pinch position pinched a memo
def is_pinched(memo, position):
    return np.all(np.array(memo.position) <= np.array(position)) and \
           np.all(np.array(position) < np.array(memo.position)+memo.size)


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

def highlight_memo(frame, memo_list, highlight_color=(0,255,255)):
    for memo in memo_list:
        if memo is None:
            continue
        highlight_left = max(memo.position[0] - 10, 0)
        highlight_right = min(memo.position[0] + memo.size + 10, frame.shape[1])
        highlight_top = max(memo.position[1] - 10, 0)
        highlight_bottom = min(memo.position[1] + memo.size + 10, frame.shape[0])

        cv2.rectangle(frame, (highlight_left, highlight_top), (highlight_right, highlight_bottom), highlight_color, -1)

    return frame
