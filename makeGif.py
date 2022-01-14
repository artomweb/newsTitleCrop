import os
from PIL import Image
import random


imageDir = "omicronDM/"
SF = 1

images = []

for r, dirs, files in os.walk(imageDir):
    random.shuffle(files[:50])
    for i, filename in enumerate(files):
        img = Image.open(imageDir + filename)
        (width, height) = img.size
        # r = int(i * SF)
        # img = img.crop((r, r, width - r, height - r))
        # img = img.resize((width, height), Image.LANCZOS)
        images.append(img)


images[0].save('output-man.gif',
               save_all=True, append_images=images[1:], optimize=False, duration=120, loop=0)
