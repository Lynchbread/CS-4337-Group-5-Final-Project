import cv2
from extract_frames import extract_frames
from detect_motion import detect_motion
from identify_objects import identify_objects

    # Get first frame, set as 'prev'

    # Vote on lines, top two should be bounds of road

    # Create mask with only road lines
    
    # Store coordinates of each line as lists of tuples

    # Start loop until no current frame exists

    # Use 3 concurrent frames for motion detection (or more if needed)

    # If motion detected and component originates within lines, ignore (Car)

    # If motion detected originates outside lines, component above threshold, draw box

    # Extract direction of motion (for instance, compare change in x, y )

    # If motion towards road, hard signal (crossing, should linger after crossed)

    # If motion along/ near road , signal (present)

    # If no motion but components exist, signal (present)

    # If no components (or car) no signal 

def main():

    #video_path = 'data\\videos\\The Deer Go Marching One by One [vZq88Iw8dsM].mp4'

    #frames = extract_frames(video_path, 5)

    #identify_objects(frames[5], frames[6], frames[7])

    #cv2.imshow("image", new_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Hardcode video path for testing
    video_path = 'data\\videos\\The Deer Go Marching One by One [vZq88Iw8dsM].mp4'
    # frames = extract_frames(video_path, 5)

    # Get video capture, fps, and delay value for playback at original speed
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    delay = int((1 / fps) * 1000)

    # Get first frame in video
    frame_exists, current_frame = video.read()
    
    # Get list containing every frame in video
    frames, i = extract_frames(video_path, 1), 0
    
    # Validate frame being correctly accessed from list
    # frames[i] = cv.cvtColor(frames[i], cv.COLOR_BGR2RGB)
    # plt.imshow(frames[len(frames) - 1])
    # plt.show()

    frame_rate = 5

    # Loop until video ends (exit using 'ctrl+C' or simply 'q')
    while frame_exists:

        """
        # # Set previous, next frames
        if i == 0:                          # Case may need attention for frame differencing
            prev_frame = current_frame
        else:
            prev_frame = frames[i - 1]
        
        next_frame = frames[i + 1]
        """

        if i >= frame_rate:
            prev_frame = frames[i - frame_rate]
            next_frame = frames[i + frame_rate]

            rectangles = identify_objects(prev_frame, current_frame, next_frame)

        # Show current_frame
        cv2.imshow('frame', current_frame)

        # Extract current frame
        frame_exists, current_frame = video.read()

        # Introduce delay, stop playback if 'q' pressed
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

        i += 1

    # Exit program gracefully
    video.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()