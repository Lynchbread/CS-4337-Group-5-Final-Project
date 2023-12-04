from PIL import Image
import glob
image_list = []
path = "C:/Sync/CodingProjects/VisualStudioCode/CS-4337-Group-5-Final-Project/TensorFlow/workspace/training_demo/images"

for filename in glob.glob(path + '/original/*.gif'): #assuming gif
    im=Image.open(filename)
    image_list.append(im)