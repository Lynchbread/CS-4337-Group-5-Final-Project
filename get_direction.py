import cv2
import numpy as np

# Returns True if getting closer
# Returns False if stationary or moving away


def get_direction(prev_object_centers, object_centers, road_contours):

    if not prev_object_centers or not object_centers:
        return False

    prev_distances = []
    current_distances = []

    for center in prev_object_centers:
        prev_distances.append(get_shortest_distance(center, road_contours))

    for center in object_centers:
        current_distances.append(get_shortest_distance(center, road_contours))

    prev_min = min(prev_distances)
    curr_min = min(current_distances)

    if curr_min == 0.0 or prev_min / curr_min > 1.001:
        return True
    
    return False


def get_shortest_distance(center, contours):

    # Create a binary image to draw contours on
    image = np.zeros((500, 500), dtype=np.uint8)
    cv2.drawContours(image, contours, -1, (255), 1)

    # Find the shortest distance
    shortest_distance = np.float32('inf')

    for contour in contours:
        distance = cv2.pointPolygonTest(contour, center, True)
        if distance < shortest_distance:
            shortest_distance = distance
    
    return shortest_distance

def get_distance(point1, point2):
    return np.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)