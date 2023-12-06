import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

def get_lines(image):

    # Convert bgr to rgb
    rgb_image = cv.cvtColor(image, cv.COLOR_BGR2RGB).astype(np.float32)
    rgb_image = rgb_image.astype(np.float32)

    plt.figure(figsize=(5,5))
    plt.imshow(image)
    plt.title('image')
    plt.show()

    r = rgb_image[:,:,0]
    g = rgb_image[:,:,1]
    b = rgb_image[:,:,2]

    not_green = (1 - ((g - r > -15) & (g - b > -15))).astype(np.uint8)
    green = (g - r > -15) & (g -b > -15).astype(np.uint8)
    green = cv.dilate(green, kernel=np.ones((3,3)))

    overlap = green & not_green

    plt.figure(figsize=(5,5))
    plt.imshow(overlap, cmap='gray')
    plt.title('not_green')
    plt.show()


    plt.figure(figsize=(5,5))
    plt.imshow(not_green, cmap='gray')
    plt.title('not_green')
    plt.show()

    plt.figure(figsize=(5,5))
    plt.imshow(green, cmap='gray')
    plt.title('green')
    plt.show()

    plt.figure(figsize=(15,5))
    plt.subplot(1, 4, 1), plt.imshow(rgb_image/255)
    plt.title('Original Image')
    plt.xticks([]), plt.yticks([])
    plt.subplot(1, 4, 2), plt.imshow(r/(r+g+b), 'Reds', vmin=0.3, vmax=0.5)
    plt.title('R channel')
    plt.xticks([]), plt.yticks([])
    plt.subplot(1, 4, 3), plt.imshow(g/(r+g+b), 'Greens', vmin=0.3, vmax=0.5)
    plt.title('G channel')
    plt.xticks([]), plt.yticks([])
    plt.subplot(1, 4, 4), plt.imshow(b/(r+g+b), 'Blues', vmin=0.3, vmax=0.5)
    plt.title('B channel')
    plt.xticks([]), plt.yticks([])
    plt.show()
    plt.imshow(rgb_image/255)
    plt.show()


    left_line, right_line = 0, 0
    return left_line, right_line
