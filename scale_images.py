from PIL import Image
import glob
import cv2

image_list = []
path = "C:/Sync/CodingProjects/VisualStudioCode/CS-4337-Group-5-Final-Project/TensorFlow/workspace/training_demo/images"

for filename in glob.glob(path + '/original/*.jpg'):
    image = Image.open(filename)
    image_list.append(image)

top_width = 0
top_height = 0

for image in image_list:
    width, height = image.size
    
    if width > top_width:
        top_width = width

    if height > top_height:
        top_height = height

output_path = path + '/resized'