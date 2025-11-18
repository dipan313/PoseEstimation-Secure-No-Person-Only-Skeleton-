import cv2
import mediapipe as mp
import numpy as np

# Initialize Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False,
                    min_detection_confidence=0.5,
                    model_complexity=1)

# Webcam (your skeleton source)
cap_person = cv2.VideoCapture(0)

# Room background video
cap_room = cv2.VideoCapture("input/`room.mp4")   # change to your file
if not cap_room.isOpened():
    raise FileNotFoundError("⚠️ Could not open room.mp4")

# Output writer (optional)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
fps = int(cap_room.get(cv2.CAP_PROP_FPS))
width = int(cap_room.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap_room.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter("skeleton_in_room.mp4", fourcc, fps, (width, height))

# Parameters to control skeleton placement
scale_factor = 1.5   # make skeleton bigger/smaller
offset_x = 0         # move left/right
offset_y = 50        # move up/down (positive → up)

while True:
    # 1. Get person frame (for skeleton only)
    ret1, person_frame = cap_person.read()
    if not ret1:
        break

    # Detect skeleton
    rgb = cv2.cvtColor(person_frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    # Draw skeleton on transparent smaller canvas (person frame size)
    person_h, person_w = person_frame.shape[:2]
    skeleton_frame = np.zeros((person_h, person_w, 3), dtype=np.uint8)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(
            skeleton_frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing.DrawingSpec(color=(225,117,66), thickness=2, circle_radius=2),
            connection_drawing_spec=mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        )

    # Resize skeleton to fit room scale
    new_w = int(width / scale_factor)
    new_h = int(height / scale_factor)
    skeleton_resized = cv2.resize(skeleton_frame, (new_w, new_h))

    # Transparent canvas same as room size
    skeleton_canvas = np.zeros((height, width, 3), dtype=np.uint8)

    # Position: bottom-center with offsets
    x_offset = width // 2 - new_w // 2 + offset_x
    y_offset = height - new_h - offset_y

    # Paste skeleton onto canvas
    skeleton_canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = skeleton_resized

    # 2. Get room background frame
    ret2, room_frame = cap_room.read()
    if not ret2:
        # loop the video
        cap_room.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret2, room_frame = cap_room.read()

    room_frame = cv2.resize(room_frame, (width, height))

    # 3. Overlay skeleton on room video
    combined = cv2.addWeighted(room_frame, 1.0, skeleton_canvas, 1.0, 0)

    # Save + Show
    out.write(combined)
    cv2.imshow("Skeleton in Room", combined)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap_person.release()
cap_room.release()
out.release()
cv2.destroyAllWindows()
