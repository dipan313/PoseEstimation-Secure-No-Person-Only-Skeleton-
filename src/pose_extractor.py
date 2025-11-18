import cv2 as cv
import numpy as np
import mediapipe as mp
from utils import detect_pose, draw_skeleton

def extract_skeleton_video(input_path, output_path):
    cap = cv.VideoCapture(input_path)
    fps = int(cap.get(cv.CAP_PROP_FPS))
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv.VideoWriter_fourcc(*'XVID')
    out = cv.VideoWriter(output_path, fourcc, fps, (width, height))

    pose_video = mp.solutions.pose.Pose(static_image_mode=False,
                                        min_detection_confidence=0.5,
                                        model_complexity=1)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        results = detect_pose(frame, pose_video)
        skeleton_frame = np.zeros_like(frame)  # black background
        skeleton_frame = draw_skeleton(skeleton_frame, results.pose_landmarks)



        out.write(skeleton_frame)
        # cv.imshow("Skeleton Extraction", skeleton_frame)
        # if cv.waitKey(1) & 0xFF == 27:
        #     break

    cap.release()
    out.release()
    cv.destroyAllWindows()
