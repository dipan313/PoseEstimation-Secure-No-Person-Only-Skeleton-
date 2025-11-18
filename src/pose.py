import cv2 as cv
import mediapipe as mp
import numpy as np
from time import time

# Initialize pose
mp_pose = mp.solutions.pose
pose_video = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)


# Stage 1: Extract skeleton video

input_video = "person.mp4"   # Change to your input video (or 0 for webcam)
skeleton_output = "skeleton.mp4"

video = cv.VideoCapture(input_video)
fps = int(video.get(cv.CAP_PROP_FPS))
width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))

# FourCC for video saving
fourcc = cv.VideoWriter_fourcc(*'MP4V')
skeleton_writer = cv.VideoWriter(skeleton_output, fourcc, fps, (width, height), True)

def detectPose(frame, pose_video):
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = pose_video.process(frame_rgb)
    return results

while video.isOpened():
    ok, frame = video.read()
    if not ok:
        break
    
    pose_results = detectPose(frame, pose_video)

    # Create transparent-like background (black canvas)
    skeleton_frame = np.zeros_like(frame)

    # Draw skeleton
    if pose_results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            skeleton_frame,
            pose_results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp.solutions.drawing_utils.DrawingSpec(color=(225,117,66), thickness=2, circle_radius=2),
            mp.solutions.drawing_utils.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        )

    skeleton_writer.write(skeleton_frame)
    cv.imshow("Skeleton Only", skeleton_frame)

    if cv.waitKey(1) & 0xFF == 27:
        break

video.release()
skeleton_writer.release()
cv.destroyAllWindows()

print("Skeleton video saved at:", skeleton_output)


# Stage 2: Overlay on room background

room_video = "room.mp4"       # background room video
output_final = "combined.mp4"

room_cap = cv.VideoCapture(room_video)
skeleton_cap = cv.VideoCapture(skeleton_output)

fps = int(room_cap.get(cv.CAP_PROP_FPS))
width = int(room_cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(room_cap.get(cv.CAP_PROP_FRAME_HEIGHT))

out = cv.VideoWriter(output_final, fourcc, fps, (width, height))

while True:
    ret1, room_frame = room_cap.read()
    ret2, skeleton_frame = skeleton_cap.read()

    if not ret1 or not ret2:
        break

    # Resize skeleton to room frame size
    skeleton_frame = cv.resize(skeleton_frame, (room_frame.shape[1], room_frame.shape[0]))

    # Overlay skeleton (addWeighted)
    combined = cv.addWeighted(room_frame, 1, skeleton_frame, 1, 0)

    out.write(combined)
    cv.imshow("Final Output", combined)
    if cv.waitKey(1) & 0xFF == 27:
        break

room_cap.release()
skeleton_cap.release()
out.release()
cv.destroyAllWindows()

print("Final video saved at:", output_final)
