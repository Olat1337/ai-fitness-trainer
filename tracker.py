import cv2
import mediapipe as mp
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

CAMERA_INDEX = 0
ESC_KEY_CODE = 27
DETECTION_CONFIDENCE = 0.5
TRACKING_CONFIDENCE = 0.5

def run_fitness_tracker():
    cv2.namedWindow('preview')
    vc = cv2.VideoCapture(CAMERA_INDEX)

    with mp_pose.Pose(min_detection_confidence = DETECTION_CONFIDENCE, min_tracking_confidence = TRACKING_CONFIDENCE) as pose:
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
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )
    return frame

def main():
    run_fitness_tracker()

if __name__ == "__main__":
    main()