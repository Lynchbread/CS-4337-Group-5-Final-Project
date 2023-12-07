import cv2 as cv

# frame_rate = 1 extracts every frame
# frame_rate = 2 extracts every other frame
# frame_rate = 3 extracts every third frame, etc
def extract_frames(video_filepath, framerate = 1):

    # Loads video
    video = cv.VideoCapture(video_filepath)

    frames = []
    frame_number = 0

    while (True):

        # Extracts next frame from video
        success, frame = video.read()

        # Appends extracted frame to list
        if success == True:
            if frame_number % framerate == 0:
                frames.append(frame)
        else:
            break
        frame_number += 1

    video.release()

    return frames       # frames is a list or array of frames in the video.