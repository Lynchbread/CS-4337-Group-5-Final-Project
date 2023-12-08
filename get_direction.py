import cv2 as cv
import numpy as np

# Returns True if getting closer
# Returns False if stationary or moving away
def get_direction(prev_object_centers, object_centers, road_contours):

    # Returns false if there are no objects in the current or previous frame.
    if not prev_object_centers or not object_centers:
        return False

    prev_distances = []
    current_distances = []

    # Get's a list of the shortest distance between the road and every object
    # in the previous frame.
    for center in prev_object_centers:
        prev_distances.append(get_shortest_distance(center, road_contours))

    # Get's a list of the shortest distance between the road and every object
    # in the current frame.
    for center in object_centers:
        current_distances.append(get_shortest_distance(center, road_contours))

    # Get's the distance of the object closest to the road in both the previous
    # and current frames.
    prev_min = min(prev_distances)
    curr_min = min(current_distances)

    # If the deer object is currently touching the road, or if the deer has moved
    # 5 percent or more closer to the road compared to the previous frame, return True.
    if curr_min == 0.0 or prev_min / curr_min > 1.05:
        return True
    
    # Returns false if the closest deer in the image is either stationary, or is
    # moving away from the road.
    return False

# Gets the shortest distance between the center point and any of the contours
# in the image.
def get_shortest_distance(center, contours):

    # Create a binary image to draw contours on
    image = np.zeros((1280,720), dtype=np.uint8)

    # Draw the contours onto the image
    cv.drawContours(image, contours, -1, (255), 1)

    # Stores the shortest distance
    shortest_distance = np.float32('inf')

    # Iterate throuh all contours and checks each center values' distance to
    # the closest pixel of the contour. Compares all of the distances
    # and keeps the shortest one.
    for contour in contours:
        distance = cv.pointPolygonTest(contour, center, True)
        if distance < shortest_distance:
            shortest_distance = distance
    
    return shortest_distance