import cv2
from extract_frames import extract_frames
from detect_motion import detect_motion
from get_road_lines import get_road_lines
from identify_objects import identify_objects
from get_direction import get_direction

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
    video_path = 'data\\videos\\DeerVideo.mp4'
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

    #for j in range(len(frames)):
    #    cv2.imwrite('data\\images\\extracted_frames\\' + str(j) + '.jpg', frames[j])

    frame_rate = 5
    leeway = 1
    if leeway > frame_rate: leeway = frame_rate
    object_centers = []
    signals = []
    signal_counter = 0

    # Loop until video ends (exit using 'ctrl+C' or simply 'q')
    while frame_exists:

        if i >= frame_rate:
            prev_frame = frames[i - frame_rate]

            if i + frame_rate < len(frames):
                next_frame = frames[i + frame_rate]
            else: break

            prev_object_centers = object_centers
            object_centers = identify_objects(prev_frame, current_frame, next_frame)
            road_contours = get_road_lines(current_frame)
            for contour in road_contours:
                current_frame = cv2.drawContours(current_frame, [contour], 0, (0, 0, 0), 3)

            signals.append(get_direction(prev_object_centers, object_centers, road_contours))

            # objects must be stationary for 30 frames straight in order for signal to go from red to yellow
            if all(signals[i-leeway:i]):
                signal_counter = 30
            else:
                signal_counter -= 1
        else:
            signals.append(False)

        
        # Draws color signal indicator in upper left corner
        if signal_counter > 0:
            current_frame[0:100,0:100] = (0,0,128)  # Maintains red
        elif signal_counter > -60:
            current_frame[0:100,0:100] = (0,128,128) # Yellow if objects are stationary
        else:
            current_frame[0:100,0:100] = (0,128,0) # Green if no movement has been detected for a while

        # For infinite length videos
        if signal_counter < -1000: signal_counter = -500

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