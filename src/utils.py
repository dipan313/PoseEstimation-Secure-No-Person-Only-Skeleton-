import cv2 as cv
import mediapipe as mp

mp_pose = mp.solutions.pose

def detect_pose(frame, pose_video):
    """Detect pose landmarks from a frame."""
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = pose_video.process(frame_rgb)
    return results

def draw_skeleton(frame, landmarks):
    """Draw pose landmarks on a blank frame."""
    if landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            frame,
            landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp.solutions.drawing_utils.DrawingSpec(color=(225,117,66), thickness=2, circle_radius=2),
            mp.solutions.drawing_utils.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        )
    return frame
