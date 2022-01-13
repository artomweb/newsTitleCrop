import os
from PIL import Image

imageDir = "output/"

images = []

for r, dirs, files in os.walk(imageDir):
    for filename in files:
        images.append(Image.open(imageDir + filename))


images[0].save('output-man.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=120, loop=0)
