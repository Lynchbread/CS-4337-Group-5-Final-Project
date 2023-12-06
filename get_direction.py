import cv2
import numpy as np

# Returns 1 if getting closer
# Returns 0 if stationary
# Returns -1 if getting further away

def get_direction_any(prev_object_centers, object_centers, road_contours):

    matched_centers = match_centers(object_centers, prev_object_centers)

    for match in match_centers:
        g = 1


def get_direction_one(prev_object_centers, object_centers, road_contours):

    if not prev_object_centers or not object_centers:
        return 0

    prev_distances = []
    current_distances = []

    for center in prev_object_centers:
        prev_distances.append(get_shortest_distance(center, road_contours))

    for center in object_centers:
        current_distances.append(get_shortest_distance(center, road_contours))

    prev_min = min(prev_distances)
    curr_min = min(current_distances)

    direction = prev_min / curr_min

    upper = 1.001
    lower = 0.999

    if direction > upper:
        return 1
    
    if direction < lower:
        return -1
    
    return 0

def match_centers(object_centers, prev_object_centers):

    matched_centers = []

    for center in prev_object_centers:
        nearest = center
        shortest_distance = np.inf(float)
        for prev_center in object_centers:
            distance = get_distance(prev_center, center)
            if distance < shortest_distance:
                shortest_distance = distance
                nearest = prev_center
        if shortest_distance < 50:
            match_centers.append(center, nearest)
        else:
            match_centers.append(center, None)



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