import cv2
import numpy as np

# Pass it 2 Mat images, compare the images.
# 'difference' is a double between 0.00 and 1.00. This represents the percent difference threshold
# If the images are more than 'difference' percent different, return True
# I gave difference a default value of 0.1, feel free to change that, I just picked it randomly.
# A difference value of 0.1 means thata the image is 10% different, 90% the same.

def detect_motion (curr_frame, prev_frame, difference = 0.1):
    # Convert images to grayscale
    gray_curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    gray_prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    # Compute absolute difference
    diff_frame = cv2.absdiff(gray_curr_frame, gray_prev_frame)

    # Threshold to get the areas with significant changes; NOTE: adjust threshold as necessary
    _, thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)

    # Calculate the percentage of changed pixels
    non_zero_pixels = np.count_nonzero(thresh_frame)
    total_pixels = thresh_frame.shape[0] * thresh_frame.shape[1]
    changed_percent = non_zero_pixels / total_pixels

    # Check if the change is greater than the threshold
    return changed_percent > difference