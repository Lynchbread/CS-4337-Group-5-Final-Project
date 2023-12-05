from extract_frames import extract_frames
from detect_motion import detect_motion
from get_road_lines import get_road_lines

import cv2


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

    video_path = 'data/videos/The Deer Go Marching One by One [vZq88Iw8dsM].mp4'

    frames = extract_frames(video_path, 5)

    line_image = get_road_lines(frames[0])

    cv2.imshow('road lines', line_image)
    cv2.waitKey(0)  # Wait indefinitely for a key press
    cv2.destroyAllWindows()  # Close all OpenCV windows


if __name__ == '__main__':
    main()