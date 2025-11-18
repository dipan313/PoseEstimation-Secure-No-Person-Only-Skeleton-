import cv2 as cv

def overlay_videos(room_path, skeleton_path, output_path):
    room_cap = cv.VideoCapture(room_path)
    skeleton_cap = cv.VideoCapture(skeleton_path)

    fps = int(room_cap.get(cv.CAP_PROP_FPS))
    width = int(room_cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(room_cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv.VideoWriter_fourcc(*'mp4v')   # MP4 output
    out = cv.VideoWriter(output_path, fourcc, fps, (width, height))

    while True:
        ret1, room_frame = room_cap.read()
        ret2, skeleton_frame = skeleton_cap.read()
        if not ret1 or not ret2:
            break

        skeleton_frame = cv.resize(skeleton_frame, (room_frame.shape[1], room_frame.shape[0]))
        combined = cv.addWeighted(room_frame, 1, skeleton_frame, 1, 0)

        out.write(combined)
        cv.imshow("Overlay Result", combined)
        if cv.waitKey(1) & 0xFF == 27:
            break

    room_cap.release()
    skeleton_cap.release()
    out.release()
    cv.destroyAllWindows()
