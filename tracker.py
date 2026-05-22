import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

CAMERA_INDEX = 0
ESC_KEY_CODE = 27
DETECTION_CONFIDENCE = 0.5
TRACKING_CONFIDENCE = 0.5

class BicepCurlCounter:
    def __init__(self, side):
        self.counter = 0
        self.stage = None
        self.side = side

    def calculate_angle(self ,a, b, c):
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])

        radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
        angle = np.abs(radians * 180.0 / np.pi)

        if angle > 180.0:
            angle = 360 - angle

        return angle

    def process(self, frame, results):
        h, w, _ = frame.shape

        if self.side == "left":
            shoulder_idx = mp_pose.PoseLandmark.LEFT_SHOULDER
            elbow_idx = mp_pose.PoseLandmark.LEFT_ELBOW
            wrist_idx = mp_pose.PoseLandmark.LEFT_WRIST
        else:
            shoulder_idx = mp_pose.PoseLandmark.RIGHT_SHOULDER
            elbow_idx = mp_pose.PoseLandmark.RIGHT_ELBOW
            wrist_idx = mp_pose.PoseLandmark.RIGHT_WRIST

        if results.pose_landmarks:
            shoulder_cords = results.pose_landmarks.landmark[shoulder_idx]
            elbow_cords = results.pose_landmarks.landmark[elbow_idx]
            wrist_cords = results.pose_landmarks.landmark[wrist_idx]

            angle = self.calculate_angle(shoulder_cords, elbow_cords, wrist_cords)

            if angle > 150:
                self.stage = "down"
            elif angle < 45 and self.stage == "down":
                self.counter +=1
                self.stage = "up"

                print(f"{self.side} arm reps: {self.counter}")
            cv2.putText(frame, str(int(angle)),
                        tuple(np.multiply([elbow_cords.x, elbow_cords.y], [w, h]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            if self.side == "left":
                cv2.putText(frame, str(self.counter), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            else:
                cv2.putText(frame, str(self.counter), (w - 100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        return frame

def run_fitness_tracker():
    cv2.namedWindow('preview', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('preview', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    vc = cv2.VideoCapture(CAMERA_INDEX)

    vc.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    with mp_pose.Pose(min_detection_confidence = DETECTION_CONFIDENCE, min_tracking_confidence = TRACKING_CONFIDENCE) as pose:
        left_tracker = BicepCurlCounter(side="left")
        right_tracker = BicepCurlCounter(side = "right")
        while vc.isOpened():
            success, frame = vc.read()
            if not success:
                break

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    mp_pose.POSE_CONNECTIONS
                )

            frame = left_tracker.process(frame, results)
            frame = right_tracker.process(frame, results)
            cv2.imshow("preview", frame)

            key = cv2.waitKey(20)
            if key == ESC_KEY_CODE:
                break

        cv2.destroyWindow("preview")
        vc.release()

def main():
    run_fitness_tracker()

if __name__ == "__main__":
    main()