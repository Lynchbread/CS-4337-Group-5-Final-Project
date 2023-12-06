import cv2 
import numpy as np

# Decting road. Additional bugs to fix:
# elimanate the edges detected on boarder of the frame image
# clean road edge line detection

def get_road_lines(frame):



    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color range for the road
    lower_gray = np.array([0, 0, 50])
    upper_gray = np.array([180, 50, 200])

    # Threshold the HSV image to get only road colors
    mask = cv2.inRange(hsv, lower_gray, upper_gray)

    # Apply dilation to fill in the small black holes
    # NOTE: not working
    kernel = np.ones((9, 9), np.uint8)
    # Apply dilation to binary_img
    mask_dilated = cv2.dilate(mask, kernel, iterations=1)

    mask_dilated = cv2.bitwise_not(mask_dilated)

    # Clean up sides of image
    mask_dilated[0:,0:200] = 0
    mask_dilated[0:,-200:] = 0

    contours = cv2.findContours(mask_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #color_image = cv2.cvtColor(mask_dilated, cv2.COLOR_GRAY2BGR)
    #color_image = cv2.drawContours(color_image, contours[0], -1, (255, 0, 0), 3)

    #cv2.imshow('edges', color_image)
    #cv2.waitKey(0)  # Wait indefinitely for a key press
    #cv2.destroyAllWindows()  # Close all OpenCV windows

    for contour in contours[0]:
        area = cv2.contourArea(contour)
        if area < 500:
            mask_dilated = cv2.drawContours(mask_dilated, [contour], 0, (0, 0, 0), -1)

    contours = cv2.findContours(mask_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    return contours[0]

    # Edge detection
    edges = cv2.Canny(mask_dilated, 50, 150)

    # Remove edges along image border
    edges[0:,0:200] = 0
    edges[0:,-200:] = 0

    cv2.imshow('edges', edges)
    cv2.waitKey(0)  # Wait indefinitely for a key press
    cv2.destroyAllWindows()  # Close all OpenCV windows

    # Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, minLineLength=100, maxLineGap=50)

    # Draw lines on the original frame: NEEDS RESTRUCTURING
    line_frame = np.copy(frame)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_frame, (x1, y1), (x2, y2), (255, 0, 0), 5)


    return line_frame

    