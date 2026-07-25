from pose_extractor import extract_skeleton_video
from overlay_videos import overlay_videos
import cv2 as cv
import os


if __name__ == "__main__":
    person_video_path = "input/person0.mp4"
    skeleton_video = "output/skeleton.avi"
    room_video = "input/room.mp4"
    final_output = "output/combined.mp4"


    # Show Original Input Video
    
    if not os.path.exists(person_video_path):
        print("Input video not found!")
        exit()

    cap = cv.VideoCapture(person_video_path)

    if not cap.isOpened():
        print("Error: Could not open input video.")
        exit()

    print("Playing Original Video...")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        cv.imshow("Original Input Video", frame)

        # Press ESC to skip
        if cv.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv.destroyAllWindows()
    cv.waitKey(1)


    # Skeleton Extraction

    print("Extracting skeleton video...")
    extract_skeleton_video(person_video_path, skeleton_video)


    # Overlay Videos

    print("Overlaying skeleton on room video...")
    overlay_videos(room_video, skeleton_video, final_output)

    print("Processing Complete!")
    print("Final video saved at:", final_output)

    # Show Final Output Video
    if not os.path.exists(final_output):
        print("Output video not found!")
        exit()

    cap = cv.VideoCapture(final_output)

    if not cap.isOpened():
        print("Error: Could not open output video.")
        exit()

    print("Playing Final Output Video...")

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        cv.imshow("Final Output Video", frame)

        # Press ESC to close
        if cv.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv.destroyAllWindows()
    cv.waitKey(1)