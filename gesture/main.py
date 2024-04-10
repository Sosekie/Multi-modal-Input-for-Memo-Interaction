import cv2
import numpy as np
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

MARGIN = 10  # pixels
FONT_SIZE = 1
FONT_THICKNESS = 1
HANDEDNESS_TEXT_COLOR = (88, 205, 54) # vibrant green

class Memo:
    def __init__(self, color, content, side, size=100):
        if side == "right":
            self.side = 1
        else:
            self.side = 0
        
        self.position_x = 0
        self.position_y = 0

        self.color = np.array(color, dtype=np.uint8)
        self.content = content
        self.size = int(size)
        
        self.pic = np.zeros((self.size, self.size, 3), dtype=np.uint8)
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1.5
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
                if abs(self.side-landmark.x)*frame.shape[1]<=self.size and landmark.y*frame.shape[0]<=self.size:
                    return True
        return False
    
    def is_pinched(self, detection_result, frame):
        thumb_tip_distance = None
        hand_landmarks_list = detection_result.hand_landmarks

        for idx_hand, hand_landmarks in enumerate(hand_landmarks_list):
            # Check if thumb tip is in the touch area
            if not (abs(self.side - hand_landmarks[4].x) * frame.shape[1] <= self.size and
                    hand_landmarks[4].y * frame.shape[0] <= self.size):
                continue  # Skip to next hand if thumb not in touch area

                # Check if index finger tip is in the touch area
            if not (abs(self.side - hand_landmarks[8].x) * frame.shape[1] <= self.size and
                    hand_landmarks[8].y * frame.shape[0] <= self.size):
                continue  # Skip to next hand if index finger not in touch area

            # Both landmarks are in the touch area, calculate distance
            thumb_tip_distance = abs(hand_landmarks[8].x - hand_landmarks[4].x) + abs(hand_landmarks[8].y - hand_landmarks[4].y)
            # Implement further logic based on thumb_tip_distance (pinch detection)
            return thumb_tip_distance
        
        # No hands or landmarks in the touch area
        return False
    
    def handle_pinch(self, detection_result, frame):
        # Check for pinch gesture using is_pinched function
        thumb_tip_distance = self.is_pinched(detection_result, frame)
        if thumb_tip_distance is not None:
        # Pinch detected, calculate movement based on distance (optional)
        # You can implement logic here to move the memo based on the calculated
        # distance (thumb_tip_distance) in the is_pinched function. For example,
        # a larger distance could correspond to a larger movement.
            # x, y, w, h = cv2.boundingRect(frame)  # x, y are top-left corner coordinates
            self.move(thumb_tip_distance)  # Call a new function to move the memo


    # Add a new function to handle movement (pseudocode)
    def move(self, distance):
        # Update memo position based on distance and side (consider damping for smoothness)
        new_x = self.position_x + (distance * (1 if self.side == 1 else -1))
        new_y = self.position_y  # You can add vertical movement if needed
        self.update_position(new_x, new_y)

    # Update position function (assuming you have position attributes)
    def update_position(self, new_x, new_y):
        self.position_x = new_x
        self.position_y = new_y


def is_catched(self, detection_result, frame):
    hand_landmarks_list = detection_result.hand_landmarks
    
    thumb_tip = hand_landmarks_list[solutions.hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks_list[solutions.hands.HandLandmark.INDEX_FINGER_TIP]
    threshold = 10
    for idx in range(len(hand_landmarks_list)):
        hand_landmarks = hand_landmarks_list[idx]
        # Check distance between thumb and index finger
        distance = abs(thumb_tip.x - index_tip.x)*frame.shape[1] + abs(thumb_tip.y - index_tip.y)*frame.shape[0]
        while distance < threshold :
            # calculate whether the location of the landmark is inside the memo area
            # if there’s a landmark inside the area of this memo, return true
            if abs(self.side-thumb_tip.x)*frame.shape[1]<=self.size and thumb_tip.y*frame.shape[0]<=self.size:
                return True
    return False


    
def draw_landmarks_on_image(rgb_image, detection_result):
    hand_landmarks_list = detection_result.hand_landmarks
    handedness_list = detection_result.handedness
    annotated_image = np.copy(rgb_image)

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

def add_memo(frame, memo):
    if memo.side:
        frame[:memo.size, -memo.size:, :] = memo.get_pic()
    else:
        frame[:memo.size, :memo.size, :] = memo.get_pic()

    return frame

def highlight_memo(frame, memo):
    if memo.side:
        cv2.rectangle(frame, (frame.shape[1]-memo.size-10,0), (frame.shape[1], memo.size+10), (0, 255, 255), -1)
    else:
        cv2.rectangle(frame, (0,0), (memo.size+10, memo.size+10), (0, 255, 255), -1)
    
def detector_init():

    base_options = python.BaseOptions(model_asset_path='./gesture/hand_landmarker.task')
    options = vision.HandLandmarkerOptions(base_options=base_options,
                                        min_hand_detection_confidence=0.4,
                                        min_hand_presence_confidence=0.3,
                                        num_hands=2)
    detector = vision.HandLandmarker.create_from_options(options)

    return detector