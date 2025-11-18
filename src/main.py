from pose_extractor import extract_skeleton_video
from overlay_videos import overlay_videos
import cv2 as cv

if __name__ == "__main__":
    person_video_path = "input/person0.mp4"
    skeleton_video = "output/skeleton.avi"
    room_video = "input/room.mp4"
    final_output = "output/combined.mp4"

    # Show original video
    cap = cv.VideoCapture(person_video_path)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv.imshow("Original Video", frame)

        # Exit when ESC key is pressed
        if cv.waitKey(2) & 0xFF == 27:
            break

    cap.release()
    cv.destroyAllWindows()

    # Process skeleton extraction
    print("Extracting skeleton video...")
    extract_skeleton_video(person_video_path, skeleton_video)

    # Overlay with room video
    print("Overlaying skeleton on room video...")
    overlay_videos(room_video, skeleton_video, final_output)

    print("Process complete. Final video saved at:", final_output)
