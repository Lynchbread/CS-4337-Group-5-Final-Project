from extract_frames import extract_frames
from detect_motion import detect_motion

def main():

    video_path = 'data\\videos\\The Deer Go Marching One by One [vZq88Iw8dsM].mp4'

    frames = extract_frames(video_path, 5)



if __name__ == '__main__':
    main()