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


def test_1(memo1, memo2):

    memo1.merge(memo2)

    # show memos
    cv2.imshow("memo1", memo1.get_pic())
    cv2.imshow("memo2", memo2.get_pic())
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def test_2(memo1, memo2, detector):
    # use the camera
    cap = cv2.VideoCapture(0)

    while True:
        # capture the frame
        ret, frame = cap.read()
        
        if ret:
            frame = np.array(frame[:, ::-1, :], dtype=np.uint8)

            # STEP 3: Load the input image.
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

            # STEP 4: Detect hand landmarks from the input image.
            detection_result = detector.detect(mp_image)
            
            # STEP 5: Process the classification result. In this case, visualize it.
            if detection_result:
                frame = draw_landmarks_on_image(mp_image.numpy_view(), detection_result)
                if memo1.is_triggered(detection_result, frame):
                    highlight_memo(frame, memo1)
                if memo2.is_triggered(detection_result, frame):
                    highlight_memo(frame, memo2)

            # add memos
            frame = add_memo(frame, memo1)
            frame = add_memo(frame, memo2)
            
            # show the frame
            cv2.imshow("camera", frame)
        
        # press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # release the camera
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    
    memo1 = Memo([200, 30, 30], "A", side="left")
    memo2 = Memo([30, 30, 200], "B", side="right")

    # test_1(memo1, memo2)

    detector = detector_init()

    test_2(memo1, memo2, detector)