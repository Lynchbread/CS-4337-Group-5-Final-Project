import cv2
import os

# frame_rate = 1 extractes every frame
# frame_rate = 2 extracts every other frame
# frame_rate = 3 extractes every third frame, etc
def extract_frames(video_filepath, frame_rate = 1):

    video = cv2.VideoCapture(video_filepath)

    frames = []
    frame_number = 0

    while (True):
        success, frame = video.read()

        if success == True:
            if frame_number % frame_rate == 0:
                #cv2.imwrite('data\\images\\extracted_frames\\frame_'+str(frame_number)+'.jpg', frame)
                frames.append(frame)
        else:
            break
        frame_number += 1

    video.release()

    return frames # frames is a list or array of frames in the video.