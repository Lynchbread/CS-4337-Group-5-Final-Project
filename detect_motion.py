import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# Pass it 2 Mat images, compare the images.
# 'difference' is a double between 0.00 and 1.00. This represents the percent difference threshold
# If the images are more than 'difference' percent different, return True
# I gave difference a default value of 0.1, feel free to change that, I just picked it randomly.
# A difference value of 0.1 means thata the image is 10% different, 90% the same.

def detect_motion (prev_frame, current_frame, next_frame):

    prev_frame = cv.cvtColor(prev_frame, cv.COLOR_BGR2GRAY)
    current_frame = cv.cvtColor(current_frame, cv.COLOR_BGR2GRAY)
    next_frame = cv.cvtColor(next_frame, cv.COLOR_BGR2GRAY)

    diff1 = cv.absdiff(prev_frame, current_frame)
    diff2 = cv.absdiff(current_frame, next_frame)

    motion = cv.min(diff1, diff2)

    thresh, binary_frame = cv.threshold(motion, thresh=10, maxval=255, type=cv.THRESH_BINARY)

    binary_frame = cv.morphologyEx(binary_frame, cv.MORPH_OPEN, kernel=np.ones((3,3)).astype(np.uint8))
    binary_frame = cv.morphologyEx(binary_frame, cv.MORPH_CLOSE, kernel=np.ones((10,10)).astype(np.uint8))

    nb_components, output, stats, centroids = cv.connectedComponentsWithStats(binary_frame, connectivity=4)

    # print(nb_components)

    areas = []
    if nb_components > 1:
        for i in range(1, nb_components):
            areas.append(i, stats[i, cv.CC_STAT_AREA])

        areas = sorted(areas, axis=1, reverse=True)[:5]

        print(areas)

    # largest_components = sorted(stats, reverse=True)[:5]

    # print(len(largest_components))

    # for i in range(1, nb_components):
    #         if stats[i, cv.CC_STAT_AREA] > 1500:
    #             top_row = int(stats[i, cv.CC_STAT_TOP])
    #             bottom_row = top_row + int(stats[i, cv.CC_STAT_HEIGHT])
    #             left_column = int(stats[i, cv.CC_STAT_LEFT])
    #             right_column = left_column + int(stats[i, cv.CC_STAT_WIDTH])


    if nb_components > 1:
        max_label, max_size = max([(i, stats[i, cv.CC_STAT_AREA]) for i in range(1, nb_components)], key=lambda x: x[1])



        binary_frame[output != max_label] = 0

    # binary_frame[output != max_label] = 0

    # plt.figure(figsize=(5,5))
    # plt.imshow(motion, cmap='gray')
    # plt.title('not_green')
    # plt.show()

    return binary_frame