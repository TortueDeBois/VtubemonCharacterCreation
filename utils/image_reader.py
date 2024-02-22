from PIL import Image
from PIL.ExifTags import TAGS
import os

# directory path
path = "E:/"

# open images from path
images = []
for file in os.listdir(path):
    if '.png' in file :
        images.append(Image.open(path + file))

# read the image data using PIL
for image in images:
    print(image.info.get("Seed"))