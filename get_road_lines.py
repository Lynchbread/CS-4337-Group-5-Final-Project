import cv2 as cv
import numpy as np

# Returns the contours of the road in the frame
def get_road_lines(frame):

    # Convert to HSV color space
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Define color range for the road
    lower_gray = np.array([0, 0, 50])
    upper_gray = np.array([180, 50, 200])

    # Threshold the HSV image to get only road colors
    mask = cv.inRange(hsv, lower_gray, upper_gray)

    # Apply dilation to fill in the small black holes
    kernel = np.ones((9, 9), np.uint8)
    mask_dilated = cv.dilate(mask, kernel, iterations=1)

    # Invert image
    mask_dilated = cv.bitwise_not(mask_dilated)

    # Clean up sides of image
    mask_dilated[0:,0:200] = 0
    mask_dilated[0:,-200:] = 0

    # Find all contours in image.
    contours = cv.findContours(mask_dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    # Removes noise from the image be removing any small contours, leaving only the road contours.
    for contour in contours[0]:
        area = cv.contourArea(contour)
        if area < 1000:
            mask_dilated = cv.drawContours(mask_dilated, [contour], 0, (0, 0, 0), -1)

    # Reaquires the road contours now that image is denoised.
    contours = cv.findContours(mask_dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    return contours[0]