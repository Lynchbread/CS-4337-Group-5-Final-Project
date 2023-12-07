import cv2
import numpy as np


def identify_objects(past_frame, current_frame, future_frame):

    # For testing. Delete later
    identify_objects.call += 1

    combined_mask = make_mask(current_frame)

    """
    # For testing. Delete later
    if (identify_objects.call == 100):
        brown_extracted = cv2.bitwise_and(current_frame, current_frame, mask=combined_mask)

        cv2.imwrite("frame.jpg", brown_extracted)
        cv2.imshow("image", brown_extracted)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    """

    binary_image = get_motion_image(past_frame, current_frame, future_frame, 10)

    binary_image = cv2.bitwise_and(binary_image, binary_image, mask=combined_mask)

    binary_image = cv2.erode(binary_image, np.ones((3, 3), np.uint8), iterations=1)
    binary_image = cv2.dilate(binary_image, np.ones((3, 3), np.uint8), iterations=9)

    """
    # For testing. Delete later
    if (identify_objects.call == 99):
        cv2.imshow("image", binary_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    """

    rectangles = get_rectangles(binary_image, 1500)
            
    if len(rectangles) < 2:
        motion = get_motion_image(past_frame, current_frame, future_frame, 1)
        binary_image = cv2.bitwise_and(motion, motion, mask=combined_mask)
        binary_image = cv2.erode(binary_image, np.ones((3, 3), np.uint8), iterations=2)
        binary_image = cv2.dilate(binary_image, np.ones((3, 3), np.uint8), iterations=4)

        rectangles = get_rectangles(binary_image, 1000)

        """
        if identify_objects.call > 240:
            cv2.imshow("image", binary_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        """
        
    
    areas = []

    for rec in rectangles:
        areas.append((rec, rec_area(rec[0], rec[1], rec[2], rec[3])))

    areas.sort(key=lambda x: x[1], reverse=True)

    i = 0
    object_centers = []

    for area in areas:
        if i < 5:
            object_centers.append(rec_center(area[0][0], area[0][1], area[0][2], area[0][3]))
            draw_rectangle(current_frame, area[0][0], area[0][1], area[0][2], area[0][3])
            i += 1
    
    return object_centers

# For testing. Delete later
identify_objects.call = 0

def get_rectangles(frame, threshold):
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(frame, connectivity = 4)

    rectangles = []

    for i in range(1, nb_components):
        if stats[i, cv2.CC_STAT_AREA] > threshold:
            top_row = int(stats[i, cv2.CC_STAT_TOP])
            bottom_row = top_row + int(stats[i, cv2.CC_STAT_HEIGHT])
            left_column = int(stats[i, cv2.CC_STAT_LEFT])
            right_column = left_column + int(stats[i, cv2.CC_STAT_WIDTH])

            rectangles.append((top_row, bottom_row, left_column, right_column))
            #draw_rectangle(current_frame, top_row, bottom_row, left_column, right_column)

    return rectangles

def make_mask(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h = 0.5
    s = 255
    v = 255
    lower1 = np.array([0 * h, 0.1 * s, 0.2 * v], dtype=np.uint8)
    upper1 = np.array([60 * h, 0.25 * s, 0.5 * v], dtype=np.uint8)
    mask1 = cv2.inRange(hsv_frame, lower1, upper1)

    #lower2 = np.array([260 * h, 0.0 * s, 0.4 * v], dtype=np.uint8)
    #upper2 = np.array([280 * h, 0.1 * s, 0.55 * v], dtype=np.uint8)
    #mask2 = cv2.inRange(hsv_frame, lower2, upper2)

    #combined_mask = mask1 | mask2
    combined_mask = mask1

    return combined_mask

def get_motion_image(past_frame, current_frame, future_frame , thresh):
    past_gray = cv2.cvtColor(past_frame, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    future_gray = cv2.cvtColor(future_frame, cv2.COLOR_BGR2GRAY)

    diff1 = cv2.absdiff(past_gray, current_gray)
    diff2 = cv2.absdiff(future_gray, current_gray)

    motion = cv2.min (diff1, diff2)

    threshold, binary_image = cv2.threshold(motion, thresh = thresh, maxval = 255, type = cv2.THRESH_BINARY)

    return binary_image

def rec_area(top, bottom, left, right):
    return (top - bottom) * (right - left)

def rec_center(top, bottom, left, right):
    return ((top+bottom)/2, (left+right)/2)

# Code pulled from Assignment 9, Modifies rectangle color.
def draw_rectangle(img, top, bottom, left, right):
    """
    Draws a rectangle on the input image.

    Args:
    - img: numpy.ndarray - The input image.
    - top: int - The y-coordinate of the top edge of the rectangle.
    - bottom: int - The y-coordinate of the bottom edge of the rectangle.
    - left: int - The x-coordinate of the left edge of the rectangle.
    - right: int - The x-coordinate of the right edge of the rectangle.

    Returns:
    - numpy.ndarray - The input image with the rectangle drawn on it.
    """
    # Determine if the image is grayscale or color
    if len(img.shape) == 2 or img.shape[2] == 1:  # Grayscale
        color = 255  # White color for grayscale
    else:  # Color
        color = (50, 255, 50)  # Green color for RGB
    
    thickness = 2
    cv2.rectangle(img, (left, top), (right, bottom), color, thickness)
    return img