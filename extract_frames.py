import cv2
import os

def extract_frames(video_filepath):

    video = cv2.VideoCapture(video_filepath)

    frames = []
    frame_number = 0

    while (True):
        success, frame = video.read()

        if success == True:
            cv2.imwrite('/data/images'+str(frame_number)+'.jpg', frame)
            frames.append(frame)
        else:
            break
        frame_number += 1

    video.release()

    return frames # frames is a list or array of frames in the video.