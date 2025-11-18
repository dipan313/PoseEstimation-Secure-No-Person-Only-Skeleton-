import cv2 as cv
import mediapipe as mp
import numpy as np

# Initialize Mediapipe
mp_pose = mp.solutions.pose
mp_selfie_segmentation = mp.solutions.selfie_segmentation

pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=1)
segment = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

# ---------------- Stage 1: Extract skeleton + silhouette ----------------
input_video = "input/person.mp4"   # Change path OR use 0 for webcam
skeleton_output = "skeleton2.mp4"

video = cv.VideoCapture(input_video)
fps = int(video.get(cv.CAP_PROP_FPS)) or 30   # default fallback
width = int(video.get(cv.CAP_PROP_FRAME_WIDTH)) or 640
height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT)) or 480

# FourCC for video saving
fourcc = cv.VideoWriter_fourcc(*'mp4v')
skeleton_writer = cv.VideoWriter(skeleton_output, fourcc, fps, (width, height), True)

while video.isOpened():
    ok, frame = video.read()
    if not ok:
        break

    # Process pose + segmentation
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    pose_results = pose.process(frame_rgb)
    seg_results = segment.process(frame_rgb)

    # Segmentation mask
    mask = seg_results.segmentation_mask > 0.3
    silhouette = np.zeros_like(frame, dtype=np.uint8)
    silhouette[:] = (50, 150, 250)  # bluish silhouette
    human_only = np.where(mask[..., None], silhouette, (0, 0, 0))

    # Draw skeleton on silhouette
    if pose_results.pose_landmarks:
        mp.solutions.drawing_utils.draw_landmarks(
            human_only,
            pose_results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp.solutions.drawing_utils.DrawingSpec(color=(255, 0, 0), thickness=2, circle_radius=2)
        )

    skeleton_writer.write(human_only)
    # #cv.imshow("Skeleton + Silhouette", human_only)

    # if cv.waitKey(1) & 0xFF == 27:  # ESC to exit
    #     break

# video.release()
# skeleton_writer.release()
# cv.destroyAllWindows()

print("✅ Skeleton + silhouette video saved at:", skeleton_output)


# ---------------- Stage 2: Overlay on room background ----------------
room_video = "input/room.mp4"
output_final = "combined2.mp4"

room_cap = cv.VideoCapture(room_video)
skeleton_cap = cv.VideoCapture(skeleton_output)

fps = int(room_cap.get(cv.CAP_PROP_FPS)) or 30
width = int(room_cap.get(cv.CAP_PROP_FRAME_WIDTH)) or 640
height = int(room_cap.get(cv.CAP_PROP_FRAME_HEIGHT)) or 480

out = cv.VideoWriter(output_final, fourcc, fps, (width, height))

while True:
    ret1, room_frame = room_cap.read()
    ret2, skeleton_frame = skeleton_cap.read()

    if not ret1 or not ret2:
        break

    skeleton_frame = cv.resize(skeleton_frame, (room_frame.shape[1], room_frame.shape[0]))

    # Overlay skeleton+silhouette on room
    combined = cv.addWeighted(room_frame, 1, skeleton_frame, 1, 0)

    out.write(combined)
    cv.imshow("Final Output", combined)

    if cv.waitKey(1) & 0xFF == 27:
        break

room_cap.release()
skeleton_cap.release()
out.release()
cv.destroyAllWindows()

print("✅ Final video saved at:", output_final)
