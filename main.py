import cv2
from extract_frames import extract_frames
from get_road_lines import get_road_lines
from identify_objects import identify_objects
from get_direction import get_direction

def main():

    # Hardcode video path for testing
    # video_path = 'data\\videos\\DeerVideo.mp4'
    video_path = 'data/videos/DeerVideo.mp4'

    # Get video capture, fps, and delay value for playback at original speed
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    delay = int((1 / fps) * 1000)

    # Get first frame in video
    frame_exists, current_frame = video.read()
    
    # Get list containing every frame in video
    frames = extract_frames(video_path)

    # Determines how far back/forward to compare current frame.
    frame_diff, leeway, i = 5, 1, 0

    # How many previous frames in a row the deer needed to move closer to the road to trigger the signal
    if leeway > frame_diff: leeway = frame_diff

    object_centers = [] # List of coordinates containing the center of the deer
    signals = []        # List of signals generated. One for each frame.
    signal_counter = 0  # Used for determing signal display length later in the code

    # Loop until video ends (exit using 'ctrl+C' or simply 'q')
    while frame_exists:

        if i >= frame_diff:

            prev_frame = frames[i - frame_diff]

            # Bounds check to prevent trying to grab frames past the end of the video.
            if i + frame_diff < len(frames):
                next_frame = frames[i + frame_diff]
            else: break

            prev_object_centers = object_centers

            # Identifies the center of all moving deer in the frame.
            object_centers = identify_objects(prev_frame, current_frame, next_frame)

            # Gets the contours of the road in the frame.
            road_contours = get_road_lines(current_frame)

            # Draws the road contours onto the current frame
            for contour in road_contours:
                current_frame = cv2.drawContours(current_frame, [contour], 0, (0, 0, 0), 3)

            # Gets whether or not the deer are moving closer to the road, and signals appropriately
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
            current_frame[0:100,0:100] = (0,128,128) # Yellow if objects are stationary or moving away from the road for at least 1 second
        else:
            current_frame[0:100,0:100] = (0,128,0) # Green if objects are stationary or moving away from the road for at least 3 seconds

        # Allows for infinite length videos by preventing signal_counter from going to negative infinity.
        if signal_counter < -1000: signal_counter = -500

        # Show current_frame
        cv2.imshow('frame', current_frame)

        # Extract current frame
        frame_exists, current_frame = video.read()

        # Introduce delay, stop playback if 'q' pressed
        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

        # iterate to next frame
        i += 1

    # Exit program gracefully
    video.release()
    cv2.destroyAllWindows()

 
if __name__ == '__main__':
    main()