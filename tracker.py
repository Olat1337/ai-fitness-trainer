import cv2
import mediapipe as mp
import numpy as np

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

CAMERA_INDEX = 0
ESC_KEY_CODE = 27
DETECTION_CONFIDENCE = 0.5
TRACKING_CONFIDENCE = 0.5

def run_fitness_tracker():
    cv2.namedWindow('preview')
    vc = cv2.VideoCapture(CAMERA_INDEX)

    with mp_pose.Pose(min_detection_confidence = DETECTION_CONFIDENCE, min_tracking_confidence = TRACKING_CONFIDENCE    ) as pose:
        while vc.isOpened():
            success, frame = vc.read()
            if not success:
                break

            frame = process_frame(frame, pose)
            cv2.imshow("preview", frame)

            key = cv2.waitKey(20)
            if key == ESC_KEY_CODE:
                break

        cv2.destroyWindow("preview")
        vc.release()

def process_frame(frame, pose):
    h, w, _ = frame.shape

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )
        shoulder_cords = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        elbow_cords = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        wrist_cords = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]

        angle = calculate_angle(shoulder_cords, elbow_cords, wrist_cords)

        cv2.putText(frame, str(int(angle)),
                    tuple(np.multiply([elbow_cords.x, elbow_cords.y], [w, h]).astype(int)),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    return frame

def calculate_angle(a, b, c):
    a = np.array([a.x, a.y])
    b = np.array([b.x, b.y])
    c = np.array([c.x, c.y])

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def main():
    run_fitness_tracker()

if __name__ == "__main__":
    main()